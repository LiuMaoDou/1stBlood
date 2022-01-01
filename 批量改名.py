import shutil, os
from pathlib import Path
import re

filepath = "/Users/**/Music/轻音乐/"
p = Path(filepath)


# files = p.glob('長笛琴人*')
files = p.glob('*《*?》*')

pattern = re.compile('.*?(《.*?》).*')
for i in files:
    old = i.name
    if "長笛琴人" not in str(i):
        print(pattern.search(old)[1])

        new = pattern.search(old)[1] + '.mp3'
        shutil.move(p / old, p / new)
    # print(pattern.search(old)[1])
    # print(old)

print("Done")
