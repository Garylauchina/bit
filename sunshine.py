import time
import requests
import json

argu1 = 'client_credential'
argu2 = 'wx7bd1096d014dc5c4'
argu3 = '6bf950052b38e94da3259b5a4bc11e12'
base_url = 'https://api.weixin.qq.com/cgi-bin'
test_id = 'o-4JI0ibLP9genCK8KVGz_KKkWWE'  # 刘刚的openid


def add_user(get_store, get_id):
    user_label = {'openid': get_id, 'last_send': 0, 'film_send': 0}
    get_store.append(user_label.copy())
    return get_store


def all_user(get_token) -> list[str]:
    get_id_url = '/user/get?access_token=%s&next_openid'
    a = requests.get(base_url + get_id_url % get_token).json()['data']['openid']
    return a  # 返回[openid]列表


def new_token():
    token_url = '/token?grant_type=%s&appid=%s&secret=%s' % (argu1, argu2, argu3)
    #
    #    id_info_url = '/user/info?access_token=%s&openid=%s&lang=zh_CN'
    a = requests.get(base_url + token_url).json()
    print('获取token成功：' + a['access_token'])
    print('有效期：' + str(a['expires_in']) + '秒')
    return a['access_token']


# 向微信公众号的用户发送消息
def send_msg(message_list, get_user, get_token):  # 发送列表中的元素,最多十个
    send_url = '/message/custom/send?access_token=%s'
    for i in range(min(len(message_list), 10)):
        content = {
            'content': message_list[i]
        }
        msg_pkg = {'touser': get_user, 'msgtype': 'text', 'text': content}
        requests.post(base_url + send_url % get_token, json.dumps(msg_pkg, ensure_ascii=False).encode('utf-8'))
    return message_list[10::]  # 去除前十个数据后返回


def sunshine_list():
    # 中国电信阳光采购网
    url = 'https://caigou.chinatelecom.com.cn/portal/base/announcementJoin/queryList'
    bit_list = []
    today = int(time.strftime('%Y%m%d', time.localtime()))
    hasnextpage = True
    headers = {
        'Accept': 'application/json,text/plain,*/*',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '107',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'Secure;Secure;CaiGouServiceInfo=!OMtbDA1sN2Py46c1qhgwHmp4DxKAGFH+DKDyAO7lgQKpNe9HwoMbDwU/c/+2'
                  '+6foSh7UiZwftGPZv/8=;JSESSIONID=0000tGpQLjAkIEtrEg9v2AVqXEq:18djc0l04;Secure=',
        'Host': 'caigou.chinatelecom.com.cn',
        'Origin': 'https://caigou.chinatelecom.com.cn',
        'Referer': 'https://caigou.chinatelecom.com.cn/ctsc-portal/search?search=',
        'sec-ch-ua': '"GoogleChrome";v="105","Not)A;Brand";v="8","Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,'
                      'likeGecko)Chrome/105.0.0.0Safari/537.36',
    }
    data = {
        'pageNum': 1,
        'pageSize': 10,
        'provinceCode': "10",
        'queryEndTime': "",
        'queryStartTime': '',
        'title': "",
        'type': "0"
    }
    while hasnextpage:
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code != 200:
                break
            r = r.json()['data']
            hasnextpage = r['hasNextPage']
            for i in r['list']:
                if today == int(i['createDate'][0:10].replace('-', '')):  # 判断发布时间是否当天
                    bit_list.append(i['docTitle'])
                else:
                    hasnextpage = False
            data['pageNum'] = data['pageNum'] + 1
        except TimeoutError:
            return []
    return bit_list


def make_img(get_list):
    return


def main():
    make_img(sunshine_list())


if __name__ == '__main__':
    main()
