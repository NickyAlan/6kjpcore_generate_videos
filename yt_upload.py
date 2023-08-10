import os
import pyautogui
import webbrowser
from time import sleep
from utils import copy2clip
# https://www.youtube.com/@6kjpcore/featured

wfu_sec =5
n_videos = len(os.listdir('videos'))

copy2clip("Desktop\\all-folders\\6kjpcore\\videos")
w, h = pyautogui.size()
webbrowser.open('https://www.youtube.com/@6kjpcore/featured', 1)
sleep(7)

for idx_video in range(n_videos) :
    if idx_video == 0 :
        pyautogui.click(x=1718, y=111)
        sleep(.2)
        pyautogui.click(x=1778, y=166)
        sleep(6)
        pyautogui.click(x=934, y=691)
        sleep(4)
        pyautogui.doubleClick(x=592, y=60)
        sleep(4)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('enter')
        sleep(2)
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
    for next in range(9) : 
        pyautogui.click(x=1470, y=933)
        sleep(1)
    sleep(wfu_sec//4)
    pyautogui.click(x=1216, y=809)
    sleep(wfu_sec//4)
    pyautogui.click(x=1211, y=712)
    sleep(wfu_sec//6)
    pyautogui.click(x=1211, y=732)
    sleep(wfu_sec//4)

pyautogui.moveTo(x=100, y=100)

