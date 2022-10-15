import os

import werobot

from joke import get_joke
from suangua import YiProgram
from sunshine import *
from stock import *
from chinamobile import *


class BitList:
    def __init__(self):
        self._ct_list = sunshine_list()
        self._ct_update = time.time()
        self._cm_list = cm_new_list()
        self._cm_update = time.time()

    def ct_list(self):
        return self._ct_list if self._ct_update - time.time() < 300 else self.refresh(1)

    def cm_list(self):
        return self._cm_list if self._cm_update - time.time() < 300 else self.refresh(2)

    def refresh(self, num):
        if num == 1:
            self._ct_update = time.time()
            self._ct_list = sunshine_list()
            return self._ct_list
        else:
            self._cm_update = time.time()
            self._cm_list = cm_new_list()
            return self._cm_list


bit_list = BitList()
print(bit_list.ct_list())
print(bit_list.cm_list())

now = time.strftime('%Y-%m-%d %H:%M:%S')
print('启动时间：' + now)
robot = werobot.WeRoBot(token='Dcbpes2098')
access_token = new_token()
token_time = int(time.time())
user_list = all_user(access_token)
lg_menu = '请输入：\n' \
          '1-广西电信招标\n' \
          '2-广西移动招标\n' \
          '3-每日一卦'

user_status = {openid: [0, 0] for openid in user_list}
print('总共%s名用户' % len(user_list))


def refresh_token():
    global access_token, token_time
    if int(time.time()) - token_time >= 3600:
        access_token = new_token()
        token_time = int(time.time())
        print('token已刷新，有效时间7200秒')
    else:
        print('token未过期，有效时间%s秒' % (7200 - (int(time.time()) - token_time)))
    return


@robot.filter('笑话')
def joke():
    return get_joke()


@robot.filter('update')
def git_update(msg):
    send_msg(['robot正在更新。。。'], msg.source, access_token)
    a = os.popen('git pull')
    return a.read()


@robot.filter('restart')
def robot_restart(msg):
    send_msg(['robot正在重启。。。'], msg.source, access_token)
    a = os.popen('supervisorctl restart wechat_robot')
    return a.read() + '\n' + 'robot重启成功'


@robot.handler
def echo(msg):
    refresh_token()
    # send_msg(['。。。'], msg.source, access_token)
    print(time.strftime('%Y-%m-%d %H:%M:%S') + '\'' + msg.source + '\'' + '\'' + msg.content + '\'')
    if msg.content == '1':
        wait_to_send = bit_list.ct_list()
        if not wait_to_send:
            return "广西电信今日无新公告\n" + lg_menu
        wait_to_send = send_msg(wait_to_send[user_status[msg.source][0]::], msg.source, access_token)
        if wait_to_send:
            user_status[msg.source][0] += 10
            return "还有%s条" % (len(wait_to_send))
        else:
            user_status[msg.source][0] = 0
            return '发送完毕\n' + lg_menu
    elif msg.content == '2':
        wait_to_send = bit_list.cm_list()
        if not wait_to_send:
            return "广西移动今日无新公告\n" + lg_menu
        wait_to_send = send_msg(wait_to_send[user_status[msg.source][1]::], msg.source, access_token)
        if wait_to_send:
            user_status[msg.source][1] += 10
            return "还有%s条" % (len(wait_to_send))
        else:
            user_status[msg.source][1] = 0
            return '发送完毕\n' + lg_menu
    elif msg.content[0] == '3':
        wish = msg.content[1:]
        if wish == '':
            return "请在3后面输入所求之事\n比如'3中标'"
        send_msg(['静心三秒。。。'], msg.source, access_token)
        obj = YiProgram()
        time.sleep(1)
        send_msg(obj.main_logic_new(wish + msg.source), msg.source, access_token)
        return '卜卦完毕\n' + lg_menu
    elif msg.content.isalpha():  # 判断输入的是字母或者中文
        realtime_list = real_time_stock(msg.content)  # 获取股票实时行情
        if len(realtime_list) > 10:
            return '包含 %s 的股票太多，请重新输入\n' % msg.content + lg_menu
        wait_to_send = []
        if realtime_list:
            for i in realtime_list:
                wait_to_send.append('名称：' + i['name'] + '\n' + \
                                    '代码：' + i['code'] + '\n' + \
                                    '价格：' + i['price'] + '\n' + \
                                    '今开：' + i['open'] + '\n' + \
                                    '昨收：' + i['pre_close'] + '\n' + \
                                    '成交：' + str(round(float(i['amount']) / 10000, 2)) + '万\n')
            send_msg(wait_to_send, msg.source, access_token)
            return '发送完毕\n' + lg_menu
        else:
            return '查不到"%s"股票信息\n' % msg.content + lg_menu
    else:
        return lg_menu


@robot.subscribe
def welcome(msg):
    refresh_token()
    user_status.update({msg.source: [0, 0]})
    print(msg.source + '用户关注')
    return "欢迎使用\n" + lg_menu


@robot.unsubscribe
def goodbye(msg):
    try:
        user_status.pop(msg.source)
        print(msg.source + '用户取关')
    except:
        pass


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
