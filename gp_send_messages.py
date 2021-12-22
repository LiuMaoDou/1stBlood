```python
import requests
import pandas as pd
import os
from lxml import etree
from tkinter import messagebox
from time import sleep
from datetime import datetime, time
from multiprocessing.dummy import Pool

os.chdir('/Users/**/Desktop')
token = '**'

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/95.0.4638.69 Safari/537.36"}


class AMessage(object):
    def __init__(self, codeList):
        self._df_ = df
        self._code_ = ""
        self._count_ = 0
        self.codeList = codeList

    def send_message(self, dic):
        flomo_data = {
            'content': "关注: {data[code]}_{data[name]}_{data[pct_chg]}%_{data[qrr]}".format(data=dic)
        }

        wx_data = {
            'text': '关注',
            '{desp}'.format(desp=flomo_data['content']): "提醒"
        }

        requests.post('https://flomoapp.com/iwh/MjMyNTE1/b2a4807c1ab2855b7f65c745afb248ef/', data=flomo_data)
        requests.post('http://wx.xtuis.cn/{token}.send'.format(token=token), data=wx_data)
        self._count_ = + 1
        return self._count_

    def get_tick_new(self, code):
        name = self._df_.at[code, 'name']
        url = "https://xueqiu.com/S/{}".format(code)
        text = requests.get(url=url, headers=headers)
        root = etree.HTML(text.text)
        qrrini = root.xpath('/html/body/div[1]/div[2]/div[2]/div[4]/table/tr[3]//text()')
        qrr = qrrini[qrrini.index('量比：')+1]
        if qrr == "--":
            qrr = 0
        pct_chgini = root.xpath('/html/body/div[1]/div[2]/div[2]/div[4]/div[1]/div[1]/div[2]//text()')
        pct_chg = pct_chgini[0].split(" ")[2].replace('%', "")
        print("{0:{3}>4}\t{1:>5}%\t{2:>3}".format(name, pct_chg, qrr, chr(12288)))
        merge = {"code": code, "name": name, "pct_chg": pct_chg, "qrr": qrr}

        if float(pct_chg) > 0 and float(qrr) >= 4:
        # if float(pct_chg) > 0 and float(qrr) >= 1:
            self.send_message(merge)
            self.codeList.remove(code)
            print(name, " ", "Message Sent")
        # sleep(1)

    @property
    def count_(self):
        return self._count_


if __name__ == '__main__':
    df = pd.read_csv('message_source.csv')
    df.set_index('code', inplace=True)
    codeLists = df.index.to_list()

    ted = AMessage(codeLists)
    pool = Pool(10)

    while datetime.now().time() < time(15, 0):
        if time(11, 30) < datetime.now().time() < time(12, 55):
            sleep(5400)

        pool.map(ted.get_tick_new, ted.codeList)

        if ted.count_ == 95:
            break


    # while True:
    # i = 0
    # while i < 3:
    # #     ted.get_tick()
    #     pool.map(ted.get_tick_new, codeLists)
    #     print("------------"+str(i)+"------------")
    #     i += 1


    pool.close()
    pool.join()
    messagebox.showinfo('股票', '...完成任务...')
    print("---Finished---")
    print("Cound_Left: ", (99 - ted.count_))


```
