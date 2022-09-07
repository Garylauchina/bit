import requests
import json

argu1 = 'client_credential'
argu2 = 'wx7bd1096d014dc5c4'
argu3 = '6bf950052b38e94da3259b5a4bc11e12'
base_url = 'https://api.weixin.qq.com/cgi-bin'
token_url = '/token?grant_type=' + argu1 + '&appid=' + argu2 + '&secret=' + argu3
delete_menu_url = '/menu/delete?access_token=%s'
access_token = requests.get(base_url + token_url).json()['access_token']
print(access_token)
r = requests.get(base_url + delete_menu_url % access_token)
print(r)
