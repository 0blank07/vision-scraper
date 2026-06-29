import json
import re

def convert_skill_tree():
    try:
        with open(r"C:\project-files\zenith-api-endpoint\src\utils\skillTree.ts", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("skillTree.ts not found")
        return
        
    # Extract the JSON part of the typescript file
    match = re.search(r"export const SKILL_TREE: Record<number, any> = (\{.*\});", content, re.DOTALL)
    if not match:
        print("Could not parse SKILL_TREE")
        return
        
    json_str = match.group(1)
    # Fix trailing commas or TS specific syntax if needed, but it looks like standard JSON format
    # Wait, TS allows unquoted keys sometimes, but the snippet shows quotes
    try:
        data = json.loads(json_str)
    except Exception as e:
        # If it fails, let's just evaluate it safely by fixing keys
        # Replace trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*\]', ']', json_str)
        data = json.loads(json_str)
        
    STAT_NAMES = {
      "acc": "Acceleration", "spd": "Sprint Speed", "fin": "Finishing", "sho": "Shot Power",
      "lsa": "Long Shot", "vol": "Volleys", "pen": "Penalties", "pos": "Positioning",
      "spa": "Short Passing", "lpa": "Long Passing", "vis": "Vision", "cro": "Crossing",
      "cur": "Curve", "frk": "Free Kick", "dri": "Dribbling", "agi": "Agility", "bal": "Balance",
      "bac": "Ball Control", "rea": "Reactions", "mrk": "Marking", "stt": "Standing Tackle",
      "slt": "Sliding Tackle", "hea": "Heading", "awr": "Awareness", "str": "Strength",
      "agg": "Aggression", "jmp": "Jumping", "sta": "Stamina",
      "gkd": "Diving", "han": "Handling", "gkk": "Kicking", "gkp": "Positioning", "ref": "Reflexes"
    }

    # Build Reverse Mapping
    # signature -> { name: "Shooting", level: 1, reqs: null }
    reverse_dict = {}
    
    for skill_id_str, skill_info in data.items():
        name = skill_info.get("name")
        boosts_map = skill_info.get("boosts", {})
        
        for level_str, boosts in boosts_map.items():
            level = int(level_str)
            # Create a signature by taking the sorted full stat names
            boosted_stats = sorted([STAT_NAMES.get(k, k.capitalize()) for k in boosts.keys()])
            sig = "|".join(boosted_stats).lower()
            
            if sig not in reverse_dict:
                reverse_dict[sig] = {
                    "name": name,
                    "boosts": boosted_stats
                }

    # Also extract Playstyles from somewhere if possible?
    # For now, just generate the skills reverse dictionary
    
    out_lines = [
        "# Auto-generated from zenith-api-endpoint data",
        f"STAT_NAMES = {json.dumps(STAT_NAMES, indent=4)}",
        f"SKILL_SIGNATURES = {json.dumps(reverse_dict, indent=4)}"
    ]
    
    with open("dictionaries.py", "w", encoding="utf-8") as f:
        f.write("\n\n".join(out_lines))
    print("dictionaries.py generated successfully!")

if __name__ == "__main__":
    convert_skill_tree()
