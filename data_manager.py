import json
import os

class DataManager:
    def __init__(self, output_file="output/players.json", fail_file="output/failed_scrapes.json"):
        self.output_file = output_file
        self.fail_file = fail_file
        self.data = []
        self.failed_data = []
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Load existing data if any
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = []
                    
        if os.path.exists(self.fail_file):
            with open(self.fail_file, 'r', encoding='utf-8') as f:
                try:
                    self.failed_data = json.load(f)
                except json.JSONDecodeError:
                    self.failed_data = []

    def validate_player(self, p):
        """Strictly validates the player data. Returns (True, "") or (False, reason)"""
        # 1. Check Name
        name = p.get('card_name') or p.get('full_name', '')
        if not name or str(name).strip() == "" or name == "Unknown" or any(char.isdigit() for char in str(name)):
            return False, "Missing or corrupted name."
            
        # 2. Check Position
        if not p.get('position') or str(p.get('position')).strip() == "":
            return False, "Missing position."
            
        # 3. Check Attributes (Needs at least 15 stats to be considered a successful read)
        attrs = p.get('attributes', {})
        if len(attrs) < 15:
            return False, f"Missing attributes. Found {len(attrs)}, expected at least 15."
            
        # 4. Check Skills
        skills = p.get('skills', [])
        if len(skills) == 0:
            return False, "Missing skills completely."
            
        return True, "Valid"

    def save_player(self, player_dict):
        """Validates the player. If valid, append to players.json, else append to failed_scrapes.json."""
        is_valid, reason = self.validate_player(player_dict)
        
        if is_valid:
            # Check if this player was previously in the failed list and remove it (Auto-Heal success)
            self.failed_data = [f for f in self.failed_data if not (f.get("OVR") == player_dict.get("OVR") and f.get("player_index") == player_dict.get("player_index"))]
            
            self.data.append(player_dict)
            self._flush_valid()
            self._flush_failed()
            print(f"  [DataManager] [PASS] Saved {player_dict.get('card_name', 'Unknown')} (OVR {player_dict.get('OVR')})")
        else:
            # Save minimal info to fail log so the auto-healer knows exactly where to look
            fail_record = {
                "OVR": player_dict.get("OVR"),
                "player_index": player_dict.get("player_index"),
                "attempted_name": player_dict.get('card_name', 'Unknown'),
                "fail_reason": reason
            }
            self.failed_data.append(fail_record)
            self._flush_failed()
            print(f"  [DataManager] [FAIL] Player {player_dict.get('player_index')} (OVR {player_dict.get('OVR')}) REJECTED: {reason}")

    def _flush_valid(self):
        """Write the valid players to disk."""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
            
    def _flush_failed(self):
        """Write the failed players to disk."""
        with open(self.fail_file, 'w', encoding='utf-8') as f:
            json.dump(self.failed_data, f, indent=4)
