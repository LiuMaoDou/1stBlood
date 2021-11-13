

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
select_item = mongo_collection.find_one(find_condition, projection= {'_id':False, 'name':True, 'num':True})# dict

find_condition = {
    '日期' : {'$gte':datetime.datetime(2021,11,13), '$lt':datetime.datetime(2021,11,14)}
}
select_item = mongo_collection.find_one(find_condition)
```

4. 删除
```
mongo_collection.delete_many({}) # 删除collection所有
mongo_collection.drop() 
```


