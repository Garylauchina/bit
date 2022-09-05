import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

argu1 = 'client_credential'
argu2 = 'wx7bd1096d014dc5c4'
argu3 = '6bf950052b38e94da3259b5a4bc11e12'
base_url = 'https://api.weixin.qq.com/cgi-bin'
token_url = '/token?grant_type=%s&appid=%s&secret=%s' % (argu1, argu2, argu3)
get_id_url = '/user/get?access_token=%s&next_openid'
id_info_url = '/user/info?access_token=%s&openid=%s&lang=zh_CN'
send_url = '/message/custom/send?access_token=%s'
access_token = requests.get(base_url + token_url).json()['access_token']
print(access_token)


# 获取用户ID
def all_user():
    a = requests.get(base_url + get_id_url % access_token)
    print('总共%s名用户' % a.json()['total'])
    print(a.json())
    a = a.json()['data']['openid']
    for n in range(len(a)):
        id_info = requests.get(base_url + id_info_url % (access_token, a[n]))
    #        print(id_info.json())
    return a


# 定义一个函数"send_msg"，用来向公众号用户群发一条消息
def send_msg(get_message, get_user):
    content = {
        'content': get_message
    }
    msg_pkg = {'touser': get_user, 'msgtype': 'text', 'text': content}
    r = requests.post(base_url + send_url % access_token, json.dumps(msg_pkg, ensure_ascii=False).encode('utf-8'))
    #    id_info = requests.get(base_url + id_info_url % (access_token, get_user[n]))
    if r.json()['errcode'] != 0:
        print('发送失败')
        print(r.json()['errmsg'])
    else:
        print('发送成功，请查收！')
    return


# 定义一个函数get_bitlist，获得近三天的招标信息(list)
def get_bitlist():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chromedriver = "/usr/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)

    bitlist = []
    encrycode = []
    type_id = []
    danyilaiyuan_url = "https://caigou.chinatelecom.com.cn/MSS-PORTAL/purchaseannouncebasic/viewHome.do?encryCode=%s&noticeType=0&id=%s"
    todaycount = 0
    forceend = False
    today = int(time.strftime('%Y%m%d', time.localtime()))
    print('今天日期：%s' % today)
    driver.get('https://caigou.chinatelecom.com.cn/MSS-PORTAL/announcementjoin/list.do?provinceJT=NJT')
    driver.find_element(By.CLASS_NAME, 'special_select').click()  # 点击省份框
    time.sleep(1)
    print('请稍等。。。点击省份')
    driver.find_element(By.XPATH, "//span[text()='广西']").click()  # 点击广西
    time.sleep(1)
    print("选择广西")
    driver.find_element(By.XPATH, "//input[@class='btn1']").click()  # 点击查询
    time.sleep(1)
    next_page = driver.find_element(By.XPATH, '/html/body/form/div/div[1]/div[2]/table[4]/tbody/tr/td[10]/a[1]/img')
    while next_page.is_enabled():
        bit_name = []
        bit_crdate = []
        hyperlink = []
        #获取标签中的onlick值，用来生成链接
        for i in range(0,10):
            bit_name.append(driver.find_element(By.CSS_SELECTOR,'table.table_data > tbody > tr:nth-child(%s) > td:nth-child(3) > a'%(i+2)).text)
            bit_crdate.append(driver.find_element(By.CSS_SELECTOR,'table.table_data > tbody > tr:nth-child(%s) > td:nth-child(6)'%(i+2)).text)
        #用正则表达式提取里面的encryCode和id，位于view后面的第三和第一个括号内
#            html_tag =
            hyperlink.append(driver.find_element(By.CSS_SELECTOR,'table.table_data > tbody > tr:nth-child(%s) > td:nth-child(3) > a'%(i+2)).get_attribute('onclick'))
        #提取pageitem中的每一个元素，单独包装为一个list
        for i in range(len(bit_crdate)):
            hyperlink[i] = hyperlink[i][4:].replace('(','').replace(')','').replace('\'','')
            encrycode.append(hyperlink[i].split(',')[2])
            type_id.append(hyperlink[i].split(',')[0])
            checkdate = int(bit_crdate[i].replace('-','')[0:8])
            if checkdate == today or checkdate == today - 1 or checkdate == today - 2:
                todaycount = todaycount + 1
                bitlist.append(bit_name[i]+danyilaiyuan_url%(encrycode[i],type_id[i]))
            else:
                forceend = True
                break
        if forceend:
            break
        else:
            next_page.click()
            time.sleep(1)
            next_page = driver.find_element(By.XPATH,
                                            '/html/body/form/div/div[1]/div[2]/table[4]/tbody/tr/td[10]/a[1]/img')
    bitlist.append('广西电信近三日共有%s条招标信息' % todaycount)
    driver.quit()
    return bitlist  # 返回一个list


# 获取素材库中的一个素材id
def image_id():
    getimg_url = '/material/batchget_material?access_token=%s'
    files = {"type": "image", "offset": 0, "count": 1}
    r = requests.post(base_url + getimg_url % access_token, json.dumps(files, ensure_ascii=False).encode("utf-8"))
    return r


# 将草稿箱清空，并将获取的信息放入第一份草稿中
def pack_info(get_info, get_img):
    count_url = '/draft/count?access_token=%s'
    pack_url = '/draft/add?access_token=%s'
    title = time.strftime('%Y-%m-%d', time.localtime()) + '招标列表'
    data = {
        "articles": [{
            "title": title,
            "author": "刘刚",
            "content": get_info,
            "content_source_url": "",
            "need_open_comment": 0,
            "only_fans_can_comment": 0,
            "digest": "",
            "thumb_media_id": get_img
        }]
    }
    post_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    r = requests.post(base_url + pack_url % access_token, data=post_data)
    return r


# 将草稿箱的一份文档发送至公众号
def send_draft(get_media_id):
    send_draft_url = '/freepublish/submit?access_token=%s'
    media_id = {"media_id": get_media_id}
    r = requests.post(base_url + send_draft_url % access_token,
                      json.dumps(media_id, ensure_ascii=False).encode('utf-8'))
    return r


# 获得草稿箱中第一份文档的id
def get_draft_id():
    get_draft_url = '/draft/batchget?access_token=%s'
    files = {"offset": 0, "count": 1, "no_content": 1}
    r = requests.post(base_url + get_draft_url % access_token, json.dumps(files, ensure_ascii=False).encode('utf-8'))
    return r


# 重新采用send_message方法！
# 第一步：获取招标信息
aa = get_bitlist()
print(aa)
print(len(aa))

# 第二步：每次最多发送10条，然后要求用户回复
test_id = 'o-4JI0ibLP9genCK8KVGz_KKkWWE' #刘刚的openid
if len(aa) >= 9:
    total = 10
else:
    total = len(aa)
for i in range(total):
    send_msg(aa[0], test_id)
    aa.pop(0)
if len(aa) == 0:
    print('已全部发送')
    send_msg('已全部发送', test_id)
else:
    print('还有%s条信息未发送' % len(aa))
    send_msg('还有%s条信息未发送' % len(aa), test_id)



#以下是通过草稿箱群发的代码，已弃用！
# bb = all_user()[0]
# print(bb)
# send_msg("这还是一个测试",bb)

'''
# 第二步：打包消息发送到草稿箱中
ss = pack_info(aa.replace('\n','<br>'), image_id().json()['item'][0]['media_id'])
print(ss.json())

# 第三部：获得草稿箱中第一份文档id，并发送至公众号
bb = get_draft_id().json()['item'][0]['media_id']
print(bb)
cc = send_draft(bb)
print(cc.json())
#
# send_msg(bitlist,all_user())
# print('近三日共有%s条招标信息' % len(bitlist))
# send_msg('近三日共有%s条招标信息' % len(bitlist))
#
# print(aa)
# bb = send_draft(aa)
# print(bb.json())
'''
