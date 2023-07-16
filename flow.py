import subprocess
from time import sleep
# vids.py -> yt_upload.py

cmds = ['python ' + file for file in ['vids.py', 'yt_upload.py']]
for cmd in cmds :
    print(f'\n[INFO] {cmd}')
    subprocess.call(cmd, shell=True)