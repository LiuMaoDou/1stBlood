[toc]

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
2. to_excel 
```python
df.to_excel('test.xlsx')
```
