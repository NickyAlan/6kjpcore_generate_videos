import pyautogui
from time import sleep

wfu_sec = 15
n_videos = 10

w, h = pyautogui.size()
for idx_video in range(n_videos) :
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
    sleep(wfu_sec//2)
    pyautogui.click(x=1228, y=802)
    sleep(wfu_sec//2)