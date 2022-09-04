import requests
import json

argu1 = 'client_credential'
argu2 = 'wx7bd1096d014dc5c4'
argu3 = '6bf950052b38e94da3259b5a4bc11e12'
base_url = 'https://api.weixin.qq.com/cgi-bin'
token_url = '/token?grant_type=%s&appid=%s&secret=%s' % (argu1, argu2, argu3)
upload_url = '/material/add_material?access_token=%s&type=image'
access_token = requests.get(base_url + token_url).json()['access_token']
print(access_token)

with open('test.jpg', 'rb') as fp:
    files = {'type': 'image', 'media': fp}
    print(files)
    r = requests.post(base_url + upload_url % access_token, files=files)
    print(r.json())
