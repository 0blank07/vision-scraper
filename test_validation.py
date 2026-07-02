from data_manager import DataManager
import os

# Create dummy data
valid_player = {
    "OVR": 120,
    "player_index": 1,
    "card_name": "MESSI",
    "position": "RW",
    "skills": [{"name": "SCORING"}],
    "attributes": {
        "Pace": 99, "Shooting": 99, "Passing": 99, "Dribbling": 99, "Defending": 99, 
        "Physical": 99, "Acceleration": 99, "Sprint Speed": 99, "Positioning": 99, 
        "Finishing": 99, "Shot Power": 99, "Long Shot": 99, "Volley": 99, "Penalties": 99, 
        "Vision": 99
    }
}

bad_name_player = valid_player.copy()
bad_name_player["card_name"] = "MESSI123"
bad_name_player["player_index"] = 2

bad_stats_player = valid_player.copy()
bad_stats_player["card_name"] = "RONALDO"
bad_stats_player["attributes"] = {"Pace": 99, "Shooting": 99} # Only 2 stats
bad_stats_player["player_index"] = 3

# Delete old outputs to ensure a clean test
if os.path.exists("output/players.json"): os.remove("output/players.json")
if os.path.exists("output/failed_scrapes.json"): os.remove("output/failed_scrapes.json")

print("--- Testing Validation System ---")
dm = DataManager()
dm.save_player(valid_player)
dm.save_player(bad_name_player)
dm.save_player(bad_stats_player)

print("\n--- Results ---")
print("Valid players saved:", len(dm.data))
print("Failed players logged:", len(dm.failed_data))
