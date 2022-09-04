import requests

argu1 = 'client_credential'
argu2 = 'wx7bd1096d014dc5c4'
argu3 = '6bf950052b38e94da3259b5a4bc11e12'
base_url = 'https://api.weixin.qq.com/cgi-bin'
token_url = '/token?grant_type=' + argu1 + '&appid=' + argu2 + '&secret=' + argu3
menu_url = '/menu/create?access_token='
r = requests.get(base_url + token_url)
access_token = r.json()['access_token']
print(access_token)

menu = {
    "button": [
        {
            "type": "click",
            "name": "查询",
            "key": "V1001_TODAY_MUSIC"
        }
    ]
}
creat_menu = requests.post(base_url + token_url + access_token, menu)
if creat_menu.status_code == 200:
    print('创建菜单成功')
else:
    print(creat_menu.json()['errmsg'])
