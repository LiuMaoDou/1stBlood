import requests
import re
import json
import pandas as pd
import datetime
import pymongo

mongo_client = pymongo.MongoClient('127.0.0.1', 27017)
# today = datetime.date.today().strftime('%Y-%m-%d')
today = datetime.datetime.today()


def stock_index():
    mongo_db = mongo_client['股票']
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


if __name__ == "__main__":
    stock_index()
