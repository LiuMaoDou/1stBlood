from pathlib import Path
import os
os.chdir('/Users/**/Desktop')

for i in Path.cwd().glob("截屏*"):
    print(i)
    send2trash.send2trash(i)
