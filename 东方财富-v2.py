import requests
import re
import json
import pandas as pd
from time import sleep
from datetime import datetime, time


lb_cb = 'jQuery112408386016515502619_1641826224604'  # 量比cb
lb_fields = 'f10,f12,f14'
lb_url = 'https://86.push2.eastmoney.com/api/qt/clist/get'  # 量比url


def get_data(url, cb, fields):
    data = {
        'cb': cb,
        'pn': '1',
        'pz': 1,
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048',
        'fields': fields
    }

    result = requests.get(url, params=data)

    pattern = re.compile(r'.*?\((.*?)\).*')
    newR = pattern.sub("\g<1>", result.text)
    newR2 = json.loads(newR)

    dataNew = {
        'cb': cb,
        'pn': '1',
        'pz': newR2['data']['total'],
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048',
        'fields': fields
    }

    resultNew = requests.get(url, params=dataNew)
    newRNew = pattern.sub("\g<1>", resultNew.text)
    newRNew2 = json.loads(newRNew)

    return newRNew2['data']['diff']


if __name__ == "__main__":
    lb_df = get_data(lb_url, lb_cb, lb_fields)
    df = pd.DataFrame(lb_df)
    df.columns = ['量比', '代码', '名称']
    time_t = datetime.now().time().strftime('%H:%M:%S')
    df = df[['代码', '名称', '量比']]
    df.insert(0, "时间", time_t)


    # while datetime.now().time() < time(15, 0):
    #     if datetime.now().time() < time(9,30):
    #         sleep(60)
    #         continue
    #
    #     if time(11, 30) < datetime.now().time() < time(12, 55):
    #         sleep(5410)
    #
    #     time_t = datetime.now().time().strftime('%H:%M:%S')
    #     df.insert(0, "时间", time_t)
    #     sleep(60)

    print(df)
    print('------Finished------')
