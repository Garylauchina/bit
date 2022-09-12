import requests
import re
import json
import tushare as ts


# 用网易平台api获取股票数据。
def get_stock(stock_name):
    new_name = stock_name[-3:] + stock_name[:6]
    new_name = new_name.replace('.SH', '0')
    new_name = new_name.replace('.SZ', '1')
    new_name = new_name.replace('.BJ', '2')
    try:
        r = requests.get('http://api.money.126.net/data/feed/%s,money.api' % new_name).text
        #        r = r.encode().decode('unicode_escape')
        r = re.findall(r"_ntes_quote_callback\((.*)\);", r)
        r = r[0]
        r = json.loads(r)
        result = '名称：' + r[new_name]['name'] + '\n' + '代码：' + stock_name + '\n' + '当前价格：' + str(
            r[new_name]['price']) + '\n' + '涨跌：' + str(
            round(r[new_name]['percent'] * 100, 2)) + '%\n' + '开盘价格：' + str(
            r[new_name]['open']) + '\n' + '成交额：' + str(int(r[new_name]['turnover'] / 10000)) + '万元'
        return result
    except:
        return


# 用tushare平台获取股票数据
def ts_stocks():
    ts.set_token('c8b4deb22f79698808459d529f7fa3bae0522794dda732a5a9b8ed73')
    pro = ts.pro_api()
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name')
    #    print(data)
    stocks_dict = data.to_dict(orient='dict')
    bind_stocks = stocks_dict
    ts_code = bind_stocks['ts_code']  # 获得代码字典
    stock_name = bind_stocks['name']  # 或者名称字典
    all_stocks = {}
    for i in ts_code.keys():  # 代码和名称合并为一个字典
        all_stocks[stock_name[i]] = ts_code[i]
    return all_stocks


# s = ts_stocks()
# print(s)
def search_code(get_list, name):
    search_stock = []
    for i in get_list.keys():
        if name in i:
            # print(i + ' ' + s[i])
            search_stock.append(get_list[i])
    return search_stock

