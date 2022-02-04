from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Separator
import NetTrans


def task_input4():
    messagebox.showinfo('开始', '...服务器启动...')
    server = NetTrans.NetworkServer(task_txt1.get(),int(task_txt2.get()))
    server.server_start()


def task_input5():
    messagebox.showinfo('结束', '...服务器关闭...')
    root.destroy()


root = Tk()
root.title('网络通信')
root.geometry('350x200+500+300')

Label(root, text='服务器端', font="微软雅黑 20 bold", height=2, width=10).grid(row=0, columnspan=2)


Separator(root, orient=HORIZONTAL).grid(row=2, columnspan=2, sticky="ew")

task_txt1 = Entry(root, width=15, font="微软雅黑 15")
task_txt1.grid(row=3, column=1)
task1 = Label(root, text='IP地址', width=15, font="微软雅黑 15")
task1.grid(row=3, column=0)

task_txt2 = Entry(root, width=15, font="微软雅黑 15")
task_txt2.grid(row=4, column=1)
task2 = Label(root, text='端口号', width=15, font="微软雅黑 15")
task2.grid(row=4, column=0)
Separator(root, orient=HORIZONTAL).grid(row=5, columnspan=2, sticky="ew")
task4 = Button(root, text="启动", width=15, font="微软雅黑 15", command=task_input4)
task4.grid(row=6, column=0)

task5 = Button(root, text="关闭", width=15, font="微软雅黑 15", command=task_input5)
task5.grid(row=6, column=1)

root.mainloop()
