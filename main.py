import time
import keyboard
import pyautogui
from ultralytics import YOLO
import logging

# Инициализация модели YOLO | Initializing the YOLO model
model = YOLO("model.pt")
logging.getLogger('ultralytics').setLevel(logging.ERROR)
def scan_for_ore():
    screenshot = pyautogui.screenshot()
    results = model(screenshot)
    if len(results) > 0:
        # Получаем координаты всех обнаруженных руд | Get the coordinates of all detected ores
        ores = [(int(box[0]), int(box[1])) for box in results[0].boxes.xyxy]
        # Находим ближайшую к центру экрана руду | Find the ore closest to the center of the screen
        screen_center = (pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)
        try:
            closest_ore = min(ores, key=lambda ore: ((ore[0] - screen_center[0])**2 + (ore[1] - screen_center[1])**2)**0.5)
        except:
            # Руды закончились | The ores have ended
            print('Руды закончились!')
            closest_ore = 0
            global running
            running = False
            time.sleep(10)
        return closest_ore
    return None

#Нажатие на руды | Click on the ores
def click_ore(x, y):
    pyautogui.click(x, y)

def main():
    print("Нажмите 'Q' для остановки.")
    running = True
    while running:
        ore_pos = scan_for_ore()
        if ore_pos:
                click_ore(*ore_pos)
                time.sleep(6)
        if keyboard.is_pressed('q'):
            running = False
    
    print("Скрипт остановлен.")

if __name__ == "__main__":
    main()
