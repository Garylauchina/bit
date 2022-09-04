from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(5)

bitlist = ''
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
        if checkdate == today or checkdate == today-1 or checkdate == today - 2:
            todaycount = todaycount + 1
            bitlist = bitlist +checkitem[2] + '\n'
#            print(checkdate)
        else:
            forceend = True
            break
    if forceend:
        break
    else:
        next_page.click()
        time.sleep(1)
        next_page = driver.find_element(By.XPATH, '/html/body/form/div/div[1]/div[2]/table[4]/tbody/tr/td[10]/a[1]/img')

print('近三日共有%s条招标信息' % todaycount)
print(bitlist)

