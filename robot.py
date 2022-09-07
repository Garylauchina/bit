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
threedays_list = sunshine_list()  # 这是一个列表，里面的元素是字典,存储了近三天的招标信息，需定时更新
for i in user_list:
    user_label = {'openid':i,'wait_to_send':[]}
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
        print('token未过期，有效时间%s秒' % (int(time.time()) - token_time))
    return


def put_list_store(get_id):
    for i in user_store:
        if i['openid'] == get_id:
            i['wait_to_send'] = threedays_list
    return


@robot.click
def option(msg):
    refresh_token()
    print(msg.source)
    if msg.key == 'v1':
        for i in user_store:  # 遍历user_store
            if i['openid'] == msg.source:  # 检索库中的用户id
                if len(i['wait_to_send']) == 0:  # 如果待发送库中列表为0，
                    to_send_list = copy.copy(threedays_list)  # 则复制threedays_list,
                for j in range([10, len(to_send_list)][len(to_send_list) <= 10]):  # 如果超过十条就发十条，不超过就全发
                    send_msg(to_send_list.pop[0]['docTitle'], msg.source, access_token)
               if len(to_send_list) == 0:
                    i['wait_to_send'] = []
                    send_msg('查询完成', msg.source, access_token)  # 最后检查，如果待发送库中列表为0，则最后一条发送为"完成"，
                    return '查询完成'
                else:
                    send_msg('点击继续发送', msg.source, access_token)  # 否则为"继续点击"
                    i['wait_to_send'] = to_send_list
                    return '等待用户点击'
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
