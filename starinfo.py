import json
import time

import PIL
import cv2
import numpy
import pyautogui
import pyperclip
import pytesseract
import re
import regions
import screen
import speach
from PIL import Image, ImageOps, ImageEnhance

p = re.compile(r'([\d., -]+)', re.IGNORECASE)
storedCredits = 0
storedHydro = 0
currentCredits = 0
currentHydro = 0
creditsCap = 0
hydroCap = 0
coordinates = None
warps = None
nonWarps = None
dump = None
transportsPosition = []


def loadCoordinates():
    global coordinates, warps, nonWarps, dump

    with open('coordinates.json', 'r') as openfile:
        coordinates = json.load(openfile)

    print(coordinates[0]['system'])
    planets = coordinates[0]['planets']

    warps = [p for p in planets if p.get('warp', False) and p.get('dump', False) is False]
    nonWarps = [p for p in planets if p.get('warp', False) is False and p.get('dump', False) is False]
    dumps = [p for p in planets if p.get('dump', False)]
    dump = dumps[0]

    for planet in warps:
        print(f"W {planet['name']}")

    for planet in nonWarps:
        print(f"N {planet['name']}")

    print(f"D {dump['name']}")


def printDistancesToPlanets(transportName):
    global coordinates

    selectTransportByName(transportName)


def selectTransportByName(transportName):
    speach.speak(f'Selecting {transportName}')
    pyautogui.press('5')
    time.sleep(0.3)

    while True:
        pyautogui.press('z')
        time.sleep(0.3)
        name = readTextFromRegion(regions.SHIP_NAME).upper()
        print(f'name {name}')
        if name == transportName:
            break


def routeCurrentToWarps():
    global warps
    speach.speak('Warps')
    routeCurrentTo(warps)


def routeCurrentToNonWarps():
    global nonWarps
    speach.speak('Non Warps')
    routeCurrentTo(nonWarps)


def routeCurrentTo(list):
    global dump

    pyautogui.press('F2')
    pyautogui.click(dump["x"], dump["y"])

    for planet in list:
        pyautogui.press('F2')
        pyautogui.click(planet["x"], planet["y"])


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

    currentCredits = readNumberFromRegion(regions.CURRENT_CREDITS)
    currentHydro = readNumberFromRegion(regions.CURRENT_HYDRO)

    toggleStarInfoWindow(True)
    storedCredits = readNumberFromRegion(regions.INFO_SYSTEM_CREDITS)
    storedHydro = readNumberFromRegion(regions.INFO_SYSTEM_HYDRO)
    toggleStarInfoWindow(False)

    # Hover over credits to get cap
    pyautogui.moveTo(1800, 40)
    # time.sleep(1)
    creditsCap = readNumberFromRegion(regions.CREDITS_CAP)

    # Hover over hydro to get cap
    pyautogui.moveTo(1800, 90)
    time.sleep(0.3)  # wait for credits cap overlay to fade out
    hydroCap = readNumberFromRegion(regions.HYDRO_CAP)

    pyautogui.moveTo(1500, 800)


def printData():
    print(f'creditsCap = {creditsCap}')
    print(f'currentCredits = {currentCredits}')
    print(f'storedCredits = {storedCredits}')

    print(f'hydroCap = {hydroCap}')
    print(f'currentHydro = {currentHydro}')
    print(f'storedHydro = {storedHydro}')


def readTextFromRegion(region):
    im = pyautogui.screenshot(region=region)
    im.save('src.jpg')
    text = pytesseract.image_to_string(im).strip()
    print(f'text = {text}')
    return text


def readNumberFromRegion(region):
    im = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(im)
    #    if ( region == regions.CURRENT_HYDRO ):
    #        im.save('src.jpg')
    print(f'text = {text}')
    r = p.match(text)
    if r:
        print(f'regex = {r.group(1)}')
    else:
        return 0
    return int(r.group(1).replace(' ', '').replace('.', '').replace(',', '').replace('-', ''))


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
        if (color[0] == 252 and color[1] == 93):
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


def toggleShipsListWindow(state):
    if pyautogui.pixelMatchesColor(1652, 592, (125, 180, 200), tolerance=1):
        if not state:
            pyautogui.press('space')
    elif state:
        pyautogui.press('space')


def activateTransports():
    global transportsPosition
    topY = None
    bottomY = None
    #    speach.speak('Locating transports')
    toggleShipsListWindow(True)

    im = screen.screenshot()
    y = 592
    px = im.getpixel((1690, y))
    print(px)
    while y > 1:
        y = y - 1
        if im.getpixel((1690, y)) == 214:
            topY = y
            break

    y = 592
    while y < 1080:
        y = y + 1
        if im.getpixel((1690, y)) != 232:
            bottomY = y
            break

    if topY is None or bottomY is None:
        print('Coule not find ship list!')
        exit()

    im = im.crop(box=(1724, topY, 1724 + 120, bottomY))
    im.save('cropped.jpg')
    text = screen.getText(im)
    print(f'crop [{screen.getText(im)}]')

    transportsPosition.clear()

    # quick
    count = 0
    for line in text.split():
        print(f'{count} {line}')
        if not line.startswith('TS') or ((32 * (count + 1)) + 32) >= im.height:
            break
        position = topY + (32 * count) + 16
        transport = {'name': line, 'position': position}
        transportsPosition.append(transport)
        count = count + 1

    # "Honest"
    #     count = 0
    #     while True:
    #         crop = im.crop(box=(0, 32 * count, im.width, (32 * count) + 32))
    #         crop.save('src.jpg')
    #         text = screen.getText(crop)
    #
    #         position = topY + (32 * count) + 16
    #         print(f'Found [{text}] at y {position}')
    #
    #         if not text.startswith('TS') or ((32 * (count + 1)) + 32) >= im.height:
    #             break
    #
    #         transport = {'name': text, 'position': position}
    #         transportsPosition.append(transport)
    # #        pyautogui.click(1900, position)
    #         count = count + 1

    speach.speak(f'{count} transports found')
    # step 32


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
