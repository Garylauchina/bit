import requests


def get_joke():
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=笑话'
    r = requests.get(url)
    if r.status_code != 200:
        return '今天没笑话'
    return r.json()['content']


if __name__ == '__main__':
    joke = get_joke()
    print(joke['content'])
