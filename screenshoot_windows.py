import os, sys, importlib

if importlib.util.find_spec('win32') is None:
    sys.exit(
        '\n'
        f'{os.path.basename(__file__)} requires win32api and win32gui to work.\n'
        'Please install with  "pip install pywin32 --user"'
        '\n'
    )

import threading
from win32api import GetKeyState
from win32gui import GetCursorPos
import time
import pyautogui

VERSION=(0,0,1,1)
AUTHOR='Dominik Jarocki'

#Setup
shootTimeout = 1 #minimal time in seconds between shoots
screenshotPath = "./screenshots" #path which screenshots will be saved to
#End Of Setup



#WILL NOT TOUCH UNLESS YOUR IS CRAZY AND WANNA BRAKE SCRIPT AND CREATOR'S HEART
#-----------------------------------------------------------------------------#

version = ""

processEnabled = True
processTerminationFlag = 0 
# 0-terminated 1-path not resolved
# 2-files exist in directory
# 3-region too small
# 4-cant set region to second screen
screenshotIndex = 0
screenshotNameTimestamp = True
screenRegion = (0, 0, 0, 0)
useCustomRegion = False

def y_prompt(prompt):
    ans = str(input(str(prompt) + " (Y/n) "))
    if ans.lower() == 'y'.lower() or ans.lower() == 'yes'.lower:
            return True
    return False

def checkPath(file_patch):
        try:
            if os.path.exists(file_patch) == False:
                try:
                    os.mkdir(file_patch)
                    print("Path " + file_patch + "  was created.")
                except OSError:
                    print("Could not create directory.")
            print("Screenshots will be saved to " + file_patch + ".\n")
        except:
            return


def checkForFiles(file_patch):
    global processEnabled
    if os.path.exists(file_patch + "/0.png"):
        if not screenshotNameTimestamp:
            print("\nScreenschots detected in directory. Continuing will result in overwriting existing files.")
            ans = str(input("Continue? (Y/n) "))
            if ans.lower() != 'y'.lower() and ans.lower() != 'yes'.lower:
            #if y_prompt('Continue?') == False:
                processEnabled = False


def init_screenshot():
    th = threading.Thread(target=take_screenshot)
    th.start()

def take_screenshot():
    global screenshotIndex

    timestamp = str(screenshotIndex)
    if screenshotNameTimestamp:
        timestamp = time.strftime('%d%m%y%H%M%S', time.gmtime())
    try:
        file_path = screenshotPath + "/" + timestamp + ".png"
        myScr = pyautogui.screenshot(region=screenRegion)
        if useCustomRegion:
            myScr = pyautogui.screenshot(region=screenRegion)
        else:
            myScr = pyautogui.screenshot()
        myScr.save(file_path)
        screenshotIndex += 1
        print(f'Screenshot saved to: ' + file_path)
    except:
        print("Due to some extreme exception screenshot attempt failed spectacularly!")

#Key Detection Functions
def key_down(key):
    state = GetKeyState(key)
    if (state != 0) and (state != 1):
        return True
    else:
        return False

def key_detect():
        if key_down(0x11) and key_down(0x12):
            if key_down(0x50):
                init_screenshot()
                time.sleep(shootTimeout)
            #elif key_down(0x51):
                #processEnabled = False

def prompt_region():
    if y_prompt("Capture whole screen?") == False:
        setup_region()

def setup_region():
    global screenRegion
    global useCustomRegion
    global processEnabled
    global processTerminationFlag
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    print("\nMove cursor over primary (top-left) point and press CTR+ALT+P.")
    while key_down(0x11) == False or key_down(0x12) == False or key_down(0x50) == False:
        continue
    (x1,y1) = GetCursorPos()
    print("Primary point set at (" + str(x1) + "," + str(y1) + ").")
    time.sleep(0.5)
    print("\nMove cursor over secondary (left-top) point and press CTR+ALT+P.")
    while key_down(0x11) == False or key_down(0x12) == False or key_down(0x50) == False:
        continue
    (x2,y2) = GetCursorPos()
    print("Primary point set at (" + str(x2) + "," + str(y2) + ").")
    time.sleep(0.5)

    if x2<=x1 or y2<=y1:
        print("Screen area must be larger than 0!")
        processEnabled = False
        processTerminationFlag = 3

    screenRegion = (x1,y1,x2-x1,y2-y1)
    useCustomRegion = True



def process_intro():
    print("\nWelcome to simple python screen shooter by DominJgon\n\n")
    print(f'Type "{os.path.basename(__file__)} --help" to see manual.')
    print("In order to change settings head into file section #setup.")
    #print("Before using make sure previous screenshots were saved outside of directory\n")
    print("Screen shooter currently supports only primary display.")
    time.sleep(1)

def process_ready():
    print("\nCTR+ALT+P to take screenshot, CTR+PAUSE or CTR+ALT+Q to quit.\n")

def main():
    process_intro()
    checkPath(screenshotPath)
    checkForFiles(screenshotPath)
    if processEnabled == False:
        print("\nIn order to use script please remove files or allow overwriting.\n")
        time.sleep(1)
        return
    prompt_region()
    if processEnabled == False:
        print("\nTerminating")
        time.sleep(1)
        return
    process_ready()
    while processEnabled:
        key_detect()
    print("\n\nThank you for using my script.")

def terminate():
    return

def handleArgs():
    global processEnabled
    global screenshotNameTimestamp
    if len(sys.argv) > 0:
        if '-h' in sys.argv or '--help' in sys.argv:
            print(
                '\n'
                'This is a screenshot taking script for quick shortcut use.\n'
                'Screenshot is taken by pressing Ctrl + Alt + P at any time\n' 
                'the script is running.\n'
                'By default taken screenshots are saved in ./screenshots directory.\n'
                '\n'
                f'Usage:    {os.path.basename(__file__)} [options]\n'
                '   -h, --help      -Shows this help and quits.\n'
                '   -v, --version   -Shows version of script.\n'
                '   -nt --no-time   -Disables timestamp forcing script into\n'
                '       overwrite mode. Saving screenshots will began from 0,\n'
                '       and reset every time script will be launched.\n'
            , end='\n')
            sys.exit()
        elif '-v' in sys.argv or '--version' in sys.argv:
            print(f'Version: {".".join(str(_) for _ in VERSION)}\nAuthor:  {AUTHOR}')
            sys.exit()
        elif '-nt' in sys.argv or '--no-time' in sys.argv:
            screenshotNameTimestamp = False
            return
        elif '--raise-test-error' in sys.argv:
            raise NameError('TestError')
        return
    else:
        return


try:
    handleArgs()
    main()
    terminate()
except (KeyboardInterrupt, SystemExit):
    pass