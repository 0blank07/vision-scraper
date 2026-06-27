import time
import cv2
import os
import json
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
            import json
            with open("bounding_boxes.json", "r") as f:
                self.bboxes = json.load(f)

    def check_and_recover_error(self):
        """Checks for error, clicks OK. Returns 'HOME', 'RESULTS', or None."""
        img = self.adb.get_screenshot()
        if img is None: return None
        
        text = self.parser.extract_text(img, (200, 200, 1400, 700))
        if "UNKNOWN" in text or "token" in text.lower() or "network" in text.lower() or "Error at line" in text:
            print("\n>> Network error detected! Clicking OK...")
            self.adb.click(*self.coords["error_ok"])
            time.sleep(5) # Wait to see where game redirects
            
            # Check where we ended up
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
        """Steps 1 to 6: Navigates to search and enters OVR."""
        while True:
            print(f"\n--- Setting up Search for OVR {ovr} ---")
            
            if not from_results:
                # Step 1: Click Signings
                print("Step 1: Clicking SIGNINGS...")
                self.adb.click(*self.coords["signings"])
                time.sleep(4)
                
                # Step 2: Handle potential error and redirect
                state = self.check_and_recover_error()
                if state == "HOME":
                    print("Recovering from Home -> Signings again...")
                    self.adb.click(*self.coords["signings"])
                    time.sleep(4)
                
                # Step 3: Click Search Button (Home variant)
                print("Step 3: Clicking Search Button...")
                self.adb.click(*self.coords["search_home"])
                time.sleep(2)
            else:
                # Step 22: Click Search Button (Results variant)
                print("Step 22: Clicking Search Filter from Results...")
                self.adb.click(*self.coords["search_results"])
                time.sleep(2)

            # Step 4: Min OVR
            print("Step 4: Entering MIN OVR...")
            self.adb.click(*self.coords["min_ovr"])
            time.sleep(1)
            self.adb._run_cmd(["adb", "-s", self.adb.device_id, "shell", "input", "text", str(ovr)])
            time.sleep(1)
            self.adb.click(845, 401) # New click after Min OVR input
            time.sleep(1)

            # Step 5: Max OVR
            print("Step 5: Entering MAX OVR...")
            self.adb.click(*self.coords["max_ovr"])
            time.sleep(1)
            # Hit backspace 3 times to clear previous input
            for _ in range(3):
                self.adb._run_cmd(["adb", "-s", self.adb.device_id, "shell", "input", "keyevent", "67"])
                time.sleep(0.2)
            self.adb._run_cmd(["adb", "-s", self.adb.device_id, "shell", "input", "text", str(ovr)])
            time.sleep(1)
            self.adb.click(1060, 401) # New click after Max OVR input
            time.sleep(1)

            # Step 6: Click Search Submit
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
        """Steps 7 to 20: Full deep dive extraction for a single player."""
        print(f"\n--- Processing Player {player_number} (OVR {ovr}) ---")
        player_data = {"OVR": ovr, "player_index": player_number, "skills": [], "playstyles": []}
        
        # Step 7: Click Player Card
        print("Step 7: Clicking player card in grid...")
        self.adb.click(card_x, card_y)
        time.sleep(4)
        
        # Step 8: Side Panel - Shards & Card Screenshot
        print("Step 8: Recording shards and capturing card image...")
        img_panel = self.adb.get_screenshot()
        if img_panel is not None:
            if "img_card" in self.bboxes:
                filepath = f"output/images/cards/ovr{ovr}_p{player_number}.png"
                self.parser.crop_and_save(img_panel, self.bboxes["img_card"], filepath)
            
            if "shard_value" in self.bboxes:
                player_data["shards"] = self.parser.extract_text(img_panel, bbox=self.bboxes["shard_value"])
        
        # Step 9: Click Player Card in Panel
        print("Step 9: Opening Full Profile...")
        self.adb.click(*self.coords["panel_card"])
        time.sleep(4)
        
        # Step 10: Overview Tab
        print("Step 10: Extracting Overview Data...")
        img_overview = self.adb.get_screenshot()
        if img_overview is not None:
            for key in ["full_name", "card_name", "position", "height", "weight", "preferred_foot", "ovr"]:
                if key in self.bboxes:
                    player_data[key] = self.parser.extract_text(img_overview, bbox=self.bboxes[key])
            
            for key in ["stamina_stars", "skill_moves_stars"]:
                if key in self.bboxes:
                    player_data[key] = self.parser.count_stars(img_overview, bbox=self.bboxes[key])
                    
            for key in ["img_nation", "img_league"]:
                if key in self.bboxes:
                    filepath = f"output/images/{key}/ovr{ovr}_p{player_number}.png"
                    self.parser.crop_and_save(img_overview, self.bboxes[key], filepath)
        
        # Step 11, 12, 13, 14: Skills
        print("Step 11-14: Processing Skills...")
        for i, skill_coord in enumerate(self.coords["skills"]):
            self.adb.click(*skill_coord)
            time.sleep(2)
            
            skill_data = {"skill_number": i+1}
            
            def extract_skill_boosts(level_name):
                print(f"  > Skill {i+1}: Recording Level {level_name}...")
                img_s = self.adb.get_screenshot()
                if img_s is None: return
                
                if "skill_name" in self.bboxes and "name" not in skill_data:
                    skill_data["name"] = self.parser.extract_text(img_s, bbox=self.bboxes["skill_name"])
                    
                if "img_skill" in self.bboxes and "image_saved" not in skill_data:
                    filepath = f"output/images/skills/ovr{ovr}_p{player_number}_s{i+1}.png"
                    self.parser.crop_and_save(img_s, self.bboxes["img_skill"], filepath)
                    skill_data["image_saved"] = True
                    
                if "unlock_requirements" in self.bboxes:
                    req_text = self.parser.extract_text(img_s, bbox=self.bboxes["unlock_requirements"])
                    if len(req_text.strip()) > 0:
                        skill_data[f"level_{level_name}_requirements"] = req_text
                        
                if "alt_positino" in self.bboxes:
                    alt_pos = self.parser.extract_text(img_s, bbox=self.bboxes["alt_positino"])
                    if len(alt_pos.strip()) > 0:
                        skill_data[f"level_{level_name}_alt_position"] = alt_pos
                    
                if "sub_category_skill_boosts" in self.bboxes:
                    bbox = self.bboxes["sub_category_skill_boosts"]
                    text1 = self.parser.extract_text(img_s, bbox=bbox)
                    boosts1 = self.parser.parse_skill_boosts(text1)
                    
                    # Scroll down list
                    self.adb._run_cmd(["adb", "-s", self.adb.device_id, "shell", "input", "swipe", "800", "600", "800", "300", "500"])
                    time.sleep(1)
                    
                    img_s_scroll = self.adb.get_screenshot()
                    text2 = self.parser.extract_text(img_s_scroll, bbox=bbox)
                    boosts2 = self.parser.parse_skill_boosts(text2)
                    
                    skill_data[f"level_{level_name}_boosts"] = {**boosts1, **boosts2}
                    
                    # Reset scroll
                    self.adb._run_cmd(["adb", "-s", self.adb.device_id, "shell", "input", "swipe", "800", "300", "800", "600", "500"])
                    time.sleep(1)

            # 1. Record Level 1 (Default)
            extract_skill_boosts("1")
            
            # 2. Open Dropdown
            self.adb.click(952, 270)
            time.sleep(1.5)
            
            # Check levels
            img_drop = self.adb.get_screenshot()
            max_level = 1
            if img_drop is not None:
                drop_text = self.parser.extract_text(img_drop, (900, 380, 1000, 520)).lower()
                if "3" in drop_text or "level 3" in drop_text:
                    max_level = 3
                elif "2" in drop_text or "level 2" in drop_text:
                    max_level = 2
            
            print(f"    Detected {max_level} levels for this skill.")
            
            # 3. Process Level 2
            if max_level >= 2:
                self.adb.click(941, 411)
                time.sleep(1.5)
                extract_skill_boosts("2")
                
            # 4. Process Level 3
            if max_level == 3:
                self.adb.click(952, 270)
                time.sleep(1.5)
                self.adb.click(940, 474)
                time.sleep(1.5)
                extract_skill_boosts("3")
            elif max_level == 1:
                self.adb.click(952, 270)
                time.sleep(1)

            # Step 14: Close Skill Window
            self.adb.click(1104, 271)
            time.sleep(1.5)
            player_data["skills"].append(skill_data)

        # Step 15: Attributes Tab
        print("Step 15: Extracting Attributes...")
        self.adb.click(*self.coords["tab_attributes"])
        time.sleep(2)
        img_attr = self.adb.get_screenshot()
        if img_attr is not None and "attributes" in self.bboxes:
            raw_text = self.parser.extract_text(img_attr, bbox=self.bboxes["attributes"])
            player_data["attributes"] = self.parser.parse_attributes(raw_text)
        
        # Step 16: Playstyles Tab
        print("Step 16-18: Extracting Playstyles...")
        self.adb.click(*self.coords["tab_playstyles"])
        time.sleep(2)
        
        def process_playstyle(j):
            img_ps = self.adb.get_screenshot()
            if img_ps is not None:
                ps_data = {}
                for key in ["playstyle_name", "playstyle_level", "playstyle_description"]:
                    if key in self.bboxes:
                        ps_data[key] = self.parser.extract_text(img_ps, bbox=self.bboxes[key])
                if "img_playstyle" in self.bboxes:
                    filepath = f"output/images/playstyles/ovr{ovr}_p{player_number}_ps{j+1}.png"
                    self.parser.crop_and_save(img_ps, self.bboxes["img_playstyle"], filepath)
                player_data["playstyles"].append(ps_data)

        # Step 17: Playstyle 1
        self.adb.click(*self.coords["playstyle_i_1"])
        time.sleep(1.5)
        process_playstyle(0)
        self.adb.click(*self.coords["playstyle_close"])
        time.sleep(1)
        
        # Step 18: Playstyle 2
        self.adb.click(*self.coords["playstyle_i_2"])
        time.sleep(1.5)
        process_playstyle(1)
        self.adb.click(*self.coords["playstyle_close"])
        time.sleep(1)

        # Step 19: Traits Tab
        print("Step 19: Extracting Traits...")
        self.adb.click(*self.coords["tab_traits"])
        time.sleep(2)
        img_traits = self.adb.get_screenshot()
        if img_traits is not None:
            for key in ["event_name", "work_rate_att", "work_rate_def"]:
                if key in self.bboxes:
                    player_data[key] = self.parser.extract_text(img_traits, bbox=self.bboxes[key])
                    
            player_data["traits"] = []
            for t in range(1, 9):
                name_key = f"trait_name_{t}"
                img_key = f"img_trait_{t}"
                if name_key in self.bboxes:
                    trait_name = self.parser.extract_text(img_traits, bbox=self.bboxes[name_key])
                    # If trait name is found, save it and its icon
                    if len(trait_name) > 2:
                        trait_data = {"name": trait_name}
                        if img_key in self.bboxes:
                            filepath = f"output/images/traits/ovr{ovr}_p{player_number}_t{t}.png"
                            self.parser.crop_and_save(img_traits, self.bboxes[img_key], filepath)
                        player_data["traits"].append(trait_data)

        # Save data
        self.data_mgr.save_player(player_data)

        # Step 20: Go Back to Results
        print("Step 20: Going back to Results...")
        self.adb.click(*self.coords["go_back"])
        time.sleep(3)

    def swipe_list_and_check(self):
        """Swipes the grid up and returns True if the screen actually moved."""
        img_before = self.adb.get_screenshot()
        # Swipe UP from bottom to top to scroll down
        self.adb._run_cmd(["adb", "-s", self.adb.device_id, "shell", "input", "swipe", "800", "700", "800", "300", "600"])
        time.sleep(2)
        img_after = self.adb.get_screenshot()
        
        # Compare a patch on the left side where cards sit (X: 100-300, Y: 450-550)
        patch_before = img_before[450:550, 100:300]
        patch_after = img_after[450:550, 100:300]
        
        diff = cv2.absdiff(patch_before, patch_after)
        non_zero = cv2.countNonZero(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY))
        
        # If enough pixels changed, the screen actually scrolled
        return non_zero > 1000

    def set_search_filter(self, ovr):
        """Uses the shifted search button to update the OVR filter without going home."""
        print(f"Setting Search Filter for OVR {ovr}...")
        
        # 1. Click shifted Search button
        self.adb.click(1441, 121)
        time.sleep(2)
        
        # 2. Min OVR
        self.adb.click(782, 337)
        time.sleep(1)
        for _ in range(3):
            self.adb._run_cmd(["adb", "-s", self.adb.device_id, "shell", "input", "keyevent", "67"]) # Backspace
        self.adb.input_text(str(ovr))
        self.adb.click(948, 428) # Confirm Min OVR
        time.sleep(1)
        
        # 3. Max OVR
        self.adb.click(1048, 335)
        time.sleep(1)
        for _ in range(3):
            self.adb._run_cmd(["adb", "-s", self.adb.device_id, "shell", "input", "keyevent", "67"]) # Backspace
        self.adb.input_text(str(ovr))
        self.adb.click(1048, 398) # Confirm Max OVR
        time.sleep(1)
        
        # 4. Click Search
        self.adb.click(1060, 824)
        print("Waiting for results to load...")
        time.sleep(3)

    def run_full_scrape(self):
        """Main Loop: OVR 120 down to 110 using the Grid System."""
        print("Starting Full Scrape Task (OVR 120 -> 110)")
        
        import os
        os.makedirs("output", exist_ok=True)
        
        # The very first time, we navigate from home
        self.navigate_to_search(120, from_results=False)
        
        player_counter = 1
        
        for ovr in range(120, 109, -1):
            if ovr < 120:
                self.set_search_filter(ovr)
                
            # --- ROW 1 ---
            row1_coords = [(637, 310), (425, 417), (702, 417), (975, 415)]
            for (cx, cy) in row1_coords:
                self.process_player(ovr, player_number=player_counter, card_x=cx, card_y=cy)
                player_counter += 1
                
            # --- SCROLLING ROWS ---
            row2_coords = [(151, 501), (424, 501), (700, 501), (977, 504)]
            while True:
                scrolled = self.swipe_list_and_check()
                if not scrolled:
                    print("Reached the bottom of the list!")
                    break
                
                print("Scrolled successfully, processing new row...")
                for (cx, cy) in row2_coords:
                    self.process_player(ovr, player_number=player_counter, card_x=cx, card_y=cy)
                    player_counter += 1
            
            # --- LAST ROW (FOOTER) ---
            print("Processing the final row attached to the footer...")
            last_row_coords = [(144, 612), (431, 610), (708, 617), (987, 615)]
            for (cx, cy) in last_row_coords:
                self.process_player(ovr, player_number=player_counter, card_x=cx, card_y=cy)
                player_counter += 1

if __name__ == "__main__":
    bot = ScraperBot()
    # bot.run_full_scrape()
