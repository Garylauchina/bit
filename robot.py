from ddys import *
import werobot
from sunshine import *
from stock import *
import time

now = time.strftime('%Y-%m-%d %H:%M:%S')
print('启动时间：' + now)
print("版本1.3 加入股票查询")
robot = werobot.WeRoBot(token='Dcbpes2098')
access_token = new_token()
token_time = int(time.time())
user_list = all_user(access_token)

user_label = {}
user_store = []
hot_film = film_list()
print('共搜索到%s部热门电影' % len(hot_film))
today_list = sunshine_list()  # 这是一个列表，里面的元素是字典,存储了当天的招标信息，需定时更新
today_list_time = time.time()  # 上次招标信息更新的时间
hot_film_time = time.time()     #电影清单更新时间
print('共搜索到%s条招标信息' % len(today_list))
for i in user_list:
    add_user(user_store, i)
print('总共%s名用户' % len(user_store))
all_stocks= ts_stocks()          #获取所有上市公司清单


def refresh_list(get_id):
    global today_list, hot_film, today_list_time, hot_film_time
    if get_id == 1:
        if time.time() - today_list_time > 1800:  # 每三十分钟更新一次招标信息
            today_list = sunshine_list()
            today_list_time = time.time()
            print('招标列表已更新')
    else:
        if get_id == 2:
            if time.time() - hot_film_time > 1800:  # 每三十分钟更新一次招标信息
                hot_film = film_list()
                hot_film_time = time.time()
                print('电影列表已更新')
    return


def refresh_token():
    global access_token, token_time
    if int(time.time()) - token_time >= 3600:
        access_token = new_token()
        token_time = int(time.time())
        print('token已刷新，有效时间7200秒')
    else:
        print('token未过期，有效时间%s秒' % (7200 - (int(time.time()) - token_time)))
    return


@robot.handler
def echo(msg):
    global today_list_time, hot_film,all_stocks
    refresh_token()
    print(msg.source)
    if msg.content == '1':
        refresh_list(1)
        for j in user_store:  # 遍历user_store
            if j['openid'] == msg.source:
                if len(today_list) - j['last_send'] > 10:  # 如果存在未发数据
                    wait_to_send = today_list[j['last_send']:j['last_send'] + 10]  # 则切片最多最多10条并发送
                    for k in wait_to_send:
                        send_msg(k, msg.source, access_token)
                    j['last_send'] += 10  # 发送完成，更新用户的发送标记
                    return "还有%s条" % (len(today_list) - j['last_send'])
                else:
                    wait_to_send = today_list[j['last_send']::]
                    for k in wait_to_send:
                        send_msg(k, msg.source, access_token)
                    j['last_send'] = 0  # 发送完成，清除标记
                    return '发送完毕\n1-电信招标网（阳光\n2-热门影视\n或者输入股票中文名，比如"石油"'
    elif msg.content == '2':
        refresh_list(2)
        for j in user_store:  # 遍历user_store
            if j['openid'] == msg.source:
                if len(hot_film) - j['film_send'] > 10:  # 如果存在未发数据
                    wait_to_send = hot_film[j['film_send']:j['film_send'] + 10]  # 则切片最多最多10条并发送
                    for k in wait_to_send:
                        send_msg(k, msg.source, access_token)
                    j['film_send'] += 10  # 发送完成，更新用户的发送标记
                    return "还有%s条" % (len(hot_film) - j['film_send'])
                else:
                    wait_to_send = hot_film[j['film_send']::]
                    for k in wait_to_send:
                        send_msg(k, msg.source, access_token)
                    j['film_send'] = 0  # 发送完成，清除标记
                    return '发送完毕\n1-电信招标网（阳光\n2-热门影视\n或者输入股票中文名，比如"石油"'
    elif len(msg.content) > 1:
        codes = search_code(all_stocks,msg.content)
        for i in codes[:10]:
            send_msg(i,msg.source,access_token)
        if len(codes) > 10:
            send_msg('名字可以准确点，谢谢',msg.source,access_token)
        return '1-电信招标网（阳光\n2-热门影视\n或者输入股票中文名，比如"石油"'
    return '1-电信招标网（阳光\n2-热门影视\n或者输入股票中文名，比如"石油"'


@robot.subscribe
def welcome(msg):
    global access_token, user_list, user_store
    refresh_token()
    refresh_list(1)
    refresh_list(2)
    user_list = all_user(access_token)
    add_user(user_store, msg.source)
    return '1---电信招标网（阳光\n2---热门影视\n或者输入股票中文名，比如"石油"'


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
