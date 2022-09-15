"""
目标1：熟练掌握enumerate命令进行列表操作
目标2：初步掌握用类进行编程
目标3：初步掌握函数装饰器的用法
目标4：初步掌握SQLite的用法
目标5：掌握后台爬虫定时工作的方法
"""
import werobot

robot = werobot.WeRoBot(token='Dcbpes2098')


@robot.text
def hello_world():
    return 'Hello World!'

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
