# Vision Scraper

An automated, computer-vision-powered scraper for extracting player data directly from the FC Mobile game UI using an Android emulator (via ADB) and OCR. This project serves as a robust, TOS-compliant alternative to direct API scraping.

## Core Architecture & Key Files

- **`main.py`**: The central orchestrator containing the `ScraperBot` class. It manages UI navigation, grid traversal, screen capturing, and dispatching OCR tasks to a background thread to prevent UI blocking. It also features a Gemini API fallback (`gemini-2.5-flash`) to handle complex OCR scenarios like playstyle descriptions.
- **`adb_controller.py`**: Manages ultra-fast communication with the Android emulator (`emulator-5554`) using a persistent ADB shell. It executes taps, swipes, text inputs, and captures direct-to-memory screenshots to minimize overhead.
- **`screen_parser.py`**: The vision engine powered by `easyocr` and OpenCV. It preprocesses images (using CLAHE for contrast), extracts text, counts stars (using HSV color filtering), and fuzzy-matches messy OCR output against a ground-truth dictionary of attributes and skills.
- **`data_manager.py`**: Responsible for formatting and saving the extracted player data into structured JSON files.
- **`dictionaries.py` / `build_dicts.py`**: Contains production dictionaries and signatures to help reverse-engineer and correct OCR errors for skill boosts and playstyles.
- **`bbox_mapper.py` / `bounding_boxes.json`**: Defines the precise pixel bounding boxes on a 1600x900 screen, allowing the parser to crop exact UI elements (names, stats, images) before feeding them to OCR.

## How the Pipeline Works

1. **Search Navigation**: The bot interacts with the game UI to set OVR filters (e.g., from 120 counting downwards).
2. **Card Traversal**: It clicks through the resulting grid of player cards, using computer vision to detect if a scroll failed or if a duplicate card was opened.
3. **Screenshot Capture**: For every card, the bot systematically opens the Side Panel, Overview, Skills, Attributes, Playstyles, and Traits tabs, taking screenshots along the way.
4. **Asynchronous Processing**: Raw images are pushed to a thread-safe task queue (`maxsize=2` to prevent memory bloat). The background worker runs local OCR and image cropping.
5. **AI Data Extraction**: If local OCR struggles with intricate popups (like playstyle names and descriptions), cropped images are sent to Gemini for accurate parsing.
6. **Persistence**: The final cleaned JSON data is saved, and visual assets (card images, skill icons, nation/league flags) are dumped into the `output/images/` directory.

## Commands & Usage

- **Run the Scraper**: 
  ```bash
  python main.py
  ```
  *(Starts the full automated scraping process)*

- **Debugging & Calibration**:
  Scripts like `debug_run.py`, `draw_all_steps.py`, and `draw_click.py` are used to test ADB clicks, visually debug bounding boxes, and verify OCR accuracy on specific game screens without running the entire pipeline.

## Important Maintenance Notes

- **Resolution Dependency**: The entire bot relies on hardcoded coordinates (`self.coords` in `main.py`) and bounding boxes tailored for a **1600x900** emulator resolution. Any changes to the emulator size or the game's UI layout will require recalibration.
- **OCR Anomalies**: `easyocr` sometimes hallucinates text or merges UI text (e.g., reading "Position Lm Position Cam" in the skill boosts menu instead of separating them). `prompt.txt` tracks these ongoing data-cleaning challenges (like removing "Unlocks after..." requirement strings from the actual stat boosts). Always check the parsing logic in `screen_parser.py` if stats look garbled.
