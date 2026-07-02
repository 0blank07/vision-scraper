import json
import os
from main import ScraperBot

def heal_scrapes():
    fail_file = "output/failed_scrapes.json"
    
    if not os.path.exists(fail_file):
        print(">> No failed scrapes found! Your database is 100% clean.")
        return
        
    with open(fail_file, "r", encoding='utf-8') as f:
        try:
            failed_cards = json.load(f)
        except json.JSONDecodeError:
            failed_cards = []
            
    if not failed_cards:
        print(">> No failed cards in the log. Everything is healthy!")
        return
        
    # Find all unique OVRs that experienced a failure
    failed_ovrs = sorted(list(set([int(f["OVR"]) for f in failed_cards])), reverse=True)
    
    print("\n=========================================")
    print("       AUTO-HEALER INITIATED             ")
    print("=========================================")
    print(f"Found {len(failed_cards)} rejected cards across {len(failed_ovrs)} OVR brackets: {failed_ovrs}")
    print("Since Android scrolling is not pixel-perfect, the safest and most reliable way to guarantee we fix these exact cards is to re-scrape their specific OVR brackets.\n")
    
    # Launch the bot, but pass the specific list of failed OVRs instead of the full range!
    bot = ScraperBot()
    bot.run_full_scrape(target_ovrs=failed_ovrs)
    
    print("\n>> Auto-Healing Complete! The DataManager will have removed the fixed cards from failed_scrapes.json automatically.")

if __name__ == "__main__":
    heal_scrapes()
