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
subCommand = None
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
    global takeCommand, subCommand, alive
    try:
        ch = key.char.lower()
        if takeCommand:
            takeCommand = False
            if subCommand is not None:
                subCommand = None
                if ch == '1':
                    print('SubAction 1')
                else:
                    print('Unknown SubAction')
            elif ch == 'z':
                starinfo.zoom()
            elif ch == 'u':
                starinfo.loadStarInfo()
            elif ch == 't':
                starinfo.activateTransports()
            elif ch == 'w':
                starinfo.routeCurrentToWarps()
            elif ch == 'n':
                starinfo.routeCurrentToNonWarps()
            elif ch == 'd':
                starinfo.printDistancesToPlanets('TS7')
            elif ch == 'e':
                takeCommand = True
                subCommand = ch
            elif ch == 'q':
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




