import werobot

robot = werobot.WeRoBot(token='Dcbpes2098')


@robot.filter("1")
def hello(msg):
    return '已为您订阅，每天23点推送当天招标信息'

@robot.subscribe
def options(msg):
    return '1---广西电信招标'


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
