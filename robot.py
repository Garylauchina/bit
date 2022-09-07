import werobot
from sunshine import *
import time

robot = werobot.WeRoBot(token='Dcbpes2098')
access_token = Access_Token()
token_time = int(time.time())
user_list = all_user(access_token)

user_label = {}
user_store = []
today_list = sunshine_list()  # 这是一个列表，里面的元素是字典,存储了当天的招标信息，需定时更新
print('共搜索到%s条招标信息' % len(today_list))
for i in user_list:
    user_label['openid'] = i
    user_label['last_send'] = 0
    user_store.append(user_label.copy())
print(user_store)


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


def put_list_store(get_id):
    for j in user_store:
        if j['openid'] == get_id:
            j['wait_to_send'] = today_list
    return


@robot.handler
def echo(msg):
    refresh_token()
    print(msg.source)
    if msg.content == '1':
        for j in user_store:  # 遍历user_store
            if j['openid'] == msg.source:  # 检索库中的用户id
                if len(today_list) - j['last_send'] > 10:  # 如果存在未发数据
                    wait_to_send = today_list[j['last_send']:j['last_send'] + 3]  # 则切片最多最多3条并发送
                    for k in range(len(wait_to_send)):
                        send_msg(wait_to_send[k]['docTitle'], msg.source, access_token)
                    j['last_send'] += 3  # 发送完成，更新用户的发送标记
                    send_msg('点击继续', msg.source, access_token)
                    return '点击继续'
                else:
                    wait_to_send = today_list[j['last_send']::]
                    for k in range(len(wait_to_send)):
                        send_msg(wait_to_send[k]['docTitle'], msg.source, access_token)
                    j['last_send'] += 0  # 发送完成，清除标记
                    send_msg('发送完毕', msg.source, access_token)
                    return '发送完毕'
    else:
        return '别考我我不是聊天机器人！'



@robot.subscribe
def welcome(msg):
    refresh_token()
    return '欢迎使用！'


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
