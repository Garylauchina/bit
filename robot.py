from ddys import *
import werobot
from sunshine import *
from stock import *
import time
from chinamobile import *

now = time.strftime('%Y-%m-%d %H:%M:%S')
print('启动时间：' + now)
print("版本1.4 加入广西移动招标信息")
robot = werobot.WeRoBot(token='Dcbpes2098')
access_token = new_token()
token_time = int(time.time())
user_list = all_user(access_token)
lg_menu = '请输入：\n1-广西电信招标\n2-广西移动招标\n3-热门影视\n或者股票中文名，比如"石油"'
# 更新电信招标信息
ct_list = sunshine_list()  # 这是一个列表，里面的元素是列表,存储了当天的招标信息，需定时更新
ct_list_time = time.time()  # 电信招标信息更新的时间
print('共搜索到%s条电信招标信息' % len(ct_list))
# 更新移动招标信息
cm_list = cm_new_list()
cm_list_time = time.time()  # 移动招标列表更新时间
print('共搜索到%s条移动招标信息' % len(cm_list))
# 更新电影清单
hot_film = film_list()
hot_film_time = time.time()  # 电影清单更新时间
print('共搜索到%s部热门电影' % len(hot_film))
# 初始化用户状态库
user_status = {}
for i in user_list:
    user_status[i] = [0, 0, 0, 0]  # 初始化用户状态，四个数值分别代表四个列表的发送断点
print('总共%s名用户' % len(user_list))
# 获取所有上市公司清单
all_stocks = ts_stocks()  # 获取所有上市公司清单
print('更新%s家上市公司信息' % len(all_stocks))


def refresh_list(get_id):
    global ct_list, hot_film, ct_list_time, hot_film_time, cm_list_time, cm_list
    if get_id == '1':
        if time.time() - ct_list_time > 1800:  # 每三十分钟更新一次招标信息
            ct_list = sunshine_list()
            ct_list_time = time.time()
            print('电信招标信息已更新')
    elif get_id == '3':
        if time.time() - hot_film_time > 1800:  # 每三十分钟更新一次招标信息
            hot_film = film_list()
            hot_film_time = time.time()
            print('电影列表已更新')
    elif get_id == '2':
        if time.time() - cm_list_time > 1800:  # 每三十分钟更新一次招标信息
            cm_list = cm_new_list()
            cm_list_time = time.time()
            print('移动招标信息已更新')
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
    global ct_list, ct_list_time, hot_film, hot_film_time, cm_list, cm_list_time, all_stocks, user_status
    refresh_token()
    print(msg.source)
    refresh_list(msg.content)
    user_tag = user_status[msg.source]  # 获取用户的状态码列表
    if msg.content == '1':
        wait_to_send = send_msg(ct_list[user_tag[0]::], msg.source, access_token)
        if wait_to_send:
            user_tag[0] += 10
            return "还有%s条" % (len(ct_list) - user_tag[0])
        else:
            user_tag[0] = 0
            return '发送完毕\n' + lg_menu
    elif msg.content == '2':
        wait_to_send = send_msg(cm_list[user_tag[1]::], msg.source, access_token)
        if wait_to_send:
            user_tag[1] += 10
            return "还有%s条" % (len(cm_list) - user_tag[1])
        else:
            user_tag[1] = 0
            return '发送完毕\n' + lg_menu
    elif msg.content == '3':
        wait_to_send = send_msg(hot_film[user_tag[2]::], msg.source, access_token)
        if wait_to_send:
            user_tag[2] += 10
            return "还有%s条" % (len(hot_film) - user_tag[2])
        else:
            user_tag[2] = 0
            return '发送完毕\n' + lg_menu
    elif '\u4e00' <= msg.content <= '\u9fa5':  # 判断输入的是中文
        codes = search_code(all_stocks, msg.content)
        if len(codes) == 0:
            return '没有%s这个股票\n' % msg.content + lg_menu
        else:
            stock_data = []
            for j in codes:
                stock_data.append(get_stock(j))
            wait_to_send = send_msg(stock_data[user_tag[3]::], msg.source, access_token)
            if wait_to_send:
                user_tag[3] += 10
                return "还有%s条" % (len(stock_data) - user_tag[3])
            else:
                user_tag[3] = 0
                return '发送完毕\n' + lg_menu
    return lg_menu


@robot.subscribe
def welcome(msg):
    global access_token, user_list, user_status
    refresh_token()
    refresh_list(1)
    refresh_list(2)
    user_list = all_user(access_token)
    add_user(user_status, msg.source)
    return '1---电信招标网（阳光\n2---热门影视\n或者输入股票中文名，比如"石油"'



robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
