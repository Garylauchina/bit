import requests
import re
import json


def get_stock(stock_name):
    try:
        r = requests.get('http://api.money.126.net/data/feed/%s,money.api' % stock_name).text
        #        r = r.encode().decode('unicode_escape')
        r = re.findall(r"_ntes_quote_callback\((.*)\);", r)
        r = r[0]
        r = json.loads(r)
        result = '名称：' + r[stock_name]['name'] + '\n' + '当前价格：' + str(
            r[stock_name]['price']) + '\n' + '涨跌：' + str(
            r[stock_name]['percent']) + '\n' + '开盘价格：' + str(r[stock_name]['open']) + '\n' + '成交额：' + str(
            r[stock_name]['turnover'])
    except:
        result = 'SH:0xxxxxx\nSZ:1xxxxxx\nBJ:2xxxxxx'
    return result
