import pprint

import requests
import re

# a = input('请输入股票代码：')
r = requests.get('http://api.money.126.net/data/feed/1000777,money.api').text
print(r)
r = r[33:-5].replace(' ','').replace('"','')
r = r.split(',')
# for i in r:
#     print(i)
print(r[30]+'\n'+r[7])
