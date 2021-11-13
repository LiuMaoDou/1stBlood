import pyperclip
import time
import re
patter = re.compile(r'\s')
space = re.compile(r'( )+')

while True:
    text = pyperclip.paste()

    while True:
        time.sleep(1)
        cur_text = pyperclip.paste()

        if cur_text != text:
            pyperclip.copy(space.sub(" ", patter.sub(" ", cur_text)))
            break

