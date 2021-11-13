from tkinter import *
from tkinter import messagebox
import xlwings as xw
import ipaddress as ip
from pathlib import Path


def is_ipv4(ipadd: str):
    return True if [1] * 4 == [x.isdigit() and 0 <= int(x) <= 255 for x in ipadd.split(".")] else False


def task_input4():
    messagebox.showinfo('启动', '======开始生成，check ip-test.xlsx======')
    ip_input = task_txt1.get()
    mask_input = task_txt2.get()
    ip_max_mask_input = task_txt3.get()

    mark = True

    if not is_ipv4(ip_input):
        messagebox.showinfo('提示', '======IP地址错误======')
        mark = False

    if mask_input == "" or ip_max_mask_input == "":
        messagebox.showinfo('提示', '======网络掩码错误======')
        mark = False
    else:
        if int(mask_input) < 1 or int(ip_max_mask_input) < 1 or int(mask_input) > 32 \
                or int(ip_max_mask_input) > 32 or int(ip_max_mask_input) > int(mask_input):
            messagebox.showinfo('提示', '======网络掩码错误======')
            mark = False

    for sheet in wb.sheets:
        if ip_input in str(sheet):
            messagebox.showinfo('提示', '======IP段已经使用======')
            mark = False

    if mark:
        wb.sheets.add(ip_input)
        ws = wb.sheets(ip_input)
        ws.clear()

        n1 = ip.ip_network((ip_input, ip_max_mask_input))
        rng = ws.range("A1")
        iplist = list(n1.subnets(prefixlen_diff=(int(mask_input) - int(ip_max_mask_input))))
        ipclist = [str(n.network_address) for n in iplist] + [str(n.broadcast_address) for n in iplist]

        i = 0
        for addr in n1:
            v1 = rng.offset(row_offset=i, column_offset=0)
            v2 = rng.offset(row_offset=i, column_offset=1)
            v3 = rng.offset(row_offset=i, column_offset=2)

            v1.value = str(addr)
            v2.value = mask_input
            if str(addr) in ipclist:
                rng.offset(row_offset=i, column_offset=2).value = "不可用"
                v1.color = 0, 0, 0
                v2.color = 0, 0, 0
                v3.color = 0, 0, 0
                v1.api.Font.ColorIndex = 2
                v2.api.Font.ColorIndex = 2
                v3.api.Font.ColorIndex = 2
            i += 1

        ws.autofit()
        wb.save()
        messagebox.showinfo('完成', '---<^_^>---')


def task_input5():
    messagebox.showinfo('结束', '======今天任务结束，check ip-test.xlsx======')
    root.destroy()


file = r'C:\Users\Desktop\TEST\ip-test.xlsx'
# 不同电脑需要修改这个文件地址
file_ex = Path(file)


if file_ex.exists():
    wb = xw.Book(file)
else:
    wb = xw.Book()
    wb.save(file)

root = Tk()
root.title('IP地址生成')
root.geometry('400x150+500+300')

task_txt1 = Entry(root, width=15, font="微软雅黑")
task_txt1.grid(row=1, column=1)
task1 = Label(root, text='IP地址段', width=15, font="微软雅黑")
task1.grid(row=1, column=0)

task_txt2 = Entry(root, width=15, font="微软雅黑")
task_txt2.grid(row=2, column=1)
task2 = Label(root, text='IP掩码', width=15, font="微软雅黑")
task2.grid(row=2, column=0)

task_txt3 = Entry(root, width=15, font="微软雅黑")
task_txt3.grid(row=3, column=1)
task3 = Label(root, text='总掩码', width=15, font="微软雅黑")
task3.grid(row=3, column=0)

task4 = Button(root, text="启动", width=15, font="微软雅黑", command=task_input4)
task4.grid(row=4, column=0)

task5 = Button(root, text="关闭", width=15, font="微软雅黑", command=task_input5)
task5.grid(row=4, column=1)

root.mainloop()
