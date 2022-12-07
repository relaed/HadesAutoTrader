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


takeCommand = False

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    #currentHydro = 10123456
    #currentHydro = round(currentHydro / 1000)
    #print(f'{currentHydro:,}')
    pytesseract.pytesseract.tesseract_cmd = f'{Path.home()}\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    speach.speak('Hades AutoTrader online.')
    while True:
        time.sleep(10)


def on_press(key):
    global takeCommand
    try:
        key.char
        if takeCommand:
            takeCommand = False
            if key.char == 'z':
                starinfo.zoom()
            elif key.char == 'u':
                starinfo.loadStarInfo()
            else:
                speach.speak('Command unknown')
    except AttributeError:
        if key == Key.pause:
            takeCommand = True


def clickityClick():
    # pytesseract.pytesseract.tesseract_cmd = '%userprofile%\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\daini\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

    time.sleep(2)
    screenWidth, screenHeight = pyautogui.size()
    print(f'w {screenWidth}, h {screenHeight}')


    # pyautogui.moveTo(100, 150)
    # pyautogui.click()

    # starinfo.loadStarInfo()
    # starinfo.writeToStarSystem()


    # pyautogui.hotkey('ctrl', 'c')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # clickityClick()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

