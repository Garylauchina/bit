import tushare as ts
from collections import namedtuple

'''
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
'''


# 用tushare平台获取股票数据
def ts_stocks():
    ts.set_token('c8b4deb22f79698808459d529f7fa3bae0522794dda732a5a9b8ed73')
    pro = ts.pro_api()
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name')
    #    print(data)
    all_stocks = {data.name[i]: data.ts_code[i] for i in range(len(data))}
    return all_stocks


def real_time_stock(get_name):
    ts.set_token('c8b4deb22f79698808459d529f7fa3bae0522794dda732a5a9b8ed73')
    stocks = ts_stocks()
    search_stocks = [code[:6] for name, code in stocks.items() if get_name in name]
    search_result = ts.get_realtime_quotes(search_stocks)
    show_result = [
        {'name': search_result.name[i],
         'code': search_result.code[i],
         'price': search_result.price[i],
         'open': search_result.open[i],
         'pre_close': search_result.pre_close[i],
         'amount': search_result.amount[i]}
        for i in range(len(search_result))]
    show_result.sort(key=lambda s: s['name'])
    return show_result


def main():
    stocks = ts_stocks()
    print(len(stocks))
    search_name = input('输入股票名：')
    print(real_time_stock(search_name))


if __name__ == '__main__':
    main()
