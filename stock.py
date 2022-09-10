import requests
import re
import json
import tushare as ts


# 用网易平台api获取股票数据。
def get_stock(stock_name):
    try:
        r = requests.get('http://api.money.126.net/data/feed/%s,money.api' % stock_name).text
        #        r = r.encode().decode('unicode_escape')
        r = re.findall(r"_ntes_quote_callback\((.*)\);", r)
        r = r[0]
        r = json.loads(r)
        result = '名称：' + r[stock_name]['name'] + '\n' + '当前价格：' + str(
            r[stock_name]['price']) + '\n' + '涨跌：' + str(
            round(r[stock_name]['percent'], 2)) + '%\n' + '开盘价格：' + str(
            r[stock_name]['open']) + '\n' + '成交额：' + str(int(r[stock_name]['turnover'] / 10000)) + '万元'
    except:
        result = stock_name[1:] + '未查询到该股票数据'
    return result


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
    for i in all_stocks.keys():
        all_stocks[i] = all_stocks[i][-3:] + all_stocks[i][:6]
        all_stocks[i] = all_stocks[i].replace('.SH', '0')
        all_stocks[i] = all_stocks[i].replace('.SZ', '1')
        all_stocks[i] = all_stocks[i].replace('.BJ', '2')
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
# aa = search_code('石油')
# for i in aa:
#     print(get_stock(i))
