import time
from typing import Tuple, Optional
import keyboard
import pyautogui
from ultralytics import YOLO
import logging
import numpy as np

# Initialize YOLO model
MODEL = YOLO("model.pt")
logging.getLogger('ultralytics').setLevel(logging.ERROR)

# Screen center calculation (done once)
SCREEN_CENTER = np.array(pyautogui.size()) // 2

# Constants
MAX_ATTEMPTS = 15
ATTEMPT_DELAY = 6

def scan_for_ore() -> Optional[Tuple[int, int]]:
    results = MODEL(np.array(pyautogui.screenshot()))
    
    if results and len(results[0].boxes):
        # Get coordinates of all detected ores (x1, y1, x2, y2)
        ores = results[0].boxes.xyxy.cpu().numpy()
        
        # Calculate centers of bounding boxes
        ore_centers = (ores[:, :2] + ores[:, 2:]) / 2
        
        # Find the ore closest to the screen center
        distances = np.linalg.norm(ore_centers - SCREEN_CENTER, axis=1)
        closest_index = np.argmin(distances)
        
        return tuple(map(int, ore_centers[closest_index]))
    
    return None

def click_ore(coords: Tuple[int, int]) -> None:
    pyautogui.click(*coords)

def main() -> None:
    print("Press 'Q' to stop the script.")
    
    consecutive_failures = 0
    
    while not keyboard.is_pressed('q'):
        ore_coords = scan_for_ore()
        
        if ore_coords:
            consecutive_failures = 0  # Reset the counter on successful detection
            click_ore(ore_coords)
            time.sleep(6)
        else:
            consecutive_failures += 1
            if consecutive_failures >= MAX_ATTEMPTS:
                print("No more ores found after multiple attempts. Stopping script.")
                break
            else:
                print(f"No ore detected. Retrying in {ATTEMPT_DELAY} seconds... (Attempt {consecutive_failures}/{MAX_ATTEMPTS})")
                time.sleep(ATTEMPT_DELAY)
    
    print("Script stopped.")

if __name__ == "__main__":
    main()
