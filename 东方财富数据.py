import requests
import re
import json
pattern = re.compile(r'.*?\((.*?)\).*')

data = {
    "cb": "jQuery112403313427088495968_1636183342280",
    "pn": "1",
    "pz": "50",
    "po": "1",
    "np": "1",
    "ut": "bd1d9ddb04089700cf9c27f6f7426281",
    "fltt": "2",
    "invt": "2",
    "fid": "",
    "fs": "b:MK0010",
    "fields": "f2,f3,f6,f12,f14",
    "_": "1636183342285"
}

result = requests.get("http://45.push2.eastmoney.com/api/qt/clist/get", params=data)

newR = pattern.sub("\g<1>",result.text)
newR2 = json.loads(newR)

for i in newR2['data']['diff']:
    print(i['f14'])
    print(i['f2'])


print(result.text)
print("finished")
