import requests


def get_joke():
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=笑话'
    r = requests.get(url)
    if r.status_code != 200:
        return '今天没笑话'
    return r.json()['content']


if __name__ == '__main__':
    joke = get_joke()
    print(type(joke))
    joke = joke.replace('提示：按分类看笑话请发送“笑话分类”', '')
    joke = joke.replace('{br}', '\n')
    print(joke)
