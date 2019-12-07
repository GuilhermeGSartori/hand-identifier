import pyautogui

# pretty basic interaction
# PRE-CONDITIONS:
    # Youtube opened on the video
    # Video window actived as the current window

def fist():
    print("play")
    pyautogui.press('space')

def bup():
    print("volume up")
    pyautogui.press('up')

def sup():
    print("volume down")
    pyautogui.press('down')
