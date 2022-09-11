import requests
from bs4 import BeautifulSoup
def cm_list():
    requests.packages.urllib3.disable_warnings()
    url = 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?'

    data = {
        'page.currentPage': 1,
        'page.perPageSize': 10,
        'noticeBean.sourceCH': '广西',
        'noticeBean.source': 'GX',
        'noticeBean.title': '',
        'noticeBean.startDate': '',
        'noticeBean.endDate': '',
        '_qt': 'TOyYDZY2NiFzM3kDO2EmY4QWMmJjZlhTMmZjYmN2Nxg',
    }
    data2 = '&page.currentPage=1&page.perPageSize=20&noticeBean.sourceCH=%E5%B9%BF%E8%A5%BF&noticeBean.source=GX' \
            '&noticeBean.title=%E5%B9%BF%E8%A5%BF&noticeBean.startDate=&noticeBean.endDate=&_qt' \
            '=TOyYDZY2NiFzM3kDO2EmY4QWMmJjZlhTMmZjYmN2Nxg '
    datajs = {
        'Accept-Ranges': 'bytes',
        'Connection': 'Keep-alive',
        'Content-Length': 97113,
        'Content-Type': 'application/javascript',
        'Date': 'Sun, 11 Sep 2022 03:42:35 GMT',
        'ETag': 'W/"97113-1658159809000"',
        'Last-Modified': 'Mon, 18 Jul 2022 15:56:49 GMT',
        'Server': '*****',
        'Via': '1.1 ID-0002262061156206 uproxy-14',
    }
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '224',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=05A134C55F9D2B9EE36B7D7B286CFF2A',
        'Host': 'b2b.10086.cn',
        'Origin': 'https://b2b.10086.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    r = requests.post(url, data=data, headers=headers,verify=False)
    soup = BeautifulSoup(r.text, 'lxml')
    td = soup.find_all('td')
    all_list = []
    for i in td:
        #    print(i)
        try:
            k = i.a.text
            all_list.append(k)
        except:
            pass
    del all_list[-4:]
    return all_list


