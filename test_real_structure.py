from data_manager import DataManager
import os
import json

# The exact real structure the user provided earlier
real_cafu_card = {
    "OVR": 120,
    "player_index": 1,
    "skills": [
        {"skill_number": 1, "name": "Wingback", "level_1_boosts": {"Ball Control": "+10"}}
    ],
    "playstyles": [
        {"playstyle_name": "Accelerator", "playstyle_description": "Fast"}
    ],
    "card_name": "CAFU",
    "shards": "68,770",
    "full_name": "TCHLIST: 0/50",
    "position": "RWB",
    "height": "176cm",
    "weight": "75kg",
    "preferred_foot": "54",
    "ovr": "120",
    "attributes": {
        "Pace": 155, "Shooting": 115, "Passing": 138, "Acceleration": 155,
        "Finishing": 102, "Short Passing": 142, "Sprint Speed": 156, "Long Shot": 118,
        "Long Passing": 140, "Shot Power": 128, "Vision": 132, "Positioning": 131,
        "Crossing": 151, "Volley": 105, "Curve": 131, "Penalties": 115,
        "Free Kick": 122, "Dribbling": 142, "Defending": 150, "Physical": 137
    }
}

# 1. Perfectly Valid Card
perfect_cafu = real_cafu_card.copy()

# 2. Corrupted Card 1: Missing Position
no_position = real_cafu_card.copy()
no_position["player_index"] = 2
no_position["position"] = ""

# 3. Corrupted Card 2: Name contains numbers
bad_name = real_cafu_card.copy()
bad_name["player_index"] = 3
bad_name["card_name"] = "CAFU123"

# 4. Corrupted Card 3: Emulator lagged, missed attributes
no_stats = real_cafu_card.copy()
no_stats["player_index"] = 4
no_stats["attributes"] = {"Pace": 155} # Only 1 stat!

# Clear output files
if os.path.exists("output/players.json"): os.remove("output/players.json")
if os.path.exists("output/failed_scrapes.json"): os.remove("output/failed_scrapes.json")

print("--- Testing Real Data Structure Validation ---")
dm = DataManager()

print("\nProcessing Player 1 (Perfect Data)...")
dm.save_player(perfect_cafu)

print("\nProcessing Player 2 (Missing Position)...")
dm.save_player(no_position)

print("\nProcessing Player 3 (Numbers in Name)...")
dm.save_player(bad_name)

print("\nProcessing Player 4 (Emulator Lag - Missing Stats)...")
dm.save_player(no_stats)

print("\n--- Summary ---")
with open("output/players.json", "r") as f:
    valid_count = len(json.load(f))
with open("output/failed_scrapes.json", "r") as f:
    failed_count = len(json.load(f))

print(f"Valid Players Saved: {valid_count} (Should be 1)")
print(f"Failed Players Blocked: {failed_count} (Should be 3)")
