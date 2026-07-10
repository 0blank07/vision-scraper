import json
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

# Configuration
DB_HOST = os.environ.get("DB_HOST", "157.230.249.27") # Change to 'localhost' if running this script directly ON the VPS
DB_USER = os.environ.get("DB_USER", "zenith_bot")
DB_PASS = os.environ.get("DB_PASS", "zenith6Z@")
DB_NAME = os.environ.get("DB_NAME", "zenith_data")

IMAGE_BASE_URL = "https://images.zenithfcm.com"

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME
    )

def setup_database():
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("Setting up fresh 'vision_' tables on the VPS...")

    # 1. Players Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vision_players (
            player_id VARCHAR(64) PRIMARY KEY,
            card_name VARCHAR(100),
            full_name VARCHAR(255),
            ovr INTEGER,
            position VARCHAR(10),
            height VARCHAR(20),
            weight VARCHAR(20),
            preferred_foot VARCHAR(20),
            event_name VARCHAR(100),
            shards VARCHAR(50),
            stamina_stars INTEGER,
            skill_moves_stars INTEGER,
            work_rate_att VARCHAR(20),
            work_rate_def VARCHAR(20),
            portrait_url VARCHAR(255),
            nation_name VARCHAR(100),
            league_name VARCHAR(100),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. Attributes Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vision_player_attributes (
            player_id VARCHAR(64) PRIMARY KEY REFERENCES vision_players(player_id) ON DELETE CASCADE,
            stats JSONB,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 3. Skills Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vision_player_skills (
            id SERIAL PRIMARY KEY,
            player_id VARCHAR(64) REFERENCES vision_players(player_id) ON DELETE CASCADE,
            skill_number INTEGER,
            skill_name VARCHAR(100),
            level_1_requirements TEXT,
            level_1_boosts JSONB,
            level_2_requirements TEXT,
            level_2_boosts JSONB,
            level_3_requirements TEXT,
            level_3_boosts JSONB,
            image_url VARCHAR(255),
            UNIQUE(player_id, skill_number)
        );
    """)

    # 4. Playstyles Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vision_player_playstyles (
            id SERIAL PRIMARY KEY,
            player_id VARCHAR(64) REFERENCES vision_players(player_id) ON DELETE CASCADE,
            playstyle_name VARCHAR(100),
            playstyle_level VARCHAR(20),
            playstyle_description TEXT,
            image_url VARCHAR(255),
            UNIQUE(player_id, playstyle_name)
        );
    """)

    # 5. Nations Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vision_player_nations (
            player_id VARCHAR(64) PRIMARY KEY REFERENCES vision_players(player_id) ON DELETE CASCADE,
            nation_name VARCHAR(100),
            image_url VARCHAR(255)
        );
    """)

    # 6. Leagues Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vision_player_leagues (
            player_id VARCHAR(64) PRIMARY KEY REFERENCES vision_players(player_id) ON DELETE CASCADE,
            league_name VARCHAR(100),
            image_url VARCHAR(255)
        );
    """)

    # 7. Traits Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vision_player_traits (
            id SERIAL PRIMARY KEY,
            player_id VARCHAR(64) REFERENCES vision_players(player_id) ON DELETE CASCADE,
            trait_number INTEGER,
            trait_name VARCHAR(100),
            image_url VARCHAR(255),
            UNIQUE(player_id, trait_number)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tables created successfully!")

def generate_player_id(card_name, ovr, event_name):
    """Generate a consistent unique ID since we don't have an official API ID."""
    raw_str = f"{str(card_name).strip().lower()}_{str(ovr)}_{str(event_name).strip().lower()}"
    return hashlib.md5(raw_str.encode('utf-8')).hexdigest()

def sync_data():
    file_path = "output/players.json"
    if not os.path.exists(file_path):
        # Fallback for VPS execution where SCP places the file in the same directory
        file_path = "players.json"
        
    if not os.path.exists(file_path):
        print(f"Error: Neither 'output/players.json' nor 'players.json' was found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            players = json.load(f)
        except json.JSONDecodeError:
            print("Error: players.json is empty or invalid.")
            return

    conn = get_db_connection()
    cur = conn.cursor()

    print(f"Syncing {len(players)} players to database...")

    for p in players:
        # Generate a unique deterministic ID
        pid = generate_player_id(p.get("card_name"), p.get("OVR"), p.get("event_name"))
        
        # Calculate image URLs based on local scraper saving format
        ovr_val = p.get("OVR") or p.get("ovr")
        p_idx = p.get("player_index")
        
        import re
        raw_name = p.get("card_name", "unknown")
        safe_name = re.sub(r'[^a-z0-9]+', '_', str(raw_name).lower()).strip('_')
        if not safe_name: safe_name = "unknown"
        base_fname = f"ovr{ovr_val}_{safe_name}_p{p_idx}"
        
        portrait_url = f"{IMAGE_BASE_URL}/cards/{base_fname}.png"

        # 1. Upsert Player
        cur.execute("""
            INSERT INTO vision_players 
            (player_id, card_name, full_name, ovr, position, height, weight, preferred_foot, event_name, shards, stamina_stars, skill_moves_stars, work_rate_att, work_rate_def, portrait_url, nation_name, league_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (player_id) DO UPDATE SET
            full_name = EXCLUDED.full_name,
            position = EXCLUDED.position,
            height = EXCLUDED.height,
            weight = EXCLUDED.weight,
            preferred_foot = EXCLUDED.preferred_foot,
            shards = EXCLUDED.shards,
            portrait_url = EXCLUDED.portrait_url,
            nation_name = EXCLUDED.nation_name,
            league_name = EXCLUDED.league_name,
            updated_at = CURRENT_TIMESTAMP;
        """, (
            pid, p.get("card_name"), p.get("full_name"), p.get("ovr") or p.get("OVR"), p.get("position"),
            p.get("height"), p.get("weight"), p.get("preferred_foot"), p.get("event_name"), p.get("shards"),
            p.get("stamina_stars"), p.get("skill_moves_stars"), p.get("work_rate_att"), p.get("work_rate_def"),
            portrait_url, p.get("nation_name"), p.get("league_name")
        ))

        # 2. Upsert Attributes
        cur.execute("""
            INSERT INTO vision_player_attributes (player_id, stats)
            VALUES (%s, %s)
            ON CONFLICT (player_id) DO UPDATE SET
            stats = EXCLUDED.stats,
            updated_at = CURRENT_TIMESTAMP;
        """, (pid, json.dumps(p.get("attributes", {}))))

        # 3. Upsert Skills
        for idx, skill in enumerate(p.get("skills", [])):
            skill_num = skill.get("skill_number", idx + 1)
            skill_img_url = f"{IMAGE_BASE_URL}/skills/{base_fname}_s{skill_num}.png"
            
            cur.execute("""
                INSERT INTO vision_player_skills 
                (player_id, skill_number, skill_name, level_1_requirements, level_1_boosts, level_2_requirements, level_2_boosts, level_3_requirements, level_3_boosts, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (player_id, skill_number) DO UPDATE SET
                skill_name = EXCLUDED.skill_name,
                level_1_requirements = EXCLUDED.level_1_requirements,
                level_1_boosts = EXCLUDED.level_1_boosts,
                level_2_requirements = EXCLUDED.level_2_requirements,
                level_2_boosts = EXCLUDED.level_2_boosts,
                level_3_requirements = EXCLUDED.level_3_requirements,
                level_3_boosts = EXCLUDED.level_3_boosts,
                image_url = EXCLUDED.image_url;
            """, (
                pid, skill_num, skill.get("name"),
                skill.get("level_1_requirements"), json.dumps(skill.get("level_1_boosts") or {}),
                skill.get("level_2_requirements"), json.dumps(skill.get("level_2_boosts") or {}),
                skill.get("level_3_requirements"), json.dumps(skill.get("level_3_boosts") or {}),
                skill_img_url
            ))
            
        # 4. Upsert Playstyles
        for idx, ps in enumerate(p.get("playstyles", [])):
            ps_name = ps.get("playstyle_name")
            if not ps_name: continue
            
            ps_img_url = f"{IMAGE_BASE_URL}/playstyles/{base_fname}_ps{idx+1}.png"
            
            cur.execute("""
                INSERT INTO vision_player_playstyles
                (player_id, playstyle_name, playstyle_level, playstyle_description, image_url)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (player_id, playstyle_name) DO UPDATE SET
                playstyle_level = EXCLUDED.playstyle_level,
                playstyle_description = EXCLUDED.playstyle_description,
                image_url = EXCLUDED.image_url;
            """, (
                pid, ps_name, ps.get("playstyle_level"), ps.get("playstyle_description"), ps_img_url
            ))

        # 5. Upsert Nation
        nation_name = p.get("nation_name")
        if nation_name:
            nation_img_url = f"{IMAGE_BASE_URL}/img_nation/{base_fname}.png"
            cur.execute("""
                INSERT INTO vision_player_nations (player_id, nation_name, image_url)
                VALUES (%s, %s, %s)
                ON CONFLICT (player_id) DO UPDATE SET
                nation_name = EXCLUDED.nation_name,
                image_url = EXCLUDED.image_url;
            """, (pid, nation_name, nation_img_url))

        # 6. Upsert League
        league_name = p.get("league_name")
        if league_name:
            league_img_url = f"{IMAGE_BASE_URL}/img_league/{base_fname}.png"
            cur.execute("""
                INSERT INTO vision_player_leagues (player_id, league_name, image_url)
                VALUES (%s, %s, %s)
                ON CONFLICT (player_id) DO UPDATE SET
                league_name = EXCLUDED.league_name,
                image_url = EXCLUDED.image_url;
            """, (pid, league_name, league_img_url))

        # 7. Upsert Traits
        for idx, trait in enumerate(p.get("traits", [])):
            trait_num = trait.get("trait_number", idx + 1)
            trait_img_url = f"{IMAGE_BASE_URL}/traits/{base_fname}_t{trait_num}.png"
            
            cur.execute("""
                INSERT INTO vision_player_traits 
                (player_id, trait_number, trait_name, image_url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (player_id, trait_number) DO UPDATE SET
                trait_name = EXCLUDED.trait_name,
                image_url = EXCLUDED.image_url;
            """, (pid, trait_num, trait.get("name"), trait_img_url))

    conn.commit()
    cur.close()
    conn.close()
    print("Database sync completed successfully!")

if __name__ == "__main__":
    print("--- Vision Scraper DB Sync ---")
    setup_database()
    sync_data()
