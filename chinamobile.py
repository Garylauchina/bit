import requests
from bs4 import BeautifulSoup


def cm_new_list():
    requests.packages.urllib3.disable_warnings()
    url = 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?'
    data = {
        'page.currentPage': 1,
        'page.perPageSize': 20,
        'noticeBean.sourceCH': '广西',
        'noticeBean.source': 'GX',
        'noticeBean.title': '',
        'noticeBean.startDate': '',
        'noticeBean.endDate': '',
        '_qt': 'TNjZ2YgjM5UzMykzMiNmMmNjNiFDNyEzN1E2M3MWOhl',
    }
    headers = {
        'Cookie': 'JSESSIONID=9F1AFB46747F7A7C7F18AF387ED32B5C',
        'Referer': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36',
    }

    r = requests.post(url, data=data, headers=headers, verify=False)
    soup = BeautifulSoup(r.text, 'lxml')
    td = soup.find_all('td')
    all_list = []
    for i in td:
        # print(i)
        try:
            k = i.a.text
            all_list.append(k)
        except:
            pass
    del all_list[-4:]
    return all_list

#print(cm_new_list())

