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
        result = r[stock_name]['name'] + '\n' + str(r[stock_name]['price'])
    except:
        result = 'SH:0xxxxxx\nSZ:1xxxxxx\nBJ:2xxxxxx'
    return result

