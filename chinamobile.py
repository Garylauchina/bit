import requests

url = 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=2'

data = 'page.currentPage=2&page.perPageSize=20&noticeBean.sourceCH=%E5%B9%BF%E8%A5%BF&noticeBean.source=GX&noticeBean' \
       '.title=&noticeBean.startDate=&noticeBean.endDate=&_qt=jNmBzMQjZ0UjM4EWZ3gzMjhjY0UGMhBTN0YzNxcjZyc '
headers = {
    'Cookie': 'JSESSIONID=604469B9D3B6A65BB4726B28517509E3',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/105.0.0.0 Safari/537.36',
}
r = requests.post(url+data,headers=headers)