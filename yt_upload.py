import pyautogui
from time import sleep
from utils import copy2clip
# https://www.youtube.com/@6kjpcore/featured

wfu_sec = 39
n_videos = 10

copy2clip("Desktop\\all-folders\\6kjpcore\\videos")
w, h = pyautogui.size()

for idx_video in range(n_videos) :
    if idx_video == 0 :
        pyautogui.click(x=1718, y=111)
        sleep(.2)
        pyautogui.click(x=1778, y=166)
        sleep(5)
        pyautogui.click(x=934, y=691)
        sleep(3)
        pyautogui.doubleClick(x=492, y=60)
        sleep(.1)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('enter')
        sleep(.4)
    else :
        pyautogui.click(x=1748, y=122)
        sleep(0.5)
        pyautogui.click(x=1761, y=165)
        sleep(0.5)
        pyautogui.click(x=906, y=505)
        sleep(0.5)
        
    pyautogui.click(x=331, y=215)
    for right in range(idx_video): pyautogui.press('right')
    pyautogui.press('enter')
    
    sleep(wfu_sec)
    for next in range(4) : 
        pyautogui.click(x=1512, y=933)
        sleep(1)
    sleep(wfu_sec//4)
    pyautogui.click(x=1216, y=809)
    # pyautogui.click(x=1211, y=712)
    sleep(wfu_sec//4)

pyautogui.moveTo(x=100, y=100)
