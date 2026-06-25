import json
import os

class DataManager:
    def __init__(self, output_file="output/players.json"):
        self.output_file = output_file
        self.data = []
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Load existing data if any
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = []

    def save_player(self, player_dict):
        """Append a player to the list and save to JSON."""
        self.data.append(player_dict)
        self._flush()
        print(f"Saved data for player: {player_dict.get('first_name', '')} {player_dict.get('last_name', 'Unknown')}")

    def _flush(self):
        """Write the current list of dictionaries to disk."""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
