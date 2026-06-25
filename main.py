import time
import cv2
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
            # Crop card image (approximate bounding box for the card artwork in the side panel)
            # Assuming side panel is on the right, card is usually upper right.
            card_crop = img_panel[100:550, 1200:1500]
            cv2.imwrite(f"output/ovr{ovr}_p{player_number}_card.png", card_crop)
            # Full panel OCR for Shards
            player_data["shards_text"] = self.parser.extract_text(img_panel, (1200, 50, 1550, 800))
        
        # Step 9: Click Player Card in Panel
        print("Step 9: Opening Full Profile...")
        self.adb.click(*self.coords["panel_card"])
        time.sleep(4)
        
        # Step 10: Overview Tab
        print("Step 10: Extracting Overview Data...")
        img_overview = self.adb.get_screenshot()
        if img_overview is not None:
            cv2.imwrite(f"output/ovr{ovr}_p{player_number}_overview.png", img_overview)
            player_data["overview_raw_text"] = self.parser.extract_text(img_overview)
        
        # Step 11, 12, 13, 14: Skills
        print("Step 11-14: Processing Skills...")
        for i, skill_coord in enumerate(self.coords["skills"]):
            self.adb.click(*skill_coord)
            time.sleep(2)
            
            skill_data = {"skill_number": i+1}
            
            # 1. Record Level 1 (Default)
            print(f"  > Skill {i+1}: Recording Level 1...")
            img_skill1 = self.adb.get_screenshot()
            if img_skill1 is not None:
                skill_data["level_1_text"] = self.parser.extract_text(img_skill1)
            
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
                print(f"  > Skill {i+1}: Recording Level 2...")
                img_skill2 = self.adb.get_screenshot()
                if img_skill2 is not None:
                    skill_data["level_2_text"] = self.parser.extract_text(img_skill2)
                
            # 4. Process Level 3
            if max_level == 3:
                self.adb.click(952, 270)
                time.sleep(1.5)
                self.adb.click(940, 474)
                time.sleep(1.5)
                print(f"  > Skill {i+1}: Recording Level 3...")
                img_skill3 = self.adb.get_screenshot()
                if img_skill3 is not None:
                    skill_data["level_3_text"] = self.parser.extract_text(img_skill3)
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
        if img_attr is not None:
            cv2.imwrite(f"output/ovr{ovr}_p{player_number}_attributes.png", img_attr)
            player_data["attributes_raw_text"] = self.parser.extract_text(img_attr)
        
        # Step 16: Playstyles Tab
        print("Step 16-18: Extracting Playstyles...")
        self.adb.click(*self.coords["tab_playstyles"])
        time.sleep(2)
        
        # Step 17: Playstyle 1
        self.adb.click(*self.coords["playstyle_i_1"])
        time.sleep(1.5)
        img_ps1 = self.adb.get_screenshot()
        if img_ps1 is not None:
            player_data["playstyles"].append(self.parser.extract_text(img_ps1))
        self.adb.click(*self.coords["playstyle_close"])
        time.sleep(1)
        
        # Step 18: Playstyle 2
        self.adb.click(*self.coords["playstyle_i_2"])
        time.sleep(1.5)
        img_ps2 = self.adb.get_screenshot()
        if img_ps2 is not None:
            player_data["playstyles"].append(self.parser.extract_text(img_ps2))
        self.adb.click(*self.coords["playstyle_close"])
        time.sleep(1)

        # Step 19: Traits Tab
        print("Step 19: Extracting Traits...")
        self.adb.click(*self.coords["tab_traits"])
        time.sleep(2)
        img_traits = self.adb.get_screenshot()
        if img_traits is not None:
            cv2.imwrite(f"output/ovr{ovr}_p{player_number}_traits.png", img_traits)
            player_data["traits_raw_text"] = self.parser.extract_text(img_traits)

        # Save data
        self.data_mgr.save_player(player_data)

        # Step 20: Go Back to Results
        print("Step 20: Going back to Results...")
        self.adb.click(*self.coords["go_back"])
        time.sleep(3)

    def run_full_scrape(self):
        """Main Loop: OVR 120 down to 110."""
        print("Starting Full Scrape Task (OVR 120 -> 110)")
        
        import os
        os.makedirs("output", exist_ok=True)
        
        self.navigate_to_search(120, from_results=False)
        
        for ovr in range(120, 109, -1):
            if ovr < 120:
                self.navigate_to_search(ovr, from_results=True)
                
            self.process_player(ovr, player_number=1, card_x=self.coords["card_1"][0], card_y=self.coords["card_1"][1])

if __name__ == "__main__":
    bot = ScraperBot()
    # bot.run_full_scrape()
