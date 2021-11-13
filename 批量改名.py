import shutil, os
from pathlib import Path
import re

filepath = "/Users/liujiannan/Downloads/rrshare/绝望的主妇第1季"
p = Path(filepath)

# 绝望的主妇.Desperate.Housewives.S01E02.Chi_Eng.HR-HDTV.AAC.1024X576.x264-YYeTs人人影视

files = p.glob('*')
pattern = re.compile('(Desperate.Housewives.S\d+E\d+)')
for i in files:
    old = i.name
    new = pattern.search(old)[1] + '.mp4'
    shutil.move(p / old, p / new)
    
print("Done")
