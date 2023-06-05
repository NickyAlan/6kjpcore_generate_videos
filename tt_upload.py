import pyautogui
from time import sleep
from utils import copy2clip

# wait for upload seconds
wfu_sec = 15
n_videos = 10
tag = ' #japanese #6kcore #vocabulary #6kjpcore'
copy2clip(tag)

print(f'[{n_videos}] Uploading')
w, h = pyautogui.size()
for idx_video in range(n_videos) :
    pyautogui.scroll(h)
    pyautogui.click(x=499, y=579)
    sleep(0.7)
    pyautogui.click(x=330, y=258)
    # select clip
    for right in range(idx_video): pyautogui.press('right')
    sleep(0.5)
    pyautogui.press('enter')
    # wait for uploading
    sleep(wfu_sec)
    pyautogui.scroll(h)
    sleep(0.5)
    pyautogui.click(x=934, y=535)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.scroll(-h)
    sleep(0.5)
    pyautogui.click(x=1031, y=310)
    # wait for uploading
    sleep(wfu_sec + 5)
    pyautogui.scroll(h)
    sleep(0.5)
    # if last video not click for next upload
    pyautogui.click(x=1039, y=870) if (idx_video + 1) != n_videos else pyautogui.click(x=998, y=981)
    sleep(3)

    print(f'[{idx_video + 1}/{n_videos}] | uploaded')