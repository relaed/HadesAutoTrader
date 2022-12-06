# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pyautogui
import time
import pytesseract
import pyperclip

import regions
import starinfo



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    currentHydro = 10123456
    currentHydro = round(currentHydro / 1000)
    print(f'{currentHydro:,}')


def clickityClick():
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\daini\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

    time.sleep(2)
    screenWidth, screenHeight = pyautogui.size()
    print(f'w {screenWidth}, h {screenHeight}')

    pyautogui.keyDown('-')
    pyautogui.keyDown('Down')
    pyautogui.keyDown('Right')
    time.sleep(2)
    pyautogui.keyUp('-')
    pyautogui.keyUp('Down')
    pyautogui.keyUp('Right')

    pyautogui.moveTo(680, 60)

    pyautogui.keyDown('=')
    time.sleep(1.6)
    pyautogui.keyUp('=')
    # pyautogui.moveTo(100, 150)
    # pyautogui.click()

    # starinfo.loadStarInfo()
    # starinfo.writeToStarSystem()


    # pyautogui.hotkey('ctrl', 'c')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    clickityClick()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

