import requests
import re
import json
import pandas as pd

pattern1 = re.compile("Summary:{mstat:\d+,pages:(\d+),page:\d+,total:\d+,hqtime:.*?},")
pattern2 = re.compile("HqData:(.*?)\};")

url = "http://q.jrjimg.cn/"
data = {
    "q": "cn|s|sa",
    "c": "s,ta,tm,sl,cot,cat,ape",
    "n": "hqa",
    "o": "cat,d",
    "p": 10100,
}

result = requests.get(url=url, params=data)

lst = []
pages = pattern1.search(result.text).group(1)
print("pages ", pages)
page = 1
while page < (int(pages) + 1):
    # while page < 2:
    data = {
        "q": "cn|s|sa",
        "c": "s,ta,tm,sl,cot,cat,ape",
        "n": "hqa",
        "o": "cat,d",
        "p": str(page) + "100",
    }
    print(page)
    result = requests.get(url=url, params=data)
    resultN = re.sub("\n", "", result.text)
    rex = pattern2.search(resultN)
    new = rex.group(1)
    newR = json.loads(new)
    # lst.append(newR)
    lst += newR
    page += 1

print(lst)

df = pd.DataFrame(lst,
                  columns=['id', 'code', 'name', 'lcp', 'stp', 'np', 'ta', 'tm', 'hlp', 'pl', 'sl', 'cat', 'cot', 'tr',
                           'ape'])
df.drop(columns=['lcp', 'stp', 'np', 'ta', 'tm', 'hlp', 'pl', 'sl', 'cot', 'tr', 'ape'], inplace=True)
df.to_excel('test.xlsx')
