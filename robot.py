import werobot
from sunshine import *
import time
import copy

robot = werobot.WeRoBot(token='Dcbpes2098')
access_token = Access_Token()
token_time = int(time.time())
user_list = all_user(access_token)


user_label = {}
user_store = []
threedays_list = sunshine_list()
for i in user_list:
    user_label['openid'] = i
    user_label['lasttime'] = token_time
    if user_label['openid'] == test_id:
        user_label['wait_to_send'] = threedays_list
    else:
        user_label['wait_to_send'] = []
    user_store.append(copy.copy(user_label))
print(user_store)

def refresh_token():
    global access_token
    global token_time
    if int(time.time()) - token_time >= 3600:
        access_token = Access_Token()
        token_time = int(time.time())
        print('token已刷新，有效时间7200秒')
    else:
        print('token未过期，有效时间%s秒'%(int(time.time())-token_time))
    return

@robot.click
def option(msg):
    refresh_token()
    print(msg.source)
    if msg.key == 'v1':
        for i in user_store:
            if i[msg.source] != [] and i['openid'] == msg.source:
                send_msg('正在查询，请稍后。。。',msg.source)
                for j in i['wait_to_send'].pop(0):
                    send_msg(j['docTitle'],msg.source)
        return "查询完成！"
    if msg.key == 'v2':
        return '祝您中标！'


@robot.subscribe
def welcome(msg):
    refresh_token()
    return '欢迎使用！'

@robot.handler
def echo(msg):
    refresh_token()
    return '别发了我不是聊天机器人！'

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
