import json
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
coordinates = None
warps = None
nonWarps = None
dump = None


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
    color = pyautogui.pixel(1652, 592)
    print(f' color {color} ')
    if (color[0] == 125 and color[1] == 180 and color[2] == 200):
        if not state:
            pyautogui.press('space')
    elif state:
        pyautogui.press('space')


def activateTransports():
    speach.speak('Locating transports')
    toggleShipsListWindow(True)
    y = 592
    while (y > 200):
        y = y - 1
        color = pyautogui.pixel(1690, y)
        if (color[0] == 31 and color[1] == 45 and color[2] == 48):
            print(f'Top found at y {y}')
            break

    count = 0
    while True:
        im = pyautogui.screenshot(region=(1725, y, 80, 32))
        text = pytesseract.image_to_string(im).rstrip()
        print(f'Found [{text}] at y {y}')
        if text != 'Transport':
            break
        pyautogui.click(1900, y + 16)
        count = count + 1
        y = y + 32
    #        time.sleep(0.1)

    speach.speak(f'{count} transports found')
    # step 32 px


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
