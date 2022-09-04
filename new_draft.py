import requests
import json

argu1 = 'client_credential'
argu2 = 'wx7bd1096d014dc5c4'
argu3 = '6bf950052b38e94da3259b5a4bc11e12'
base_url = 'https://api.weixin.qq.com/cgi-bin'
token_url = '/token?grant_type=' + argu1 + '&appid=' + argu2 + '&secret=' + argu3
get_id_url = '/user/get?access_token='
send_url = '/message/custom/send?access_token='
access_token = requests.get(base_url + token_url).json()['access_token']
print(access_token)

# 获取用户ID
id_list = requests.get(base_url + get_id_url + access_token + '&next_openid')
id_list = id_list.json()['data']['openid']
print(id_list)

message = "这是一个测试消息"
content = {
    'content': message
}
k = json.dumps(message, ensure_ascii=False).encode('utf-8')
send_data = {}
for n in range(len(id_list)):
    send_data['touser'] = id_list[n]
    send_data['msgtype'] = 'text'
    send_data['text'] = content
    r = requests.post(base_url + send_url + access_token, json.dumps(send_data, ensure_ascii=False).encode('utf-8'))
    if r.json()['errcode'] != 0:
        print('第%s个用户发送失败' % (n+1))
        print(r.json()['errmsg'])
    else:
        print('第%s个用户发送成功，请查收！' % (n+1))
