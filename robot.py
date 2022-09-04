import werobot

robot = werobot.WeRoBot(token='Dcbpes2098')


@robot.handler
def hello(msg):
    return 'Hello World!'


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
