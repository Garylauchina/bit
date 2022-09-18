import requests


def get_joke():
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=笑话'
    r = requests.get(url)
    if r.status_code != 200:
        return '今天没笑话'
    r = r.json()['content']
    r = r.replace('提示：按分类看笑话请发送“笑话分类”', '')
    r = r.replace('{br}', '\n')
    return r


def kuki_chat(talk):
    url = 'https://devman.kuki.ai/talk'
    data = {
        'botkey': 'e8f4d92be20f62f58972585917e549e610c7c158abeccedf77f7ed4e0b3647a4',
        'input': talk,
        'client_name': 'foo',
    }
    r = requests.post(url,data=data)
    r = r.json()
    return r['responses'][0]


if __name__ == '__main__':
    while True:
        chatbox = input()
        if chatbox == 'exit':
            exit()
        chat = kuki_chat(chatbox)
        print(chat)
