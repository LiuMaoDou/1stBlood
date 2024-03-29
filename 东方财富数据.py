import requests
import re
import json
import pandas as pd
import datetime
import pymongo
import time

mongo_client = pymongo.MongoClient('127.0.0.1', 27017)
mongo_db = mongo_client['股票']
today_iso = datetime.date.today().strftime('%Y-%m-%d')
today = datetime.datetime.fromisoformat(today_iso)
# today = datetime.datetime(year=2021, month=11, day=15, hour=0, minute=0, second=0)


def timer(function):
    """
    装饰器函数timer
    :param function:想要计时的函数
    :return:
    """

    def wrapper(*args, **kwargs):
        time_start = time.time()
        res = function(*args, **kwargs)
        cost_time = time.time() - time_start
        print("【%s】运行时间：【%s】秒" % (function.__name__, cost_time))
        return res

    return wrapper


@timer
def stock_index():
    mongo_collection = mongo_db['指数']
    pattern = re.compile(r'.*?\((.*?)\).*')
    lst = []

    data = {
        'cb': 'jQuery112405264117517608742_1636809601454',
        'pn': '1',
        'pz': '21',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fs': 'i:1.000001,i:0.399001,i:0.399005,i:0.399006,i:1.000300,i:100.HSI,i:100.HSCEI,i:124.HSCCI,i:100.TWII,'
              'i:100.N225,i:100.KOSPI200,i:100.KS11,i:100.STI,i:100.SENSEX,i:100.KLSE,i:100.SET,i:100.PSI,i:100.KSE100,'
              'i:100.VNINDEX,i:100.JKSE,i:100.CSEALL',
        'fields': 'f2,f3,f14',
        '_': '1636809601455'
    }

    result = requests.get("http://55.push2.eastmoney.com/api/qt/clist/get", params=data)

    newR = pattern.sub("\g<1>", result.text)
    newR2 = json.loads(newR)

    for i in newR2['data']['diff']:
        dic = {'名称': i['f14'], '日期': today, '最新价': i['f2'], '涨跌幅': i['f3']}
        lst.append(dic)

    mongo_collection.insert_many(lst)
    print('------Finished------')


@timer
def daily_data():
    mongo_collection = mongo_db['每日股票']

    pattern = re.compile(r'.*?\((.*?)\).*')
    lst = []

    data = {
        'cb': 'jQuery112403205794673765159_1636870325325',
        'pn': '1',
        'pz': '1',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048',
        'fields': 'f1',
        '_': '1636870325356'
    }

    result = requests.get("http://50.push2.eastmoney.com/api/qt/clist/get", params=data)

    newR = pattern.sub("\g<1>", result.text)
    newR2 = json.loads(newR)

    data = {
        'cb': 'jQuery112403205794673765159_1636870325325',
        'pn': '1',
        'pz': newR2['data']['total'],
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048',
        'fields': 'f2,f3,f6,f9,f14',
        '_': '1636870325356'
    }

    result = requests.get("http://50.push2.eastmoney.com/api/qt/clist/get", params=data)

    newR = pattern.sub("\g<1>", result.text)
    newR2 = json.loads(newR)

    for i in newR2['data']['diff']:
        if i['f6'] == "-":
            cj = 0
        else:
            cj = float(i['f6']) / 100000000

        dic = {'名称': i['f14'], '日期': today, '最新价': i['f2'], '涨跌幅': i['f3'], '成交额(亿)': cj,
               'PE': i['f9']}
        lst.append(dic)

    mongo_collection.insert_many(lst)
    print('------Finished------')


@timer
def group_data():
    mongo_collection = mongo_db['板块']

    pattern = re.compile(r'.*?\((.*?)\).*')
    lst = []

    data = {
        'cb': 'jQuery1123039820439462558643_1637012892751',
        'fid': 'f62',
        'po': '1',
        'pz': '50',
        'pn': '1',
        'np': '1',
        'fltt': '2',
        'invt': '2',
        'ut': 'b2884a393a59ad64002292a3e90d46a5',
        'fs': 'm:90 t:2',
        'fields': 'f14'
    }

    result = requests.get("http://50.push2.eastmoney.com/api/qt/clist/get", params=data)

    newR = pattern.sub("\g<1>", result.text)
    newR2 = json.loads(newR)

    data = {
        'cb': 'jQuery1123039820439462558643_1637012892751',
        'fid': 'f62',
        'po': '1',
        'pz': newR2['data']['total'],
        'pn': '1',
        'np': '1',
        'fltt': '2',
        'invt': '2',
        'ut': 'b2884a393a59ad64002292a3e90d46a5',
        'fs': 'm:90 t:2',
        'fields': 'f3,f14,f62,f204'
    }

    result = requests.get("http://push2.eastmoney.com/api/qt/clist/get", params=data)

    newR = pattern.sub("\g<1>", result.text)
    newR2 = json.loads(newR)

    for i in newR2['data']['diff']:
        cj = round((float(i['f62']) / 100000000), 2)

        dic = {'名称': i['f14'], '日期': today, '涨跌幅': i['f3'], '净额(亿)': cj, '关注股票': i['f204']}
        lst.append(dic)

    mongo_collection.insert_many(lst)
    print('------Finished------')


if __name__ == "__main__":
    stock_index()
    daily_data()
    group_data()
