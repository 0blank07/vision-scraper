# Auto-generated from zenith-api-endpoint data

STAT_NAMES = {
    "acc": "Acceleration",
    "spd": "Sprint Speed",
    "fin": "Finishing",
    "sho": "Shot Power",
    "lsa": "Long Shot",
    "vol": "Volleys",
    "pen": "Penalties",
    "pos": "Positioning",
    "spa": "Short Passing",
    "lpa": "Long Passing",
    "vis": "Vision",
    "cro": "Crossing",
    "cur": "Curve",
    "frk": "Free Kick",
    "dri": "Dribbling",
    "agi": "Agility",
    "bal": "Balance",
    "bac": "Ball Control",
    "rea": "Reactions",
    "mrk": "Marking",
    "stt": "Standing Tackle",
    "slt": "Sliding Tackle",
    "hea": "Heading",
    "awr": "Awareness",
    "str": "Strength",
    "agg": "Aggression",
    "jmp": "Jumping",
    "sta": "Stamina",
    "gkd": "Diving",
    "han": "Handling",
    "gkk": "Kicking",
    "gkp": "Positioning",
    "ref": "Reflexes"
}

SKILL_SIGNATURES = {
    "finishing|long shot|shot power": {
        "name": "Shooting",
        "boosts": [
            "Finishing",
            "Long Shot",
            "Shot Power"
        ]
    },
    "long passing|short passing|vision": {
        "name": "Passing",
        "boosts": [
            "Long Passing",
            "Short Passing",
            "Vision"
        ]
    },
    "acceleration|agility|reactions": {
        "name": "Dexterity",
        "boosts": [
            "Acceleration",
            "Agility",
            "Reactions"
        ]
    },
    "finishing|heading|long shot|positioning|shot power|volleys": {
        "name": "Finisher",
        "boosts": [
            "Finishing",
            "Heading",
            "Long Shot",
            "Positioning",
            "Shot Power",
            "Volleys"
        ]
    },
    "balance|ball control|positioning|short passing|strength|vision": {
        "name": "Target Man",
        "boosts": [
            "Balance",
            "Ball Control",
            "Positioning",
            "Short Passing",
            "Strength",
            "Vision"
        ]
    },
    "agility|ball control|dribbling|positioning|shot power|sprint speed": {
        "name": "Counter",
        "boosts": [
            "Agility",
            "Ball Control",
            "Dribbling",
            "Positioning",
            "Shot Power",
            "Sprint Speed"
        ]
    },
    "finishing|long shot|strength": {
        "name": "Shooting",
        "boosts": [
            "Finishing",
            "Long Shot",
            "Strength"
        ]
    },
    "curve|finishing|heading|long shot|strength|volleys": {
        "name": "Power-Striker",
        "boosts": [
            "Curve",
            "Finishing",
            "Heading",
            "Long Shot",
            "Strength",
            "Volleys"
        ]
    },
    "awareness|marking|standing tackle": {
        "name": "Defending",
        "boosts": [
            "Awareness",
            "Marking",
            "Standing Tackle"
        ]
    },
    "balance|ball control|strength": {
        "name": "Physical",
        "boosts": [
            "Balance",
            "Ball Control",
            "Strength"
        ]
    },
    "awareness|balance|ball control|reactions|stamina|strength": {
        "name": "Ball-Winning Midfielder",
        "boosts": [
            "Awareness",
            "Balance",
            "Ball Control",
            "Reactions",
            "Stamina",
            "Strength"
        ]
    },
    "agility|ball control|dribbling|long passing|short passing|vision": {
        "name": "Playmaker",
        "boosts": [
            "Agility",
            "Ball Control",
            "Dribbling",
            "Long Passing",
            "Short Passing",
            "Vision"
        ]
    },
    "balance|ball control|reactions|short passing|stamina|vision": {
        "name": "Box-To-Box",
        "boosts": [
            "Balance",
            "Ball Control",
            "Reactions",
            "Short Passing",
            "Stamina",
            "Vision"
        ]
    },
    "balance|ball control|long shot|shot power|stamina|strength": {
        "name": "Mezzala",
        "boosts": [
            "Balance",
            "Ball Control",
            "Long Shot",
            "Shot Power",
            "Stamina",
            "Strength"
        ]
    },
    "awareness|positioning|vision": {
        "name": "Awareness",
        "boosts": [
            "Awareness",
            "Positioning",
            "Vision"
        ]
    },
    "agility|awareness|dribbling|positioning|short passing|vision": {
        "name": "Roaming Midfielder",
        "boosts": [
            "Agility",
            "Awareness",
            "Dribbling",
            "Positioning",
            "Short Passing",
            "Vision"
        ]
    },
    "crossing|long passing|short passing": {
        "name": "Passing",
        "boosts": [
            "Crossing",
            "Long Passing",
            "Short Passing"
        ]
    },
    "crossing|long passing|long shot|short passing|vision|volleys": {
        "name": "Playmaker",
        "boosts": [
            "Crossing",
            "Long Passing",
            "Long Shot",
            "Short Passing",
            "Vision",
            "Volleys"
        ]
    },
    "awareness|balance|heading|marking|standing tackle|strength": {
        "name": "No-Nonsense Centre-Back",
        "boosts": [
            "Awareness",
            "Balance",
            "Heading",
            "Marking",
            "Standing Tackle",
            "Strength"
        ]
    },
    "ball control|long passing|marking|short passing|standing tackle|vision": {
        "name": "Ball-Playing Defender",
        "boosts": [
            "Ball Control",
            "Long Passing",
            "Marking",
            "Short Passing",
            "Standing Tackle",
            "Vision"
        ]
    },
    "balance|long passing|stamina|standing tackle|strength|vision": {
        "name": "Libero",
        "boosts": [
            "Balance",
            "Long Passing",
            "Stamina",
            "Standing Tackle",
            "Strength",
            "Vision"
        ]
    },
    "balance|heading|jumping|stamina|standing tackle|strength": {
        "name": "Aerial",
        "boosts": [
            "Balance",
            "Heading",
            "Jumping",
            "Stamina",
            "Standing Tackle",
            "Strength"
        ]
    },
    "balance|shot power|strength": {
        "name": "Tackler",
        "boosts": [
            "Balance",
            "Shot Power",
            "Strength"
        ]
    },
    "aggression|balance|heading|reactions|shot power|strength": {
        "name": "Tackling Marksman",
        "boosts": [
            "Aggression",
            "Balance",
            "Heading",
            "Reactions",
            "Shot Power",
            "Strength"
        ]
    },
    "aggression|marking|standing tackle": {
        "name": "Defending",
        "boosts": [
            "Aggression",
            "Marking",
            "Standing Tackle"
        ]
    },
    "aggression|heading|long passing|marking|sliding tackle|strength": {
        "name": "No-Nonsense Centre-Back",
        "boosts": [
            "Aggression",
            "Heading",
            "Long Passing",
            "Marking",
            "Sliding Tackle",
            "Strength"
        ]
    },
    "agility|ball control|dribbling": {
        "name": "Dribbling",
        "boosts": [
            "Agility",
            "Ball Control",
            "Dribbling"
        ]
    },
    "agility|ball control|dribbling|positioning|reactions|short passing": {
        "name": "Enganche",
        "boosts": [
            "Agility",
            "Ball Control",
            "Dribbling",
            "Positioning",
            "Reactions",
            "Short Passing"
        ]
    },
    "acceleration|agility|finishing|long shot|positioning|reactions": {
        "name": "Shadow Striker",
        "boosts": [
            "Acceleration",
            "Agility",
            "Finishing",
            "Long Shot",
            "Positioning",
            "Reactions"
        ]
    },
    "acceleration|agility|long shot|positioning|reactions|shot power": {
        "name": "Longshot Taker",
        "boosts": [
            "Acceleration",
            "Agility",
            "Long Shot",
            "Positioning",
            "Reactions",
            "Shot Power"
        ]
    },
    "awareness|balance|marking|sliding tackle|standing tackle|strength": {
        "name": "Anchor",
        "boosts": [
            "Awareness",
            "Balance",
            "Marking",
            "Sliding Tackle",
            "Standing Tackle",
            "Strength"
        ]
    },
    "awareness|balance|ball control|dribbling|short passing|strength": {
        "name": "NAME_SKILL_5060",
        "boosts": [
            "Awareness",
            "Balance",
            "Ball Control",
            "Dribbling",
            "Short Passing",
            "Strength"
        ]
    },
    "acceleration|dribbling|long passing|marking|reactions|sliding tackle": {
        "name": "Intercept-Master",
        "boosts": [
            "Acceleration",
            "Dribbling",
            "Long Passing",
            "Marking",
            "Reactions",
            "Sliding Tackle"
        ]
    },
    "crossing|dribbling|standing tackle": {
        "name": "Balanced",
        "boosts": [
            "Crossing",
            "Dribbling",
            "Standing Tackle"
        ]
    },
    "awareness|ball control|crossing|dribbling|standing tackle|vision": {
        "name": "Wide Midfielder",
        "boosts": [
            "Awareness",
            "Ball Control",
            "Crossing",
            "Dribbling",
            "Standing Tackle",
            "Vision"
        ]
    },
    "crossing|dribbling|marking": {
        "name": "Balanced",
        "boosts": [
            "Crossing",
            "Dribbling",
            "Marking"
        ]
    },
    "acceleration|awareness|marking|sliding tackle|standing tackle|strength": {
        "name": "No-Nonsense Fullback",
        "boosts": [
            "Acceleration",
            "Awareness",
            "Marking",
            "Sliding Tackle",
            "Standing Tackle",
            "Strength"
        ]
    },
    "acceleration|agility|crossing|long passing|short passing|vision": {
        "name": "Attacking Fullback",
        "boosts": [
            "Acceleration",
            "Agility",
            "Crossing",
            "Long Passing",
            "Short Passing",
            "Vision"
        ]
    },
    "acceleration|awareness|crossing|dribbling|marking|standing tackle": {
        "name": "Fullback",
        "boosts": [
            "Acceleration",
            "Awareness",
            "Crossing",
            "Dribbling",
            "Marking",
            "Standing Tackle"
        ]
    },
    "acceleration|aggression|awareness|marking|sliding tackle|standing tackle": {
        "name": "Tackler",
        "boosts": [
            "Acceleration",
            "Aggression",
            "Awareness",
            "Marking",
            "Sliding Tackle",
            "Standing Tackle"
        ]
    },
    "crossing|dribbling|long passing": {
        "name": "Balanced",
        "boosts": [
            "Crossing",
            "Dribbling",
            "Long Passing"
        ]
    },
    "acceleration|crossing|long passing|short passing|sprint speed|vision": {
        "name": "Wingback",
        "boosts": [
            "Acceleration",
            "Crossing",
            "Long Passing",
            "Short Passing",
            "Sprint Speed",
            "Vision"
        ]
    },
    "acceleration|agility|ball control|dribbling|short passing|sprint speed": {
        "name": "Inverted Wingback",
        "boosts": [
            "Acceleration",
            "Agility",
            "Ball Control",
            "Dribbling",
            "Short Passing",
            "Sprint Speed"
        ]
    },
    "acceleration|agility|crossing|dribbling|long passing|sprint speed": {
        "name": "Complete Wingback",
        "boosts": [
            "Acceleration",
            "Agility",
            "Crossing",
            "Dribbling",
            "Long Passing",
            "Sprint Speed"
        ]
    },
    "acceleration|agility|finishing|heading|positioning|reactions": {
        "name": "Raumdeuter",
        "boosts": [
            "Acceleration",
            "Agility",
            "Finishing",
            "Heading",
            "Positioning",
            "Reactions"
        ]
    },
    "agility|ball control|dribbling|short passing|shot power|volleys": {
        "name": "Inverted Winger",
        "boosts": [
            "Agility",
            "Ball Control",
            "Dribbling",
            "Short Passing",
            "Shot Power",
            "Volleys"
        ]
    },
    "agility|balance|finishing|positioning|reactions|sprint speed": {
        "name": "Runner",
        "boosts": [
            "Agility",
            "Balance",
            "Finishing",
            "Positioning",
            "Reactions",
            "Sprint Speed"
        ]
    },
    "agility|dribbling|shot power": {
        "name": "Dribbling",
        "boosts": [
            "Agility",
            "Dribbling",
            "Shot Power"
        ]
    },
    "agility|balance|curve|dribbling|finishing|shot power": {
        "name": "NAME_SKILL_9440",
        "boosts": [
            "Agility",
            "Balance",
            "Curve",
            "Dribbling",
            "Finishing",
            "Shot Power"
        ]
    },
    "curve|finishing|free kick|long shot|shot power|volleys": {
        "name": "Sniper",
        "boosts": [
            "Curve",
            "Finishing",
            "Free Kick",
            "Long Shot",
            "Shot Power",
            "Volleys"
        ]
    },
    "diving|positioning|reflexes": {
        "name": "Diving",
        "boosts": [
            "Diving",
            "Positioning",
            "Reflexes"
        ]
    },
    "agility|handling|kicking": {
        "name": "GK Passing",
        "boosts": [
            "Agility",
            "Handling",
            "Kicking"
        ]
    },
    "diving|handling|jumping|positioning|reactions|reflexes": {
        "name": "Shot Stopper",
        "boosts": [
            "Diving",
            "Handling",
            "Jumping",
            "Positioning",
            "Reactions",
            "Reflexes"
        ]
    },
    "agility|handling|kicking|long passing|reactions|short passing": {
        "name": "Sweeper Keeper",
        "boosts": [
            "Agility",
            "Handling",
            "Kicking",
            "Long Passing",
            "Reactions",
            "Short Passing"
        ]
    },
    "acceleration|balance|reactions": {
        "name": "DEXTERITY",
        "boosts": [
            "Acceleration",
            "Balance",
            "Reactions"
        ]
    },
    "aggression|jumping|strength": {
        "name": "PHYSICAL",
        "boosts": [
            "Aggression",
            "Jumping",
            "Strength"
        ]
    },
    "marking|sliding tackle|standing tackle": {
        "name": "DEFENDING",
        "boosts": [
            "Marking",
            "Sliding Tackle",
            "Standing Tackle"
        ]
    },
    "heading|marking|sliding tackle|sprint speed|standing tackle|strength": {
        "name": "Defender",
        "boosts": [
            "Heading",
            "Marking",
            "Sliding Tackle",
            "Sprint Speed",
            "Standing Tackle",
            "Strength"
        ]
    },
    "acceleration|heading|jumping|marking|sliding tackle|sprint speed|standing tackle|strength": {
        "name": "Defender",
        "boosts": [
            "Acceleration",
            "Heading",
            "Jumping",
            "Marking",
            "Sliding Tackle",
            "Sprint Speed",
            "Standing Tackle",
            "Strength"
        ]
    },
    "acceleration|awareness|balance|marking|reactions|sliding tackle": {
        "name": "Stopper",
        "boosts": [
            "Acceleration",
            "Awareness",
            "Balance",
            "Marking",
            "Reactions",
            "Sliding Tackle"
        ]
    },
    "acceleration|aggression|awareness|marking|reactions|sliding tackle|sprint speed|standing tackle": {
        "name": "Stopper",
        "boosts": [
            "Acceleration",
            "Aggression",
            "Awareness",
            "Marking",
            "Reactions",
            "Sliding Tackle",
            "Sprint Speed",
            "Standing Tackle"
        ]
    },
    "acceleration|agility|awareness|dribbling|standing tackle|vision": {
        "name": "Ball-Playing Defender",
        "boosts": [
            "Acceleration",
            "Agility",
            "Awareness",
            "Dribbling",
            "Standing Tackle",
            "Vision"
        ]
    },
    "acceleration|awareness|dribbling|long passing|short passing|sprint speed|standing tackle|vision": {
        "name": "Ball-Playing Defender",
        "boosts": [
            "Acceleration",
            "Awareness",
            "Dribbling",
            "Long Passing",
            "Short Passing",
            "Sprint Speed",
            "Standing Tackle",
            "Vision"
        ]
    },
    "balance|heading|jumping": {
        "name": "Header",
        "boosts": [
            "Balance",
            "Heading",
            "Jumping"
        ]
    },
    "aggression|balance|strength": {
        "name": "Physical",
        "boosts": [
            "Aggression",
            "Balance",
            "Strength"
        ]
    },
    "awareness|sliding tackle|standing tackle": {
        "name": "Fullback",
        "boosts": [
            "Awareness",
            "Sliding Tackle",
            "Standing Tackle"
        ]
    },
    "aggression|balance|sliding tackle|sprint speed|standing tackle|strength": {
        "name": "Complete Fullback",
        "boosts": [
            "Aggression",
            "Balance",
            "Sliding Tackle",
            "Sprint Speed",
            "Standing Tackle",
            "Strength"
        ]
    },
    "acceleration|awareness|balance|crossing|sliding tackle|sprint speed|standing tackle|strength": {
        "name": "Complete Fullback",
        "boosts": [
            "Acceleration",
            "Awareness",
            "Balance",
            "Crossing",
            "Sliding Tackle",
            "Sprint Speed",
            "Standing Tackle",
            "Strength"
        ]
    },
    "acceleration|awareness|ball control|crossing|short passing|sliding tackle": {
        "name": "Wingback",
        "boosts": [
            "Acceleration",
            "Awareness",
            "Ball Control",
            "Crossing",
            "Short Passing",
            "Sliding Tackle"
        ]
    },
    "acceleration|agility|awareness|ball control|crossing|short passing|sliding tackle|sprint speed": {
        "name": "Wingback",
        "boosts": [
            "Acceleration",
            "Agility",
            "Awareness",
            "Ball Control",
            "Crossing",
            "Short Passing",
            "Sliding Tackle",
            "Sprint Speed"
        ]
    },
    "awareness|ball control|short passing|sprint speed|standing tackle|vision": {
        "name": "Falseback",
        "boosts": [
            "Awareness",
            "Ball Control",
            "Short Passing",
            "Sprint Speed",
            "Standing Tackle",
            "Vision"
        ]
    },
    "acceleration|awareness|ball control|long passing|short passing|sprint speed|standing tackle|vision": {
        "name": "NAME_SKILL_31040",
        "boosts": [
            "Acceleration",
            "Awareness",
            "Ball Control",
            "Long Passing",
            "Short Passing",
            "Sprint Speed",
            "Standing Tackle",
            "Vision"
        ]
    },
    "crossing|long passing|vision": {
        "name": "Crossing",
        "boosts": [
            "Crossing",
            "Long Passing",
            "Vision"
        ]
    },
    "awareness|ball control|standing tackle": {
        "name": "Defensive Midfielder",
        "boosts": [
            "Awareness",
            "Ball Control",
            "Standing Tackle"
        ]
    },
    "aggression|awareness|marking|sprint speed|standing tackle|strength": {
        "name": "Holding",
        "boosts": [
            "Aggression",
            "Awareness",
            "Marking",
            "Sprint Speed",
            "Standing Tackle",
            "Strength"
        ]
    },
    "acceleration|aggression|awareness|marking|short passing|sprint speed|standing tackle|strength": {
        "name": "Holding",
        "boosts": [
            "Acceleration",
            "Aggression",
            "Awareness",
            "Marking",
            "Short Passing",
            "Sprint Speed",
            "Standing Tackle",
            "Strength"
        ]
    },
    "acceleration|awareness|balance|short passing|standing tackle|strength": {
        "name": "Box-To-Box",
        "boosts": [
            "Acceleration",
            "Awareness",
            "Balance",
            "Short Passing",
            "Standing Tackle",
            "Strength"
        ]
    },
    "acceleration|awareness|balance|ball control|short passing|sprint speed|standing tackle|strength": {
        "name": "Box-To-Box",
        "boosts": [
            "Acceleration",
            "Awareness",
            "Balance",
            "Ball Control",
            "Short Passing",
            "Sprint Speed",
            "Standing Tackle",
            "Strength"
        ]
    },
    "ball control|crossing|long passing|short passing|sprint speed|vision": {
        "name": "Deep-Lying Playmaker",
        "boosts": [
            "Ball Control",
            "Crossing",
            "Long Passing",
            "Short Passing",
            "Sprint Speed",
            "Vision"
        ]
    },
    "acceleration|agility|awareness|ball control|long passing|short passing|sprint speed|vision": {
        "name": "NAME_SKILL_32040",
        "boosts": [
            "Acceleration",
            "Agility",
            "Awareness",
            "Ball Control",
            "Long Passing",
            "Short Passing",
            "Sprint Speed",
            "Vision"
        ]
    },
    "acceleration|ball control|dribbling|positioning|short passing|vision": {
        "name": "Half-Winger",
        "boosts": [
            "Acceleration",
            "Ball Control",
            "Dribbling",
            "Positioning",
            "Short Passing",
            "Vision"
        ]
    },
    "acceleration|agility|ball control|curve|dribbling|short passing|sprint speed|vision": {
        "name": "Half-Winger",
        "boosts": [
            "Acceleration",
            "Agility",
            "Ball Control",
            "Curve",
            "Dribbling",
            "Short Passing",
            "Sprint Speed",
            "Vision"
        ]
    },
    "balance|ball control|long passing|short passing|sprint speed|vision": {
        "name": "Playmaker",
        "boosts": [
            "Balance",
            "Ball Control",
            "Long Passing",
            "Short Passing",
            "Sprint Speed",
            "Vision"
        ]
    },
    "acceleration|ball control|curve|dribbling|long passing|short passing|sprint speed|vision": {
        "name": "Playmaker",
        "boosts": [
            "Acceleration",
            "Ball Control",
            "Curve",
            "Dribbling",
            "Long Passing",
            "Short Passing",
            "Sprint Speed",
            "Vision"
        ]
    },
    "crossing|dribbling|vision": {
        "name": "NAME_SKILL_34010",
        "boosts": [
            "Crossing",
            "Dribbling",
            "Vision"
        ]
    },
    "agility|ball control|crossing|long passing|short passing|sprint speed": {
        "name": "Wide Playmaker",
        "boosts": [
            "Agility",
            "Ball Control",
            "Crossing",
            "Long Passing",
            "Short Passing",
            "Sprint Speed"
        ]
    },
    "acceleration|agility|ball control|crossing|long passing|short passing|sprint speed|vision": {
        "name": "NAME_SKILL_34020",
        "boosts": [
            "Acceleration",
            "Agility",
            "Ball Control",
            "Crossing",
            "Long Passing",
            "Short Passing",
            "Sprint Speed",
            "Vision"
        ]
    },
    "aggression|balance|ball control|crossing|short passing|sprint speed": {
        "name": "Complete Wide Midfielder",
        "boosts": [
            "Aggression",
            "Balance",
            "Ball Control",
            "Crossing",
            "Short Passing",
            "Sprint Speed"
        ]
    },
    "acceleration|aggression|ball control|crossing|dribbling|short passing|sprint speed|standing tackle": {
        "name": "Complete Wide Midfielder",
        "boosts": [
            "Acceleration",
            "Aggression",
            "Ball Control",
            "Crossing",
            "Dribbling",
            "Short Passing",
            "Sprint Speed",
            "Standing Tackle"
        ]
    },
    "agility|ball control|crossing|dribbling|long passing|sprint speed": {
        "name": "Traditional Winger",
        "boosts": [
            "Agility",
            "Ball Control",
            "Crossing",
            "Dribbling",
            "Long Passing",
            "Sprint Speed"
        ]
    },
    "acceleration|agility|ball control|crossing|curve|dribbling|long passing|sprint speed": {
        "name": "Traditional Winger",
        "boosts": [
            "Acceleration",
            "Agility",
            "Ball Control",
            "Crossing",
            "Curve",
            "Dribbling",
            "Long Passing",
            "Sprint Speed"
        ]
    },
    "long shot|positioning|short passing": {
        "name": "Attacking Midfielder",
        "boosts": [
            "Long Shot",
            "Positioning",
            "Short Passing"
        ]
    },
    "acceleration|curve|finishing|positioning|reactions|shot power": {
        "name": "Shadow Striker",
        "boosts": [
            "Acceleration",
            "Curve",
            "Finishing",
            "Positioning",
            "Reactions",
            "Shot Power"
        ]
    },
    "acceleration|ball control|curve|finishing|positioning|reactions|shot power|sprint speed": {
        "name": "Shadow Striker",
        "boosts": [
            "Acceleration",
            "Ball Control",
            "Curve",
            "Finishing",
            "Positioning",
            "Reactions",
            "Shot Power",
            "Sprint Speed"
        ]
    },
    "curve|long shot|shot power": {
        "name": "Long Shot",
        "boosts": [
            "Curve",
            "Long Shot",
            "Shot Power"
        ]
    },
    "acceleration|crossing|positioning": {
        "name": "Winger",
        "boosts": [
            "Acceleration",
            "Crossing",
            "Positioning"
        ]
    },
    "agility|ball control|curve|dribbling|finishing|sprint speed": {
        "name": "Inside Forward",
        "boosts": [
            "Agility",
            "Ball Control",
            "Curve",
            "Dribbling",
            "Finishing",
            "Sprint Speed"
        ]
    },
    "acceleration|agility|ball control|curve|dribbling|finishing|shot power|sprint speed": {
        "name": "Inside Forward",
        "boosts": [
            "Acceleration",
            "Agility",
            "Ball Control",
            "Curve",
            "Dribbling",
            "Finishing",
            "Shot Power",
            "Sprint Speed"
        ]
    },
    "finishing|shot power|volleys": {
        "name": "Striker",
        "boosts": [
            "Finishing",
            "Shot Power",
            "Volleys"
        ]
    },
    "finishing|positioning|reactions|shot power|sprint speed|volleys": {
        "name": "Advance Forward",
        "boosts": [
            "Finishing",
            "Positioning",
            "Reactions",
            "Shot Power",
            "Sprint Speed",
            "Volleys"
        ]
    },
    "acceleration|dribbling|finishing|positioning|shot power|sprint speed|strength|volleys": {
        "name": "Advance Forward",
        "boosts": [
            "Acceleration",
            "Dribbling",
            "Finishing",
            "Positioning",
            "Shot Power",
            "Sprint Speed",
            "Strength",
            "Volleys"
        ]
    },
    "acceleration|agility|finishing|positioning|reactions|volleys": {
        "name": "Poacher",
        "boosts": [
            "Acceleration",
            "Agility",
            "Finishing",
            "Positioning",
            "Reactions",
            "Volleys"
        ]
    },
    "acceleration|agility|finishing|heading|positioning|reactions|sprint speed|volleys": {
        "name": "Poacher",
        "boosts": [
            "Acceleration",
            "Agility",
            "Finishing",
            "Heading",
            "Positioning",
            "Reactions",
            "Sprint Speed",
            "Volleys"
        ]
    },
    "balance|ball control|heading|short passing|sprint speed|strength": {
        "name": "Target Forward",
        "boosts": [
            "Balance",
            "Ball Control",
            "Heading",
            "Short Passing",
            "Sprint Speed",
            "Strength"
        ]
    },
    "acceleration|ball control|finishing|heading|jumping|short passing|sprint speed|strength": {
        "name": "NAME_SKILL_37040",
        "boosts": [
            "Acceleration",
            "Ball Control",
            "Finishing",
            "Heading",
            "Jumping",
            "Short Passing",
            "Sprint Speed",
            "Strength"
        ]
    },
    "acceleration|agility|ball control|dribbling|positioning|short passing": {
        "name": "False 9",
        "boosts": [
            "Acceleration",
            "Agility",
            "Ball Control",
            "Dribbling",
            "Positioning",
            "Short Passing"
        ]
    },
    "acceleration|agility|ball control|dribbling|finishing|short passing|sprint speed|vision": {
        "name": "False 9",
        "boosts": [
            "Acceleration",
            "Agility",
            "Ball Control",
            "Dribbling",
            "Finishing",
            "Short Passing",
            "Sprint Speed",
            "Vision"
        ]
    },
    "diving|jumping|reactions": {
        "name": "Goal Keeper",
        "boosts": [
            "Diving",
            "Jumping",
            "Reactions"
        ]
    },
    "diving|handling|positioning|reactions|reflexes|strength": {
        "name": "Shot Stopper",
        "boosts": [
            "Diving",
            "Handling",
            "Positioning",
            "Reactions",
            "Reflexes",
            "Strength"
        ]
    },
    "agility|kicking|long passing|reactions|reflexes|short passing": {
        "name": "Sweeper Keeper",
        "boosts": [
            "Agility",
            "Kicking",
            "Long Passing",
            "Reactions",
            "Reflexes",
            "Short Passing"
        ]
    },
    "agility|diving|kicking|long passing|reflexes|short passing": {
        "name": "NAME_SKILL_38030",
        "boosts": [
            "Agility",
            "Diving",
            "Kicking",
            "Long Passing",
            "Reflexes",
            "Short Passing"
        ]
    },
    "kicking|long passing|vision": {
        "name": "NAME_SKILL_38040",
        "boosts": [
            "Kicking",
            "Long Passing",
            "Vision"
        ]
    },
    "acceleration|handling|positioning": {
        "name": "GK Rush",
        "boosts": [
            "Acceleration",
            "Handling",
            "Positioning"
        ]
    },
    "handling|jumping|positioning": {
        "name": "Highballs",
        "boosts": [
            "Handling",
            "Jumping",
            "Positioning"
        ]
    },
    "finishing|heading|long shot|shot power": {
        "name": "SCORING",
        "boosts": [
            "Finishing",
            "Heading",
            "Long Shot",
            "Shot Power"
        ]
    },
    "crossing|long passing|short passing|vision": {
        "name": "PASSING",
        "boosts": [
            "Crossing",
            "Long Passing",
            "Short Passing",
            "Vision"
        ]
    },
    "agility|ball control|dribbling|reactions": {
        "name": "DRIBBLING",
        "boosts": [
            "Agility",
            "Ball Control",
            "Dribbling",
            "Reactions"
        ]
    },
    "awareness|marking|sliding tackle|standing tackle": {
        "name": "DEFENDING",
        "boosts": [
            "Awareness",
            "Marking",
            "Sliding Tackle",
            "Standing Tackle"
        ]
    },
    "aggression|balance|jumping|strength": {
        "name": "PHYSICAL",
        "boosts": [
            "Aggression",
            "Balance",
            "Jumping",
            "Strength"
        ]
    },
    "ball control|dribbling|short passing": {
        "name": "GK BALL-PLAYING",
        "boosts": [
            "Ball Control",
            "Dribbling",
            "Short Passing"
        ]
    },
    "acceleration|sliding tackle|sprint speed": {
        "name": "GK RUSH",
        "boosts": [
            "Acceleration",
            "Sliding Tackle",
            "Sprint Speed"
        ]
    }
}
PLAYSTYLES = {
    "FINESSE EXPERT": "Player can curl finesse shots past the keeper with great accuracy.  Read more",
    "PLAY MAKER": "trait_desc_18",
    "BRUISER": "Player has greater strength during physical battles, both at protecting the ball while dribbling or contesting the opponent during a jostle.  Read more",
    "RELENTLESS": "Player has great stamina and is able to make many runs without getting tired easily.  Read more",
    "GUARDIAN": "Player has a higher hard tackle proficiency and success rate.  Read more",
    "PENALTY EXPERT": "Player has exceptional accuracy at penalty kicks.  Read more",
    "RAPID": "Player has a more explosive acceleration for sprint dribble and knock-ons.  Read more",
    "ANTICIPATE": "Player has a higher stand tackle proficiency and success rate.  Read more",
    "ACCELERATOR": "Player is able to have a quick burst of speed when  accelerating without the ball .  Read more",
    "POWER SHOT": "Player can take powerful shots with high precision\nLvl 1: Increases accuracy and shot speed for power shots.  Read more",
    "WHIPPED CROSS": "Player can perform high-speed whipped crosses into the box.  Read more",
    "DEFLECTOR": "Goalkeeper has the ability to deflect the ball far, wide and into safer areas.  Read more",
    "CHIP SHOT": "Player has exceptional skill at chipping the goalkeeper.  Read more",
    "CLINICAL FINISHER": "Player can accurately place the ball in the net from close to mid-range shooting distance.  Read more",
    "PRECISION HEADER": "Player has exceptional performance when heading the ball.  Read more",
    "BULLET PASS": "Player is able to perform more accurate and faster driven ground passes.  Read more",
    "TIKI TAKA": "Player is able to perform more accurate and faster  ground passes.  Read more",
    "RUSH OUT": "Goalkeeper has the ability to quickly rush out of goal to pressure the opponent.  Read more",
    "TRICKSTER": "Player can more effectively perform skill moves and beat defenders in 1v1 situations.  Read more",
    "NONE": None,
    "FINESSE SHOT": "trait_desc_16",
    "GK LONG THROWER": "trait_desc_21"
}
