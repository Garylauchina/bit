import werobot
from sunshine import *
import time
import copy

robot = werobot.WeRoBot(token='Dcbpes2098')
access_token = Access_Token()
user_list = all_user(access_token)
token_time = int(time.time())
print(token_time)
user_label = {}
user_store =[]
k = sunshine_list(1)
for i in user_list:
    user_label['openid'] = i
    user_label['lasttime'] = token_time
    if user_label['openid'] == test_id:
        user_label['wait_to_send'] = k
    else:
        user_label['wait_to_send'] = []
    k = copy.copy(user_label)
    user_store.append(k)
print(user_store)



@robot.click
def option(msg):
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
    return '欢迎使用！'

@robot.handler
def echo(message):
    return '别发了我不是聊天机器人！'

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
