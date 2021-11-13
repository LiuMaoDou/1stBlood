import tkinter as tk
from tkinter import filedialog, messagebox
from aip import AipOcr  # baidu-aip
import os
import re
import time


def input_file_path():
    window = tk.Tk()
    window.title('(^_^))')
    window.geometry('220x20')

    l = tk.Label(window, text='"Pls Select The File"')
    l.pack()

    inpath = filedialog.askopenfilename(parent=window,
                                        initialdir=os.getcwd(),
                                        title="Please select a file:",
                                        filetypes=[('all files', '.*')])

    expath = re.sub("\..*", ".txt", inpath)
    return inpath, expath


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


if __name__ == "__main__":
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    now1 = time.time()
    APP_ID = '21808493'
    API_KEY = 'xXUZ0xzi2b7LQgwoYilrulBE'
    SECRET_KEY = 'LxyP9CP6uUUGAXKq62mMRd6IAEed7hYA'

    pic, output = input_file_path()

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    with open(output, 'a+') as txt:
        image = get_file_content(pic)
        text = client.basicAccurate(image)
        result = text["words_result"]
        for i in result:
            txt.write(i["words"])
            txt.write('\n')

    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    now2 = time.time()
    now3 = now2 - now1
    messagebox.showinfo('结束', '结束，用时'+str(now3)+'s')
