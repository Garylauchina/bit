import time

import requests
import json

argu1 = 'client_credential'
argu2 = 'wx7bd1096d014dc5c4'
argu3 = '6bf950052b38e94da3259b5a4bc11e12'
base_url = 'https://api.weixin.qq.com/cgi-bin'
test_id = 'o-4JI0qhR7p3irhZCY2eGKtLar2E'  # 刘刚的openid

def all_user(get_token):
    get_id_url = '/user/get?access_token=%s&next_openid'
    a = requests.get(base_url + get_id_url % get_token).json()['data']['openid']
#    print('总共%s名用户' % a.json()['total'])
    print(a)
#    a = a.json()['data']
#    for n in range(len(a)):
#        id_info = requests.get(base_url + id_info_url % (access_token, a[n]))
    #        print(id_info.json())
    return a

def Access_Token():
    token_url = '/token?grant_type=%s&appid=%s&secret=%s' % (argu1, argu2, argu3)
#
#    id_info_url = '/user/info?access_token=%s&openid=%s&lang=zh_CN'
    a = requests.get(base_url + token_url).json()
    print('获取token成功：' + a['access_token'])
    print('有效期：'+str(a['expires_in'])+'秒')
    return a['access_token']


def sunshine_list(pagenum):
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
        'pageNum': pagenum,
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
                  'encryCode', 'encryEditCode', 'encryViewCode', 'endRow', 'pageNum', 'pageSize', 'orderByColumn',
                  'isSelf',
                  'userIdentity', 'isAsc', 'params', 'idEncryStrForFile', 'encryDeleteCode', 'count', 'startRow',
                  'isCancel',
                  'companyName', 'pageView', 'business_type', 'user_collection', 'provinceCode', 'parProvider',
                  'provinceName',
                  'function_type']:
            i.pop(j)
    return bit_list


def cm_list():
    url = 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=2'
    headers = {
        'Accept': '*/*',
        'Accept - Encoding': 'gzip,deflate,br',
        'Accept - Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content - Length': '206',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': 'JSESSIONID=DDC0DAFF5B7A06BA1B807A2A2A1F33F3',
        'Host': 'b2b.10086.cn',
        'Origin': 'https://b2b.10086.cn',
        'Referer': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2',
        'sec-ch-ua': '"GoogleChrome";v="105","Not)A;Brand";v="8","Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User - Agent': 'Mozilla / 5.0(Macintosh;Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 105.0.0.0 Safari / 537.36',
        'X - Requested - With': 'XMLHttpRequest',
    }
    data = {
        'page.currentPage': '1',
        'page.perPageSize': '20',
        'noticeBean.sourceCH': '广西',
        'noticeBean.source': 'GX',
        'noticeBean.title': '',
        'noticeBean.startDate': '',
        'noticeBean.endDate': '',
        '_qt': 'zNmhTMITY3UzMlZDNklTY1I2NkBTOllTOhVGZ3IWOld',
    }
    r = requests.post(url, json=data, headers=headers)
    return r


# 向微信公众号发送消息
def send_msg(get_message, get_user,get_token):
    send_url = '/message/custom/send?access_token=%s'
    content = {
        'content': get_message
    }
    msg_pkg = {'touser': get_user, 'msgtype': 'text', 'text': content}
    r = requests.post(base_url + send_url % get_token, json.dumps(msg_pkg, ensure_ascii=False).encode('utf-8'))
    #    id_info = requests.get(base_url + id_info_url % (get_token, get_user[n]))
    if r.json()['errcode'] != 0:
        print('发送失败')
        print(r.json()['errmsg'])
    else:
        print('发送成功，请查收！')
    return

'''
def send_sunshine(page,get_id):
    get_list = sunshine_list(page)  # 获取第一页，字典格式
    send_list = []
    for i in get_list:
        send_list.append(i['docTitle'] + '\n' + i['docType'])
    for i in send_list:
        print(i)
        send_msg(i, get_id)
    return
'''