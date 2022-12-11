import pyautogui
import pytesseract
from PIL import ImageOps


def screenshot():
    # grab whole screen - quicker to get once and crop it later
    im = pyautogui.screenshot()

    # convert to grayscale
    im = im.convert('L')

    # invert, tessaract works better with black text on white background
    inverted = ImageOps.invert(im)
    inverted.save('srcShot.jpg')
    return inverted


def getText(image):
    # Usually image is too small for tessaract to distinguish some letters/numbers, resizing helps
    image = image.resize((int(image.size[0] * 2), int(image.size[1] * 2)))
    return pytesseract.image_to_string(image, config='--psm 6').strip()
