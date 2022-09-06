import requests
# 中国电信阳光采购网
url = 'https://caigou.chinatelecom.com.cn/portal/base/announcementJoin/queryList'

headers = {
    'Accept': 'application/json,text/plain,*/*',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '107',
    'Content-Type': 'application/json;charset=UTF-8',
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
    'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/105.0.0.0Safari/537.36',
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
r = requests.post(url, json=data, headers=headers)
bit_list = r.json()['data']['list']
print(len(bit_list))
for i in bit_list:
    for j in ['id', 'searchValue', 'updateBy', 'updateTime', 'remark', 'createBy', 'createTime', 'securityCode',
              'idEncryStr',
              'encryCode', 'encryEditCode', 'encryViewCode', 'endRow', 'pageNum', 'pageSize', 'orderByColumn', 'isSelf',
              'userIdentity', 'isAsc', 'params', 'idEncryStrForFile', 'encryDeleteCode', 'count', 'startRow',
              'isCancel',
              'companyName', 'pageView', 'business_type', 'user_collection', 'provinceCode', 'parProvider',
              'provinceName',
              'function_type']:
        i.pop(j)
    print(i)
print(bit_list)

# soupObj = bs4.BeautifulSoup(obj, features="html.parser")
