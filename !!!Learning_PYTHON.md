

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
1. 启动数据库
```
brew services start mongodb-community@5.0
```
2. 插入

```python
pip3 install pymongo
import pymongo
mongo_client = pymongo.MongoClient('127.0.0.1', 27017)
mongo_collection.insert_one(info) # info是dict
mongo_collection.insert_many(insert_list)
```
3. 查询
```
select_item = mongo_collection.find_one(find_condition, projection= {'_id':False, 'name':True, 'num':True})# dict


