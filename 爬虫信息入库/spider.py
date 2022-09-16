import re
import requests
from bs4 import BeautifulSoup


class Spider:
    def __init__(self, name):
        self.name = name
        print('构建%s列表' % name)

    def all_list(self):
        if self.name == 'ct':
            query_url = 'https://caigou.chinatelecom.com.cn/portal/base/announcementJoin/queryList'
            headers = {
                'Accept': 'application/json,text/plain,*/*',
                'Accept-Encoding': 'gzip,deflate,br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Length': '107',
                'Content-Type': 'application/json;charset=UTF-8',
                'Cookie': 'Secure;Secure;Secure=',
                'Host': 'caigou.chinatelecom.com.cn',
                'Origin': 'https://caigou.chinatelecom.com.cn',
                'Pragma': 'no-cache',
                'Referer': 'https://caigou.chinatelecom.com.cn/ctsc-portal/search?search=',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/105.0.0.0Safari/537.36',
                'sec-ch-ua': '"GoogleChrome";v="105","Not)A;Brand";v="8","Chromium";v="105"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
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
            r = requests.post(query_url, json=data, headers=headers)
            if r.status_code != 200:
                return [r.status_code]
            r = r.json()
            return r
        elif self.name == 'cm':
            requests.packages.urllib3.disable_warnings()
            url = 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2'
            r = requests.get(url, verify=False)
            print(r.status_code)
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
            print(post_tag)                                        #获得完整_qt参数
            url = 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?'
            data = {
                'page.currentPage': 1,
                'page.perPageSize': 20,
                'noticeBean.sourceCH': '广西',
                'noticeBean.source': 'GX',
                'noticeBean.title': '',
                'noticeBean.startDate': '',
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
    spider1 = Spider('ct')
    print(spider1.all_list())
    spider2 = Spider('cm')
    print(spider2.all_list())


if __name__ == '__main__':
    main()
