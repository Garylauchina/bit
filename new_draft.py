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
        print(id_info.json())
    return a


# 定义一个函数"send_msg"，用来向公众号用户群发一条消息
def send_msg(get_message, get_user):
    content = {
        'content': get_message
    }
    msg_pkg = {}
    for n in range(len(get_user)):
        msg_pkg['touser'] = get_user[n]
        msg_pkg['msgtype'] = 'text'
        msg_pkg['text'] = content
        r = requests.post(base_url + send_url % access_token, json.dumps(msg_pkg, ensure_ascii=False).encode('utf-8'))
        id_info = requests.get(base_url + id_info_url % (access_token, get_user[n]))
        if r.json()['errcode'] != 0:
            print('第%s个用户%s发送失败' % ((n + 1), id_info.json()['remark']))
            print(r.json()['errmsg'])
        else:
            print('第%s个用户%s发送成功，请查收！' % ((n + 1), id_info.json()['remark']))
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
        divs = driver.find_elements(By.CLASS_NAME, 'table_data')  # 获取当前页面数据
        pageitem = divs[0].text.split('\n')  # 切分存入列表
        pageitem.pop(0)
        for i in pageitem:
            checkitem = i.split(' ')
            try:
                checkdate = int(checkitem[5].replace('-', ''))
            except ValueError:
                checkdate = int(checkitem[6].replace('-', ''))
            if checkdate == today or checkdate == today - 1 or checkdate == today - 2:
                todaycount = todaycount + 1
                bitlist.append(checkitem[2])
            #            print(checkdate)
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
    return bitlist


# 获取素材库中的一个素材id
def image_id():
    getimg_url = '/material/batchget_material?access_token=%s'
    files = {"type": "image", "offset": 0, "count": 1}
    r = requests.post(base_url + getimg_url % access_token, json.dumps(files, ensure_ascii=False).encode("utf-8"))
    return r


# 将获取的信息打包到一个草稿中
def pack_info(get_info, get_img):
    pack_url = '/draft/add?access_token=%s'
    title = time.strftime('%Y-%m-%d', time.localtime()) + '招标列表'
    data = {
        "articles": [{
            "title": title,
            "author": "tyzh",
            "content": get_info,
            "content_source_url": "",
            "need_open_comment": 0,
            "only_fans_can_comment": 0,
            "digest": "",
            "thumb_media_id": get_img
        }]
    }
    post_data = json.dumps(data,ensure_ascii=False).encode('utf-8')
    r = requests.post(base_url + pack_url % access_token, data=post_data)
    return r

aa ='还是测试\n测试了一遍又一遍\n快点给个好评\n'
ss = pack_info(aa, image_id().json()['item'][0]['media_id'])
print(ss.json())
# print(image_id().json())
# bitlist = get_bitlist()
# print(bitlist)
# send_msg(bitlist,all_user())
# print('近三日共有%s条招标信息' % len(bitlist))
# send_msg('近三日共有%s条招标信息' % len(bitlist))
