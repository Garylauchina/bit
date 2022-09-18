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


if __name__ == '__main__':
    joke = get_joke()
    print(joke)
