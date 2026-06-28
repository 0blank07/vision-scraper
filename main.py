import time
import cv2
import os
import json
import threading
import queue
from adb_controller import ADBController
from screen_parser import ScreenParser
from data_manager import DataManager

class ScraperBot:
    def __init__(self):
        self.adb = ADBController()
        self.parser = ScreenParser()
        self.data_mgr = DataManager()
        
        # --- PRECISE COORDINATES FROM USER ---
        self.coords = {
            "signings": (808, 844),
            "error_ok": (800, 600),
            "search_home": (235, 705),
            "search_results": (1441, 121),
            "min_ovr": (784, 335),
            "max_ovr": (1052, 334),
            "search_submit": (1060, 822),
            "card_1": (637, 310), # 1st player card
            "panel_card": (1354, 357), # Player card in right panel
            "skills": [
                (1067, 672), (1138, 671), (1210, 672), 
                (1282, 672), (1357, 672), (1428, 671)
            ],
            "skill_lvl_2": (927, 271),
            "skill_lvl_3": (940, 475),
            "skill_close": (1102, 271),
            "tab_attributes": (465, 850),
            "tab_playstyles": (791, 848),
            "playstyle_i_1": (734, 311),
            "playstyle_i_2": (1070, 312),
            "playstyle_close": (1305, 80),
            "tab_traits": (1122, 848),
            "go_back": (54, 45)
        }
        
        self.bboxes = {}
        if os.path.exists("bounding_boxes.json"):
            with open("bounding_boxes.json", "r") as f:
                self.bboxes = json.load(f)
                
        # --- ASYNC OCR QUEUE ---
        # CRITICAL SAFETY: maxsize=2 prevents catastrophic RAM explosion (OOM). 
        # Each player holds ~150MB of raw images. If the Clicker outpaces the OCR AI,
        # it will pause and wait for the queue to drain, capping memory at ~300MB.
        # Threading Event to pause OCR during critical UI animations (like scrolling)
        self.animation_lock = threading.Event()
        self.animation_lock.set() # Allow worker to run by default
        
        self.task_queue = queue.Queue(maxsize=2)
        self.worker_thread = threading.Thread(target=self._ocr_worker, daemon=True)
        self.worker_thread.start()
        print(">> Asynchronous OCR Background Worker Started.")

    def _ocr_worker(self):
        while True:
            # Industry Standard: Yield CPU if the main thread is performing a critical UI animation
            self.animation_lock.wait() 
            
            task = self.task_queue.get()
            if task is None: break
            
            try:
                ovr, player_number, images, player_data = task
                print(f"  [OCR Worker] Processing Player {player_number} (OVR {ovr})...")
                
                # Step 8: Side Panel Shards & Card
                if images.get("panel") is not None:
                    if "img_card" in self.bboxes:
                        filepath = f"output/images/cards/ovr{ovr}_p{player_number}.png"
                        self.parser.crop_and_save(images["panel"], self.bboxes["img_card"], filepath)
                    if "shard_value" in self.bboxes:
                        player_data["shards"] = self.parser.extract_text(images["panel"], bbox=self.bboxes["shard_value"])

                # Step 10: Overview Tab
                if images.get("overview") is not None:
                    for key in ["full_name", "position", "height", "weight", "preferred_foot", "ovr"]:
                        if key in self.bboxes:
                            player_data[key] = self.parser.extract_text(images["overview"], bbox=self.bboxes[key])
                    for key in ["stamina_stars", "skill_moves_stars"]:
                        if key in self.bboxes:
                            player_data[key] = self.parser.count_stars(images["overview"], bbox=self.bboxes[key])
                    for key in ["img_nation", "img_league"]:
                        if key in self.bboxes:
                            filepath = f"output/images/{key}/ovr{ovr}_p{player_number}.png"
                            self.parser.crop_and_save(images["overview"], self.bboxes[key], filepath)

                # Step 11-14: Skills
                for s_data in images.get("skills", []):
                    parsed_skill = {"skill_number": s_data["skill_number"]}
                    
                    def process_skill_level(level_name, img_s, img_s_scroll):
                        if img_s is None: return
                        if "skill_name" in self.bboxes and "name" not in parsed_skill:
                            parsed_skill["name"] = self.parser.extract_text(img_s, bbox=self.bboxes["skill_name"])
                        if "img_skill" in self.bboxes and "image_saved" not in parsed_skill:
                            filepath = f"output/images/skills/ovr{ovr}_p{player_number}_s{parsed_skill['skill_number']}.png"
                            self.parser.crop_and_save(img_s, self.bboxes["img_skill"], filepath)
                            parsed_skill["image_saved"] = True
                        if "unlock_requirements" in self.bboxes:
                            req_text = self.parser.extract_text(img_s, bbox=self.bboxes["unlock_requirements"])
                            if req_text.strip(): parsed_skill[f"level_{level_name}_requirements"] = req_text
                        if "alt_positino" in self.bboxes:
                            alt_pos = self.parser.extract_text(img_s, bbox=self.bboxes["alt_positino"])
                            if alt_pos.strip(): parsed_skill[f"level_{level_name}_alt_position"] = alt_pos
                        if "sub_category_skill_boosts" in self.bboxes:
                            bbox = self.bboxes["sub_category_skill_boosts"]
                            boosts1 = self.parser.parse_skill_boosts(self.parser.extract_text(img_s, bbox=bbox))
                            boosts2 = {}
                            if img_s_scroll is not None:
                                boosts2 = self.parser.parse_skill_boosts(self.parser.extract_text(img_s_scroll, bbox=bbox))
                            parsed_skill[f"level_{level_name}_boosts"] = {**boosts1, **boosts2}
                            
                    if "level_1" in s_data: process_skill_level("1", s_data["level_1"], s_data.get("level_1_scroll"))
                    if "level_2" in s_data: process_skill_level("2", s_data["level_2"], s_data.get("level_2_scroll"))
                    if "level_3" in s_data: process_skill_level("3", s_data["level_3"], s_data.get("level_3_scroll"))
                    
                    player_data["skills"].append(parsed_skill)

                # Step 15: Attributes
                if images.get("attributes") is not None and "attributes" in self.bboxes:
                    raw_text = self.parser.extract_text(images["attributes"], bbox=self.bboxes["attributes"])
                    player_data["attributes"] = self.parser.parse_attributes(raw_text)

                # Step 16-18: Playstyles
                for j, img_ps in enumerate(images.get("playstyles", [])):
                    if img_ps is not None:
                        ps_data = {}
                        for key in ["playstyle_name", "playstyle_level", "playstyle_description"]:
                            if key in self.bboxes:
                                ps_data[key] = self.parser.extract_text(img_ps, bbox=self.bboxes[key])
                        if "img_playstyle" in self.bboxes:
                            filepath = f"output/images/playstyles/ovr{ovr}_p{player_number}_ps{j+1}.png"
                            self.parser.crop_and_save(img_ps, self.bboxes["img_playstyle"], filepath)
                        player_data["playstyles"].append(ps_data)

                # Step 19: Traits
                if images.get("traits") is not None:
                    img_traits = images["traits"]
                    for key in ["event_name", "work_rate_att", "work_rate_def"]:
                        if key in self.bboxes:
                            player_data[key] = self.parser.extract_text(img_traits, bbox=self.bboxes[key])
                    player_data["traits"] = []
                    for t in range(1, 9):
                        name_key = f"trait_name_{t}"
                        img_key = f"img_trait_{t}"
                        if name_key in self.bboxes:
                            trait_name = self.parser.extract_text(img_traits, bbox=self.bboxes[name_key])
                            if len(trait_name) > 2:
                                trait_data = {"name": trait_name}
                                if img_key in self.bboxes:
                                    filepath = f"output/images/traits/ovr{ovr}_p{player_number}_t{t}.png"
                                    self.parser.crop_and_save(img_traits, self.bboxes[img_key], filepath)
                                player_data["traits"].append(trait_data)

                # Save data
                self.data_mgr.save_player(player_data)
                print(f"  [OCR Worker] Completed and Saved Player {player_number} (OVR {ovr}).")
                
            except Exception as e:
                print(f"  [OCR Worker] Error processing Player {player_number}: {e}")
            finally:
                self.task_queue.task_done()

    def check_and_recover_error(self):
        img = self.adb.get_screenshot()
        if img is None: return None
        text = self.parser.extract_text(img, (200, 200, 1400, 700))
        if "UNKNOWN" in text or "token" in text.lower() or "network" in text.lower() or "Error at line" in text:
            print("\n>> Network error detected! Clicking OK...")
            self.adb.click(*self.coords["error_ok"])
            time.sleep(5)
            img_after = self.adb.get_screenshot()
            text_after = self.parser.extract_text(img_after, (0, 700, 1600, 900))
            if "STORE" in text_after or "EXCHANGE" in text_after or "QUESTS" in text_after:
                print(">> Error kicked us to Home Screen.")
                return "HOME"
            else:
                print(">> Error dismissed, stayed on current screen.")
                return "RESULTS"
        return None

    def navigate_to_search(self, ovr, from_results=False):
        while True:
            print(f"\n--- Setting up Search for OVR {ovr} ---")
            if not from_results:
                print("Step 1: Clicking SIGNINGS...")
                self.adb.click(*self.coords["signings"])
                time.sleep(4)
                if self.check_and_recover_error() == "HOME":
                    print("Recovering from Home -> Signings again...")
                    self.adb.click(*self.coords["signings"])
                    time.sleep(4)
                print("Step 3: Clicking Search Button...")
                self.adb.click(*self.coords["search_home"])
                time.sleep(2)
            else:
                print("Step 22: Clicking Search Filter from Results...")
                self.adb.click(*self.coords["search_results"])
                time.sleep(2)

            print("Step 4: Entering MIN OVR...")
            self.adb.click(*self.coords["min_ovr"])
            time.sleep(1)
            self.adb.input_text(str(ovr))
            time.sleep(1)
            self.adb.click(845, 401)
            time.sleep(1)

            print("Step 5: Entering MAX OVR...")
            self.adb.click(*self.coords["max_ovr"])
            time.sleep(1)
            for _ in range(3):
                self.adb.keyevent(67)
                time.sleep(0.2)
            self.adb.input_text(str(ovr))
            time.sleep(1)
            self.adb.click(1060, 401)
            time.sleep(1)

            print("Step 6: Waiting 2 seconds then submitting Search...")
            time.sleep(2)
            self.adb.click(*self.coords["search_submit"])
            time.sleep(8)
            
            if self.check_and_recover_error() == "HOME":
                print("Error on submit kicked to Home. Restarting full navigation...")
                from_results = False
                continue
                
            print("Navigation to results successful!")
            break

    def process_player(self, ovr, player_number=1, card_x=624, card_y=310):
        print(f"\n--- Fast Capturing Player {player_number} (OVR {ovr}) ---")
        player_data = {"OVR": ovr, "player_index": player_number, "skills": [], "playstyles": []}
        images = {}
        
        # BULLETPROOF FAILSAFE: Take picture before clicking grid
        img_before_grid = self.adb.get_screenshot()
        
        self.adb.click(card_x, card_y)
        time.sleep(1.0)
        
        images["panel"] = self.adb.get_screenshot()
        
        # Check if the screen actually changed (did the side panel open or update?)
        if img_before_grid is not None and images["panel"] is not None:
            diff = cv2.absdiff(img_before_grid, images["panel"])
            non_zero = cv2.countNonZero(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY))
            if non_zero < 10000:
                print(f">> Screen didn't change enough (Diff: {non_zero}). Clicked an empty grid space. Aborting.")
                return False
        
        self.adb.click(*self.coords["panel_card"])
        time.sleep(1.5)
        
        images["overview"] = self.adb.get_screenshot()
        
        # BULLETPROOF FAILSAFE 2: Did the side panel actually change?
        # If we click an empty grid space, the side panel stays open on the previous player!
        if hasattr(self, 'last_overview') and self.last_overview is not None and images["overview"] is not None:
            # Crop to the right side panel [y_start:y_end, x_start:x_end] to avoid grid animations
            patch_old = self.last_overview[200:800, 1100:1600]
            patch_new = images["overview"][200:800, 1100:1600]
            diff_panel = cv2.absdiff(patch_old, patch_new)
            non_zero_panel = cv2.countNonZero(cv2.cvtColor(diff_panel, cv2.COLOR_BGR2GRAY))
            
            if non_zero_panel < 5000:
                print(f">> Overview panel didn't change (Diff: {non_zero_panel}). Clicked empty space or same player. Aborting row.")
                return False
                
        if images["overview"] is not None:
            self.last_overview = images["overview"].copy()
            
        # Ensure the summary page is actually loaded
        if images["overview"] is not None and "card_name" in self.bboxes:
            card_name = self.parser.extract_text(images["overview"], bbox=self.bboxes["card_name"])
            if len(card_name.strip()) < 2:
                print(">> Warning: Name missing. Summary page might be slow to load. Retrying...")
                time.sleep(1.0)
                images["overview"] = self.adb.get_screenshot()
                card_name = self.parser.extract_text(images["overview"], bbox=self.bboxes["card_name"])
                if len(card_name.strip()) < 2:
                    print(">> Still couldn't read player name (OCR failure). Proceeding anyway...")
                    card_name = "Unknown"
                    
            # DUPLICATE DETECTION: If we hit the exact same player again, the scroll lagged!
            if hasattr(self, 'recent_names') and card_name != "Unknown" and card_name in self.recent_names:
                print(f">> DUPLICATE DETECTED ({card_name})! The grid scroll must have failed/lagged.")
                self.adb.click(*self.coords["go_back"])
                time.sleep(1.0)
                return "DUPLICATE"
                
            player_data["card_name"] = card_name
            
            # Store in recent names for duplicate detection (keep last 8)
            if not hasattr(self, 'recent_names'): self.recent_names = []
            if card_name != "Unknown":
                self.recent_names.append(card_name)
                if len(self.recent_names) > 8: self.recent_names.pop(0)
            
        player_max_level = None
        images["skills"] = []
        for i, skill_coord in enumerate(self.coords["skills"]):
            self.adb.click(*skill_coord)
            time.sleep(1.0)
            
            s_data = {"skill_number": i+1}
            
            s_data["level_1"] = self.adb.get_screenshot()
            self.adb.swipe(800, 600, 800, 300, 500)
            time.sleep(1.0)
            s_data["level_1_scroll"] = self.adb.get_screenshot()
            self.adb.swipe(800, 300, 800, 600, 500)
            time.sleep(1.0)
            
            if player_max_level is None:
                self.adb.click(952, 270)
                time.sleep(1.0)
                img_drop = self.adb.get_screenshot()
                max_level = 1
                if img_drop is not None:
                    drop_text = self.parser.extract_text(img_drop, (900, 380, 1000, 520)).lower()
                    if "3" in drop_text or "level 3" in drop_text: max_level = 3
                    elif "2" in drop_text or "level 2" in drop_text: max_level = 2
                player_max_level = max_level
                if player_max_level == 1:
                    self.adb.click(952, 270)
                    time.sleep(1.0)
                    
            if player_max_level >= 2:
                if i != 0:
                    self.adb.click(952, 270)
                    time.sleep(1.0)
                self.adb.click(941, 411)
                time.sleep(1.0)
                s_data["level_2"] = self.adb.get_screenshot()
                self.adb.swipe(800, 600, 800, 300, 500)
                time.sleep(1.0)
                s_data["level_2_scroll"] = self.adb.get_screenshot()
                self.adb.swipe(800, 300, 800, 600, 500)
                time.sleep(1.0)
                
            if player_max_level == 3:
                self.adb.click(952, 270)
                time.sleep(1.0)
                self.adb.click(940, 474)
                time.sleep(1.0)
                s_data["level_3"] = self.adb.get_screenshot()
                self.adb.swipe(800, 600, 800, 300, 500)
                time.sleep(1.0)
                s_data["level_3_scroll"] = self.adb.get_screenshot()
                self.adb.swipe(800, 300, 800, 600, 500)
                time.sleep(1.0)
                
            self.adb.click(1104, 271)
            time.sleep(1.0)
            images["skills"].append(s_data)
            
        self.adb.click(*self.coords["tab_attributes"])
        time.sleep(1.0)
        images["attributes"] = self.adb.get_screenshot()
        
        self.adb.click(*self.coords["tab_playstyles"])
        time.sleep(1.0)
        images["playstyles"] = []
        
        self.adb.click(*self.coords["playstyle_i_1"])
        time.sleep(1.0)
        images["playstyles"].append(self.adb.get_screenshot())
        self.adb.click(*self.coords["playstyle_close"])
        time.sleep(1.0)
        
        self.adb.click(*self.coords["playstyle_i_2"])
        time.sleep(1.0)
        images["playstyles"].append(self.adb.get_screenshot())
        self.adb.click(*self.coords["playstyle_close"])
        time.sleep(1.0)
        
        self.adb.click(*self.coords["tab_traits"])
        time.sleep(1.0)
        images["traits"] = self.adb.get_screenshot()
        
        self.adb.click(*self.coords["go_back"])
        time.sleep(1.5)
        
        # OFF-LOAD HEAVY OCR TO BACKGROUND WORKER
        self.task_queue.put((ovr, player_number, images, player_data))
        return True

    def swipe_list_and_check(self):
        print(">> Pausing background AI for 2 seconds to guarantee a perfectly smooth scroll...")
        self.animation_lock.clear() # Pauses the OCR worker instantly
        
        for attempt in range(2):
            img_before = self.adb.get_screenshot()
            
            # Using the exact smooth scroll coordinates (increased duration by 10% to 2200ms)
            self.adb.swipe(800, 650, 800, 400, 2200)
            time.sleep(3.5)
            
            img_after = self.adb.get_screenshot()
            
            patch_before = img_before[450:550, 100:300]
            patch_after = img_after[450:550, 100:300]
            
            diff = cv2.absdiff(patch_before, patch_after)
            non_zero = cv2.countNonZero(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY))
            
            if non_zero > 1000:
                self.animation_lock.set() # Unpause the worker!
                return True
                
            print(f">> Swipe failed to move screen (Diff: {non_zero}). Retrying to ensure it wasn't dropped by lag...")
            
        self.animation_lock.set() # Unpause if we fail
        return False

    def set_search_filter(self, ovr):
        print(f"Setting Search Filter for OVR {ovr}...")
        self.adb.click(1425, 125)
        time.sleep(1.5)
        self.adb.click(782, 337)
        time.sleep(0.5)
        for _ in range(3): self.adb.keyevent(67)
        self.adb.input_text(str(ovr))
        self.adb.click(948, 428)
        time.sleep(0.5)
        self.adb.click(1048, 335)
        time.sleep(0.5)
        for _ in range(3): self.adb.keyevent(67)
        self.adb.input_text(str(ovr))
        self.adb.click(1048, 398)
        time.sleep(0.5)
        self.adb.click(1060, 824)
        print("Waiting for results to load...")
        time.sleep(1.5)

    def run_full_scrape(self):
        print("Starting Full Scrape Task (OVR 120 -> 110)")
        os.makedirs("output", exist_ok=True)
        self.navigate_to_search(120, from_results=False)
        player_counter = 1
        
        for ovr in range(120, 109, -1):
            if ovr < 120: self.set_search_filter(ovr)
            
            row1_coords = [(637, 310), (425, 417), (702, 417), (975, 415)]
            ovr_complete = False
            for (cx, cy) in row1_coords:
                if not self.process_player(ovr, player_number=player_counter, card_x=cx, card_y=cy):
                    ovr_complete = True
                    break
                player_counter += 1
                
            if ovr_complete:
                print(f"Finished scraping all players for OVR {ovr}.")
                continue
                
            row2_coords = [(151, 501), (424, 501), (700, 501), (977, 504)]
            consecutive_scroll_fails = 0
            
            while True:
                scrolled = self.swipe_list_and_check()
                if not scrolled:
                    print("Reached the bottom of the list!")
                    break
                
                print("Scrolled successfully, processing new row...")
                row_failed = False
                for i, (cx, cy) in enumerate(row2_coords):
                    result = self.process_player(ovr, player_number=player_counter, card_x=cx, card_y=cy)
                    
                    if result == "DUPLICATE":
                        print(">> Duplicate caught! Triggering corrective scroll...")
                        row_failed = True
                        break
                        
                    if not result:
                        if i == 0:
                            print(">> Missed the first card! The emulator probably lagged during the scroll. Retrying swipe...")
                            row_failed = True
                            break
                        else:
                            # If we miss the 2nd, 3rd, or 4th card, it's just a half-empty row. Safely end the OVR.
                            ovr_complete = True
                            break
                    
                    player_counter += 1
                    consecutive_scroll_fails = 0 # Reset counter on successful click
                    
                if row_failed:
                    consecutive_scroll_fails += 1
                    if consecutive_scroll_fails >= 2:
                        print(">> Failed to find a card twice. We must be at the end of the OVR.")
                        ovr_complete = True
                        break
                    continue # Loop back and swipe again!
                    
                if ovr_complete: break
            
            if ovr_complete:
                print(f"Finished scraping all players for OVR {ovr}.")
                continue
            
            print("Processing the final row attached to the footer...")
            last_row_coords = [(144, 612), (431, 610), (708, 617), (987, 615)]
            for (cx, cy) in last_row_coords:
                if not self.process_player(ovr, player_number=player_counter, card_x=cx, card_y=cy):
                    break
                player_counter += 1
            print(f"Finished scraping all players for OVR {ovr}.")
            
        print("Waiting for final background OCR tasks to complete...")
        self.task_queue.join()
        print("Scrape Complete!")

if __name__ == "__main__":
    bot = ScraperBot()
    # bot.run_full_scrape()
