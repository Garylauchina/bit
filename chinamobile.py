import re
import time

import requests
from bs4 import BeautifulSoup


# 解决了二次传送post参数的问题
def cm_new_list():
    requests.packages.urllib3.disable_warnings()
    url = 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2'
    r = requests.get(url, verify=False)
    if r.status_code != 200 and r.status_code != 403:
        return []
    post_cookie = 'JSESSIONID=' + r.cookies.get_dict()['JSESSIONID']  # 获取网站cookie
    headers = {
        'Cookie': post_cookie,
        'Referer': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36',
    }
    r = requests.get(url, headers=headers, verify=False)
    pattern1 = re.compile(r'\'\w{14}\'')  # 查找_qt参数第一部分
    pattern2 = re.compile(r'\'\w{29}\'')  # 查找_qt参数第二部分
    data1 = re.findall(pattern1, r.text)[0].replace('\'', '')
    data2 = re.findall(pattern2, r.text)[0].replace('\'', '')
    post_tag = data1 + data2
    # print(post_tag)                                        #获得完整_qt参数
    url = 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?'
    data = {
        'page.currentPage': 1,
        'page.perPageSize': 20,
        'noticeBean.sourceCH': '广西',
        'noticeBean.source': 'GX',
        'noticeBean.title': '',
        'noticeBean.startDate': time.strftime('%Y-%m-%d', time.localtime()),
        'noticeBean.endDate': '',
        '_qt': post_tag,
    }
    headers = {
        'Cookie': post_cookie,
        'Referer': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36',
    }

    r = requests.post(url, data=data, headers=headers, verify=False)
    # print(r)
    bit_list = []
    soup = BeautifulSoup(r.text, 'lxml')
    tag_td = soup.find_all('td')
    tag_td = tag_td[5:-9:]
    for i in tag_td:
        txt = i.find('a')
        if txt:
            if txt.get('title') is None:
                name = txt.text
            else:
                name = txt.get('title')
            bit_list.append(name)
    return bit_list


def main():
    print(cm_new_list())


if __name__ == '__main__':
    main()
