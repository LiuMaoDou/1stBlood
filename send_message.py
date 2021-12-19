import requests
token = '***'

flomo_data={
'content':'测试:发送一条数据给你'
}

wx_data={
'text':'你的标题', '{desp}'.format(desp=flomo_data['content']):'最大支持64KB的文字内容'
}

requests.post('https://flomoapp.com/iwh/MjMyNTE1/b2a4807c1ab2855b7f65c745afb248ef/', data=flomo_data) 
requests.post('http://wx.xtuis.cn/{token}.send'.format(token=token), data=wx_data) 
