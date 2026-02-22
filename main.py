import pyautogui
import threading
import ctypes
import sys
import time
import os
import subprocess
from pynput import keyboard

# --- НАСТРОЙКИ ---
SAFE_KEY = '9' 
VIDEO_URL = "https://youtu.be/yuzFyxP_7SY?si=Dnvj4BTrrr0eGGzP"

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
running = True

def setup_pirat_style():
    try:
        # Получаем путь к картинке, которая лежит внутри EXE
        if hasattr(sys, '_MEIPASS'):
            img_path = os.path.join(sys._MEIPASS, "pirat.jpg")
        else:
            img_path = os.path.abspath("pirat.jpg")
        
        # Установка обоев (20 - SPI_SETDESKWALLPAPER)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, img_path, 3)
    except: pass

def lock_mouse():
    while running:
        pyautogui.moveTo(0, 0)
        time.sleep(0.01)

def on_press(key):
    global running
    try:
        if hasattr(key, 'char') and key.char == SAFE_KEY:
            running = False
            return False 
        if key == keyboard.Key.space:
            return 
    except: pass

if __name__ == "__main__":
    # 1. Смена обоев
    setup_pirat_style()
    
    # 2. Запуск видео через системную команду (надежнее)
    subprocess.Popen(f'start {VIDEO_URL}', shell=True)
    
    # 3. Блокировка
    threading.Thread(target=lock_mouse, daemon=True).start()

    with keyboard.Listener(on_press=on_press, suppress=True) as listener:
        listener.join()
    
    sys.exit()
