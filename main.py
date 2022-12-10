# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pyautogui
import time
import pytesseract
import pyperclip
from pynput.keyboard import Key

import regions
import speach
import starinfo
from pynput import keyboard
from pathlib import Path
import json


takeCommand = False
alive = True

def startup():
    global alive
    #currentHydro = 10123456
    #currentHydro = round(currentHydro / 1000)
    #print(f'{currentHydro:,}')
    pytesseract.pytesseract.tesseract_cmd = f'{Path.home()}\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    starinfo.loadCoordinates()

    speach.speak('Hades AutoTrader online.')
    while alive:
        time.sleep(1)


def on_press(key):
    global takeCommand, alive
    try:
        key.char
        if takeCommand:
            takeCommand = False
            if key.char == 'z':
                starinfo.zoom()
            elif key.char == 'u':
                starinfo.loadStarInfo()
            elif key.char == 't':
                starinfo.activateTransports()
            elif key.char == 'w':
                starinfo.routeCurrentToWarps()
            elif key.char == 'n':
                starinfo.routeCurrentToNonWarps()
            elif key.char == 'd':
                starinfo.printDistancesToPlanets('TS7')
            elif key.char == 'q':
                speach.speak('Bye')
                alive = False
            else:
                speach.speak('Command unknown')
    except AttributeError:
        if key == Key.pause:
            takeCommand = True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startup()




