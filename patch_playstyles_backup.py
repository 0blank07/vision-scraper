import re
import json

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update OCR parse to use backups
old_parse = """                # Step 16-18: Playstyles
                for j, ps_dict in enumerate(images.get("playstyles", [])):
                    img_ps = ps_dict.get("base")
                    img_ps_scroll = ps_dict.get("scroll")
                    if img_ps is not None:
                        is_empty = False
                        if "playstyle_name" in self.bboxes:
                            px1, py1, px2, py2 = self.bboxes["playstyle_name"]
                            if img_ps[py1:py2, px1:px2].std() < 5.0:
                                is_empty = True
                                
                        if not is_empty:
                            ps_data = {}
                            raw_name = ""
                            raw_level = ""
                            raw_desc_1 = ""
                            raw_desc_2 = ""
                            
                            if "playstyle_name" in self.bboxes:
                                raw_name = self.parser.extract_text(img_ps, bbox=self.bboxes["playstyle_name"])
                                # Strip "Lvl X" if captured in the big box
                                raw_name = __import__('re').sub(r'(?i)lvl\s*\d+', '', raw_name).strip()
                                
                            if "playstyle_level" in self.bboxes:
                                raw_level = self.parser.extract_text(img_ps, bbox=self.bboxes["playstyle_level"])
                                
                            if "playstyle_description" in self.bboxes:
                                raw_desc_1 = self.parser.extract_text(img_ps, bbox=self.bboxes["playstyle_description"])
                                if img_ps_scroll is not None:
                                    raw_desc_2 = self.parser.extract_text(img_ps_scroll, bbox=self.bboxes["playstyle_description"])
                            
                            full_desc = raw_desc_1 + " " + raw_desc_2
                            full_desc = __import__('re').sub(r'\\s+', ' ', full_desc).strip()
                            
                            ps_data["playstyle_name"] = raw_name
                            ps_data["playstyle_level"] = "Lvl 2" if "2" in str(raw_level) else "Lvl 1"
                            ps_data["playstyle_description"] = full_desc
                            
                            if "img_playstyle" in self.bboxes:
                                filepath = f"output/images/playstyles/ovr{ovr}_p{player_number}_ps{j+1}.png"
                                self.parser.crop_and_save(img_ps, self.bboxes["img_playstyle"], filepath)
                            player_data["playstyles"].append(ps_data)"""

new_parse = """                # Step 16-18: Playstyles
                for j, ps_dict in enumerate(images.get("playstyles", [])):
                    img_ps = ps_dict.get("base")
                    img_ps_scroll = ps_dict.get("scroll")
                    if img_ps is not None:
                        is_popup_open = True
                        if "playstyle_name" in self.bboxes:
                            px1, py1, px2, py2 = self.bboxes["playstyle_name"]
                            if img_ps[py1:py2, px1:px2].std() < 5.0:
                                is_popup_open = False
                                
                        raw_name = ""
                        raw_level = ""
                        raw_desc_1 = ""
                        raw_desc_2 = ""
                        
                        if is_popup_open:
                            if "playstyle_name" in self.bboxes:
                                raw_name = self.parser.extract_text(img_ps, bbox=self.bboxes["playstyle_name"])
                                raw_name = __import__('re').sub(r'(?i)lvl\s*\d+', '', raw_name).strip()
                                
                            if "playstyle_level" in self.bboxes:
                                raw_level = self.parser.extract_text(img_ps, bbox=self.bboxes["playstyle_level"])
                                
                            if "playstyle_description" in self.bboxes:
                                raw_desc_1 = self.parser.extract_text(img_ps, bbox=self.bboxes["playstyle_description"])
                                if img_ps_scroll is not None:
                                    raw_desc_2 = self.parser.extract_text(img_ps_scroll, bbox=self.bboxes["playstyle_description"])
                        else:
                            # Popup failed to open! Use backup boxes.
                            backup_box = f"playstyle_name_{j+1}"
                            if backup_box in self.bboxes:
                                bx1, by1, bx2, by2 = self.bboxes[backup_box]
                                if img_ps[by1:by2, bx1:bx2].std() >= 5.0:
                                    raw_name = self.parser.extract_text(img_ps, bbox=self.bboxes[backup_box])
                                    raw_name = __import__('re').sub(r'(?i)lvl\s*\d+', '', raw_name).strip()
                                    raw_desc_1 = "" # No description available
                                    
                        if raw_name:
                            ps_data = {}
                            full_desc = raw_desc_1 + " " + raw_desc_2
                            full_desc = __import__('re').sub(r'\\s+', ' ', full_desc).strip()
                            
                            ps_data["playstyle_name"] = raw_name
                            ps_data["playstyle_level"] = "Lvl 2" if "2" in str(raw_level) else "Lvl 1"
                            ps_data["playstyle_description"] = full_desc
                            
                            if "img_playstyle" in self.bboxes:
                                filepath = f"output/images/playstyles/ovr{ovr}_p{player_number}_ps{j+1}.png"
                                self.parser.crop_and_save(img_ps, self.bboxes["img_playstyle"], filepath)
                            player_data["playstyles"].append(ps_data)"""
                            
content = content.replace(old_parse, new_parse)

# 2. Update Gemini parse to use backups
old_gemini = """                    # 3. Playstyle Names
                    for j, ps_dict in enumerate(images.get("playstyles", [])):
                        img_ps = ps_dict.get("base")
                        img_ps_scroll = ps_dict.get("scroll")
                        
                        if img_ps is not None and "playstyle_name" in self.bboxes:
                            is_empty = False
                            if "playstyle_name" in self.bboxes:
                                px1, py1, px2, py2 = self.bboxes["playstyle_name"]
                                if img_ps[py1:py2, px1:px2].std() < 5.0:
                                    is_empty = True
                            
                            if not is_empty:
                                x1, y1, x2, y2 = self.bboxes["playstyle_name"]
                                ps_cv = img_ps[y1:y2, x1:x2]
                                gemini_images.append(PIL.Image.fromarray(cv2.cvtColor(ps_cv, cv2.COLOR_BGR2RGB)))
                                gemini_prompt += f"Image {len(gemini_images)}: Playstyle Name {j+1} (Usually ALL CAPS. Output EXACTLY what you see, or empty string. DO NOT INCLUDE 'Lvl').\\n"
                                
                                if "playstyle_description" in self.bboxes:
                                    dx1, dy1, dx2, dy2 = self.bboxes["playstyle_description"]
                                    desc_cv_1 = img_ps[dy1:dy2, dx1:dx2]
                                    gemini_images.append(PIL.Image.fromarray(cv2.cvtColor(desc_cv_1, cv2.COLOR_BGR2RGB)))
                                    gemini_prompt += f"Image {len(gemini_images)}: Playstyle Description {j+1} Part 1.\\n"
                                    
                                    if img_ps_scroll is not None:
                                        desc_cv_2 = img_ps_scroll[dy1:dy2, dx1:dx2]
                                        gemini_images.append(PIL.Image.fromarray(cv2.cvtColor(desc_cv_2, cv2.COLOR_BGR2RGB)))
                                        gemini_prompt += f"Image {len(gemini_images)}: Playstyle Description {j+1} Part 2 (scrolled).\\n"
                            
                    if len(gemini_images) > 0:
                        gemini_prompt += "\\nOutput JSON format:\\n{\\n  \\"preferred_foot\\": \\"54\\",\\n  \\"skills\\": [\\"SCORING\\", \\"DEFENDING\\", ...],\\n  \\"playstyles\\": [ {\\"name\\": \\"FINESSE SHOT\\", \\"description\\": \\"combined description here\\"}, ... ]\\n}"
                        try:
                            print(f"  [Gemini API] Batch processing {len(gemini_images)} tricky fields for Player {player_number}...")
                            client = genai.Client()
                            response = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=[gemini_prompt] + gemini_images,
                                config=types.GenerateContentConfig(response_mime_type="application/json")
                            )
                            gemini_data = json.loads(response.text)
                            
                            # Merge back into player_data
                            if "preferred_foot" in gemini_data:
                                player_data["preferred_foot"] = gemini_data["preferred_foot"]
                                
                            for i, skill_name in enumerate(gemini_data.get("skills", [])):
                                if i < len(player_data["skills"]) and skill_name:
                                    player_data["skills"][i]["name"] = skill_name
                                    
                            for j, ps_obj in enumerate(gemini_data.get("playstyles", [])):
                                if j < len(player_data["playstyles"]) and ps_obj:
                                    name = ps_obj.get("name", "")
                                    desc = ps_obj.get("description", "")
                                    name = __import__('re').sub(r'(?i)lvl\s*\d+', '', name).strip()
                                    
                                    if name:
                                        player_data["playstyles"][j]["playstyle_name"] = name
                                    if desc:
                                        player_data["playstyles"][j]["playstyle_description"] = desc"""

new_gemini = """                    # 3. Playstyle Names
                    for j, ps_dict in enumerate(images.get("playstyles", [])):
                        img_ps = ps_dict.get("base")
                        img_ps_scroll = ps_dict.get("scroll")
                        
                        if img_ps is not None:
                            is_popup_open = True
                            if "playstyle_name" in self.bboxes:
                                px1, py1, px2, py2 = self.bboxes["playstyle_name"]
                                if img_ps[py1:py2, px1:px2].std() < 5.0:
                                    is_popup_open = False
                            
                            if is_popup_open and "playstyle_name" in self.bboxes:
                                x1, y1, x2, y2 = self.bboxes["playstyle_name"]
                                ps_cv = img_ps[y1:y2, x1:x2]
                                gemini_images.append(PIL.Image.fromarray(cv2.cvtColor(ps_cv, cv2.COLOR_BGR2RGB)))
                                gemini_prompt += f"Image {len(gemini_images)}: Playstyle Name {j+1} (Usually ALL CAPS. Output EXACTLY what you see, or empty string. DO NOT INCLUDE 'Lvl').\\n"
                                
                                if "playstyle_description" in self.bboxes:
                                    dx1, dy1, dx2, dy2 = self.bboxes["playstyle_description"]
                                    desc_cv_1 = img_ps[dy1:dy2, dx1:dx2]
                                    gemini_images.append(PIL.Image.fromarray(cv2.cvtColor(desc_cv_1, cv2.COLOR_BGR2RGB)))
                                    gemini_prompt += f"Image {len(gemini_images)}: Playstyle Description {j+1} Part 1.\\n"
                                    
                                    if img_ps_scroll is not None:
                                        desc_cv_2 = img_ps_scroll[dy1:dy2, dx1:dx2]
                                        gemini_images.append(PIL.Image.fromarray(cv2.cvtColor(desc_cv_2, cv2.COLOR_BGR2RGB)))
                                        gemini_prompt += f"Image {len(gemini_images)}: Playstyle Description {j+1} Part 2 (scrolled).\\n"
                            
                            elif not is_popup_open:
                                backup_box = f"playstyle_name_{j+1}"
                                if backup_box in self.bboxes:
                                    bx1, by1, bx2, by2 = self.bboxes[backup_box]
                                    if img_ps[by1:by2, bx1:bx2].std() >= 5.0:
                                        ps_cv = img_ps[by1:by2, bx1:bx2]
                                        gemini_images.append(PIL.Image.fromarray(cv2.cvtColor(ps_cv, cv2.COLOR_BGR2RGB)))
                                        gemini_prompt += f"Image {len(gemini_images)}: Playstyle Name {j+1} BACKUP (Usually ALL CAPS. Output EXACTLY what you see. DO NOT INCLUDE 'Lvl').\\n"
                            
                    if len(gemini_images) > 0:
                        gemini_prompt += "\\nOutput JSON format:\\n{\\n  \\"preferred_foot\\": \\"54\\",\\n  \\"skills\\": [\\"SCORING\\", \\"DEFENDING\\", ...],\\n  \\"playstyles\\": [ {\\"name\\": \\"FINESSE SHOT\\", \\"description\\": \\"combined description here\\"}, ... ]\\n}"
                        try:
                            print(f"  [Gemini API] Batch processing {len(gemini_images)} tricky fields for Player {player_number}...")
                            client = genai.Client()
                            response = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=[gemini_prompt] + gemini_images,
                                config=types.GenerateContentConfig(response_mime_type="application/json")
                            )
                            gemini_data = json.loads(response.text)
                            
                            # Merge back into player_data
                            if "preferred_foot" in gemini_data:
                                player_data["preferred_foot"] = gemini_data["preferred_foot"]
                                
                            for i, skill_name in enumerate(gemini_data.get("skills", [])):
                                if i < len(player_data["skills"]) and skill_name:
                                    player_data["skills"][i]["name"] = skill_name
                                    
                            for j, ps_obj in enumerate(gemini_data.get("playstyles", [])):
                                if j < len(player_data["playstyles"]) and ps_obj:
                                    name = ps_obj.get("name", "")
                                    desc = ps_obj.get("description", "")
                                    name = __import__('re').sub(r'(?i)lvl\s*\d+', '', name).strip()
                                    
                                    if name:
                                        player_data["playstyles"][j]["playstyle_name"] = name
                                    if desc:
                                        player_data["playstyles"][j]["playstyle_description"] = desc
                                    elif name and not desc:
                                        db_match = self.parser.reverse_engineer_playstyle(name, "")
                                        player_data["playstyles"][j]["playstyle_description"] = db_match["playstyle_description"]"""

content = content.replace(old_gemini, new_gemini)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated main.py successfully with backup boxes!")
