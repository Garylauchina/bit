import pprint

import requests
import time

from bs4 import BeautifulSoup


def sunshine_list():
    # 中国电信阳光采购网
    url = 'https://caigou.chinatelecom.com.cn/portal/base/announcementJoin/queryList'
    bit_list = []
    headers = {
        # 'Accept': 'application/json,text/plain,*/*',
        # 'Accept-Encoding': 'gzip,deflate,br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '107',
        # 'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'Secure;Secure;CaiGouServiceInfo=!OMtbDA1sN2Py46c1qhgwHmp4DxKAGFH+DKDyAO7lgQKpNe9HwoMbDwU/c/+2+6foSh7UiZwftGPZv/8=;JSESSIONID=0000tGpQLjAkIEtrEg9v2AVqXEq:18djc0l04;Secure=',
        'Host': 'caigou.chinatelecom.com.cn',
        'Origin': 'https://caigou.chinatelecom.com.cn',
        'Referer': 'https://caigou.chinatelecom.com.cn/ctsc-portal/search?search=',
        'sec-ch-ua': '"GoogleChrome";v="105","Not)A;Brand";v="8","Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
#        'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/105.0.0.0Safari/537.36',
    }
    data = {"pageNum": 1, "pageSize": 10, "type": "0", "title": "", "queryStartTime": "", "provinceCode": "10"}
    # data = {
    #     'pageNum': 1,
    #     'pageSize': 20,
    #     'provinceCode': "",
    #     'queryEndTime': "",
    #     'queryStartTime': "2022-09-08T16:00:00.000Z",
    #     'title': "",
    #     'type': "0"
    # }
    r = requests.post(url, json=data, headers=headers).json()
    r = r.json()
    # totalpage = r['navigatepageNums']
    # print(totalpage)
#    pprint.pprint(r)
#     for i in r:
#         bit_list.append(r['list'])
#       else:
 #           data['pageNum'] = data['pageNum'] + 1
    return bit_list

def oldsunshine_list():
    url='https://caigou.chinatelecom.com.cn/MSS-PORTAL/announcementjoin/list.do?provinceJT=NJT'
    headers={
        'Cookie':'name=value;Secure=;CaiGouServiceInfo=!BAC4o4Do7flQiFU1qhgwHmp4DxKAGGtR0Y9bHWOnTBp0a6s4cw2FU3TSIpVZQ3PwmD2bMJXrhb+rL7c=;JSESSIONID=0000ESC-Qg6jaAHt_Lw8uEYiw3T:18djc0j4k',
        'Host':'caigou.chinatelecom.com.cn',
        'Origin':'https://caigou.chinatelecom.com.cn',
        'Pragma':'no-cache',
        'Referer':'https://caigou.chinatelecom.com.cn/MSS-PORTAL/announcementjoin/list.do?provinceJT=NJT',
        'Sec-Fetch-Dest':'document',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-User':'?1',
        'Upgrade-Insecure-Requests':'1',
        }
    data = {
    'provinceJT':'NJT',
    'docTitle':'',
    'docCode':'',
    'provinceCode':'10',
    'provinceNames':'广西',
    'startDate':'',
    'endDate':'',
    'docType':'',
    'paging.start':'1',
    'paging.pageSize':'10',
    'pageNum':'10',
    'goPageNum':'1',
    }
    r = requests.post(url,data=data,headers=headers).text
    soup = BeautifulSoup(r,'html.parser')
    soup.prettify()
    td = soup.select('td')
    print(type(td))
    for text in td :
        print(text.text)
#    print(td)
    return
oldsunshine_list()
# l=sunshine_list()
# pprint.pprint(l)
# print((len(l)))