import requests
import json

argu1 = 'client_credential'
argu2 = 'wx7bd1096d014dc5c4'
argu3 = '6bf950052b38e94da3259b5a4bc11e12'
base_url = 'https://api.weixin.qq.com/cgi-bin'
token_url = '/token?grant_type=' + argu1 + '&appid=' + argu2 + '&secret=' + argu3
creat_menu_url = '/menu/create?access_token='
access_token = requests.get(base_url + token_url).json()['access_token']
print(access_token)

menu = {
    "button": [
        {
            'type':'click',
            'name':'查询',
            'key':'v1'
        },
        {
            "type": "click",
            "name": "点赞",
            "key": "v2"
        }
    ]
}
k = json.dumps(menu, ensure_ascii=False).encode('utf-8')
creat_menu = requests.post(base_url + creat_menu_url + access_token, k)
print(creat_menu.json()['errmsg'])
