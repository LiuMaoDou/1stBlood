

## pycharm
1. 批量增加引号

```python
Ctrl+R 
(.*?): (.*)
'$1':'$2'
```

## Pandas
1. from_list
```python
df = pd.DataFrame(lst, columns =['Name', 'Age'])
```
![image](https://user-images.githubusercontent.com/65071754/141647846-9f91cdfd-f5c2-4649-9d20-bb815379b90b.png)

2. to_excel 
```python
df.to_excel('test.xlsx')
```

3. to_dict
```python
df.to_dict('series')
```
![image](https://user-images.githubusercontent.com/65071754/141647757-e0049612-c79a-4953-80fb-24681ffa50e7.png)

4. from_dict
```
pd.DataFrame.from_dict(data, orient='index', columns=['A', 'B', 'C', 'D'])
df = pd.DataFrame(select_item[0],index=[0]) # 如果只有一行

df = pd.DataFrame(columns=['名称','日期','最新价','涨跌幅'])
for i in select_item:
    df = df.append(i, ignore_index=True)
```
5. column改名
```python
df.rename(columns={'最新价':'上证指数'},inplace=False)
```
6. 某一列当index
```python
df.set_index('日期',inplace=True)
```
7. 重复值
```python
df.duplicated() #第一次重复的不算
df.duplicated(keep='last') #最后一次重复的不算,默认是first
df.duplicated(keep=False) #所有重复的都是True
df.duplicated(subset=['B'], keep=False) #指定列检测
df[df.duplicated()] #筛选重复值

df.drop_duplicates()
```
8. pandas合并
`df1.append(df2)`
9. 数据筛选
`df[df['end_date'=='20210930']]`
10. 修改列名
`data.rename(columns={'ts_code':'symbol'},inplace=True)`
11. 数据合并
`test = pd.merge(df_data,data, on = "symbol")`
12. 排序
`test.sort_values("mkv",ascending=False)`



## pymongo
1. 启动/关闭数据库
```
brew services start mongodb-community@5.0
brew services stop mongodb-community@5.0
```
2. 插入

```python
pip3 install pymongo
import pymongo
mongo_client = pymongo.MongoClient('127.0.0.1', 27017)
mongo_db = mongo_client['股票']
mongo_collection = mongo_db['指数']
mongo_collection.insert_one(info) # info是dict
mongo_collection.insert_many(insert_list)
```
3. 查询
```
find_condition = {
    '日期' : {'$gte':datetime.datetime(2021,11,13), '$lt':datetime.datetime(2021,11,14)}
}
select_item = mongo_collection.find_one(find_condition)
select_item = mongo_collection.find_one(find_condition, projection= {'_id':False, 'name':True, 'num':True})# dict
select_item = mongo_collection.find(find_condition,{'_id':0})

```

4. 删除
```
mongo_collection.delete_many({}) # 删除collection所有
mongo_collection.drop() 
```

5. 更新
```
mongo_collection.update_one({"日期": {'$gte':datetime.datetime(2021,11,16,0,1), '$lt':datetime.datetime(2021,11,17)}},
                        {'$set' : {'日期':datetime.datetime(2021, 11, 16, 0, 0)}})

mongo_collection.update_many({"日期": {'$gte':datetime.datetime(2021,11,16,0,1), '$lt':datetime.datetime(2021,11,17)}},
                        {'$set' : {'日期':datetime.datetime(2021, 11, 16, 0, 0)}})
```

## matplotlib.pyplot


data=json.dumps(payload) -- 字典转JSON
