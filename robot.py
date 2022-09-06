import werobot

robot = werobot.WeRoBot(token='Dcbpes2098')


@robot.handler
def echo(msg):
    print(msg)
    if msg.content == '1':
        return '正在查询，请稍后。。。'
    else:
        return '1---广西电信招标'


@robot.subscribe
def options(msg):
    return '1---广西电信招标'


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
