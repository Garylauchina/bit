import werobot

robot = werobot.WeRoBot(token='Dcbpes2098')


@robot.handler
def echo(message):
    return '别发了我不是聊天机器人！'


@robot.click
def option(msg):
    print(type(msg))
    print(msg)
    if msg.key == 'v1':
        return '正在查询，请稍后。。。'
    if msg.key == 'v2':
        return '请点赞支持！'


@robot.subscribe
def welcome(msg):
    return '欢迎使用！'


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
