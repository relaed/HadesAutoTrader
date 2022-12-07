import time
import pyautogui
import pyperclip
import pytesseract
import re
import regions
import speach

p = re.compile(r'([\d., -]+)', re.IGNORECASE)
storedCredits = 0
storedHydro = 0
currentCredits = 0
currentHydro = 0
creditsCap = 0
hydroCap = 0

def loadStarInfo():
    speach.speak('Collecting star info')
    toggleChatWindow(False)

    collectData()
    printData()
    writeToStarSystem()

def writeToStarSystem():
    toggleChatWindow(True)
    time.sleep(0.2)
    pyautogui.click(10, 260)
    time.sleep(0.2)
    cc = round(currentCredits / 1000)
    ch = round(currentHydro / 1000)
    sc = round(storedCredits / 1000)
    text = f'Before trade {cc:,}kC/{ch:,}kH with {sc:,}kC in shipments'
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
#    pyautogui.press('return')

def collectData():
    global storedCredits, currentCredits, storedHydro, currentHydro, creditsCap, hydroCap

    currentCredits = grabTextFromRegion(regions.CURRENT_CREDITS)
    currentHydro = grabTextFromRegion(regions.CURRENT_HYDRO)

    toggleStarInfoWindow(True)
    storedCredits = grabTextFromRegion(regions.INFO_SYSTEM_CREDITS)
    storedHydro = grabTextFromRegion(regions.INFO_SYSTEM_HYDRO)
    toggleStarInfoWindow(False)

    # Hover over credits to get cap
    pyautogui.moveTo(1800, 40)
    # time.sleep(1)
    creditsCap = grabTextFromRegion(regions.CREDITS_CAP)

    # Hover over hydro to get cap
    pyautogui.moveTo(1800, 90)
    # time.sleep(1)
    hydroCap = grabTextFromRegion(regions.HYDRO_CAP)

    pyautogui.moveTo(1500, 800)

def printData():
    print(f'creditsCap = {creditsCap}')
    print(f'currentCredits = {currentCredits}')
    print(f'storedCredits = {storedCredits}')

    print(f'hydroCap = {hydroCap}')
    print(f'currentHydro = {currentHydro}')
    print(f'storedHydro = {storedHydro}')


def grabTextFromRegion(region):
    im = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(im)
    im.save('src.jpg')
    print(f'text = {text}')
    r = p.match(text)
    if r:
        print(f'regex = {r.group(1)}')
    else:
        return 0
    return int(r.group(1).replace(' ', '').replace('.', '').replace(',', '').replace('-',''))


def toggleChatWindow(state):
    color = pyautogui.pixel(10, 310)
    print(f' color {color} ')
    if (color[0] == 31 and color[2] == 48):
        if not state:
            pyautogui.press('tab')
    elif state:
        pyautogui.press('tab')


def toggleStarInfoWindow(state):
    # Check if Information window is open - press I to open it if not.
    color = pyautogui.pixel(150, 400)
    # print(f' color {color} ')
    if state:
        if ( color[0] == 252 and color[1] == 93 ):
            # window is already open - we need to close it and open again to refresh data
            print('Refreshing star info')
            pyautogui.press('i')
            time.sleep(0.5)
            pyautogui.press('i')
        else:
            # it is not open, just press i to open it up
            print('Opening star info')
            pyautogui.press('i')
    else:
        if (color[0] == 252 and color[1] == 93):
            # Simply close
            pyautogui.press('i')



def zoom():
    speach.speak('Positioning the star')
    pyautogui.keyDown('-')
    pyautogui.keyDown('Down')
    pyautogui.keyDown('Right')
    time.sleep(3)
    pyautogui.keyUp('-')
    pyautogui.keyUp('Down')
    pyautogui.keyUp('Right')

    pyautogui.moveTo(680, 60)

    pyautogui.keyDown('=')
    time.sleep(1.6)
    pyautogui.keyUp('=')