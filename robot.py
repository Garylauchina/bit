from ddys import *
import werobot
from sunshine import *
import time

print("版本1.1 加入supervisor进程")
robot = werobot.WeRoBot(token='Dcbpes2098')
access_token = Access_Token()
token_time = int(time.time())
user_list = all_user(access_token)

user_label = {}
user_store = []
hot_film = film_list()
today_list = sunshine_list()  # 这是一个列表，里面的元素是字典,存储了当天的招标信息，需定时更新
today_list_time = time.time()  #上次招标信息更新的时间
print('共搜索到%s条招标信息' % len(today_list))
for i in user_list:
    user_label['openid'] = i
    user_label['last_send'] = 0
    user_label['film_send'] = 0
    user_store.append(user_label.copy())
print(user_store)
def refresh_list(get_list):
    global today_list_time
    if time.time() - today_list_time > 1800:    #每三十分钟更新一次招标信息
        get_list = sunshine_list()
        today_list_time = time.time()
        print('列表已更新')
    return get_list

def refresh_token():
    global access_token
    global token_time
    if int(time.time()) - token_time >= 3600:
        access_token = Access_Token()
        token_time = int(time.time())
        print('token已刷新，有效时间7200秒')
    else:
        print('token未过期，有效时间%s秒' % (7200 - (int(time.time()) - token_time)))
    return


@robot.handler
def echo(msg):
    refresh_token()
    refresh_list(today_list)
    print(msg.source)
    if msg.content == '2':
        for j in user_store:  # 遍历user_store
            if j['openid'] == msg.source:  # 检索库中的用户id
                if len(hot_film) - j['film_send'] > 10:  # 如果存在未发数据
                    wait_to_send = hot_film[j['film_send']:j['film_send'] + 10]  # 则切片最多最多3条并发送
                    for k in range(len(wait_to_send)):
                        send_msg(wait_to_send[k], msg.source, access_token)
                    j['film_send'] += 10  # 发送完成，更新用户的发送标记
                    return "还有%s条"%(len(hot_film) - j['film_send'])
                else:
                    wait_to_send = hot_film[j['film_send']::]
                    for k in range(len(wait_to_send)):
                        send_msg(wait_to_send[k], msg.source, access_token)
                    j['film_send'] = 0  # 发送完成，清除标记
                    return '发送完毕'
    else:
        if msg.content == '1':
            for j in user_store:  # 遍历user_store
                if j['openid'] == msg.source:  # 检索库中的用户id
                    if len(today_list) - j['last_send'] > 10:  # 如果存在未发数据
                        wait_to_send = today_list[j['last_send']:j['last_send'] + 10]  # 则切片最多最多3条并发送
                        for k in range(len(wait_to_send)):
                            send_msg(wait_to_send[k]['docTitle'], msg.source, access_token)
                        j['last_send'] += 10  # 发送完成，更新用户的发送标记
                        return "还有%s条" % (len(today_list) - j['last_send'])
                    else:
                        wait_to_send = today_list[j['last_send']::]
                        for k in range(len(wait_to_send)):
                            send_msg(wait_to_send[k]['docTitle'], msg.source, access_token)
                        j['last_send'] = 0  # 发送完成，清除标记
                        return '发送完毕'

        return '1---电信招标网（阳光）\n 2---热门影视'



@robot.subscribe
def welcome(msg):
    refresh_token()
    user_list.append(msg.source)
    user_label['openid'] = msg.source
    user_label['last_send'] = 0
    user_store.append(user_label.copy())
    return '1---电信招标网（阳光）\n 2---热门影视'


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
