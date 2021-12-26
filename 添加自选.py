from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
chrome_options.add_argument("disable-blink-features=AutomationControlled")#就是这一行告诉chrome去掉了webdriver痕迹
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("http://t.10jqka.com.cn/newcircle/user/userPersonal/?from=circle")
# 用户登录

dtypes = {'code_a': 'str', 'code_b': 'str', 'name': 'str'}
df = pd.read_csv('message_source.csv', dtype=dtypes)
codeLists = df['code_a'].to_list()

for code in codeLists:
    driver.get("http://t.10jqka.com.cn/newcircle/group/modifySelfStock/?callback=modifyStock&op=add&stockcode={}".format(code))
