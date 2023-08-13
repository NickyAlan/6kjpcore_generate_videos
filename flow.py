import os 
import subprocess
from time import sleep
# vids.py -> yt_upload.py

DIR = './videos'
cmds = ['python ' + file for file in ['vids.py', 'yt_upload.py']]
for cmd in cmds :
    print(f'\n[INFO] {cmd}')
    subprocess.call(cmd, shell=True)
    sleep(2)

need_rmv = input("Remove all videos? (y/n): ").lower()
if need_rmv == 'y' :
    file_paths = [os.path.join(DIR, file_name) for file_name in os.listdir(DIR)]
    for path in file_paths : os.remove(path)
    print("[COMPLETE] remove all files.")