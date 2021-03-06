# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-10-19 17:00:02
# @Descripttion: 注册

import json
import random
import re
import string
import time

import pysnooper
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--headless')  # 无界面形式
    options.add_argument('--no-sandbox')  # 取消沙盒模式
    options.add_argument('--disable-setuid-sandbox')
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
    options.add_argument('--user-agent=' + generate_user_agent())
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(get_proxies()))
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """})

    return browser


def get_verification_code(email):
    for i in range(50):
        req = requests.get('https://snapmail.cc/emailList/' + email)
        if req.status_code == 200:
            email_text = json.loads(req.text)[0]['html']
            validation_code = re.search(r'([0-9]{4})', email_text)
            print(validation_code.group(1))
            return validation_code.group(1)

        print("Waiting for next retry")
        time.sleep(6)


def get_proxies():
    ip_url = "http://152.136.208.143:5000/w/ip/random"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    print(proxies['http'])
    return proxies['http']


def create_phone():
    # 第二位数字
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]

    # 第三位数字
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]

    # 最后八位数字
    suffix = random.randint(9999999, 100000000)

    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)


@pysnooper.snoop('./Log/register.log')
def main():
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    userinfo = dict()
    url = 'http://218.77.183.75:81/pubsearch/portal/uiIndex.shtml'
    name_A = string.ascii_uppercase
    name_a = string.ascii_lowercase
    name_n = string.digits
    name_t = '!@#$%^&*'
    driver = getDriver()
    min_num = 51
    max_num = 60
    while min_num <= max_num:
        try:
            time.sleep(5)
            email = 'nuhdi' + str(min_num) + '@snapmail.cc'  # 邮箱
            # email = 'hanne@snapmail.cc'
            username_n = random.randint(4, 19)
            password_n = random.randint(12, 19)
            username_l = []
            password_l = []
            username_n = random.randint(4, 19)
            for i_1 in range(username_n // 2):
                username_l.append(random.choice(string.ascii_letters))
            for i_2 in range(username_n // 2, username_n):
                username_l.append(random.choice(name_n))
            if random.randint(0, 1) == 1:
                index = random.randint(1, len(username_l))
                username_l.insert(index, '_')
            username = ''.join(username_l)  # 用户名

            for j_1 in range(password_n // 4 * 1):
                password_l.append(random.choice(name_A))
            for j_2 in range(password_n // 4 * 1, password_n // 4 * 2):
                password_l.append(random.choice(name_a))
            for j_3 in range(password_n // 4 * 2, password_n // 4 * 3):
                password_l.append(random.choice(name_n))
            for j_4 in range(password_n // 4 * 3, password_n):
                password_l.append(random.choice(name_t))
            password = ''.join(password_l)  # 密码

            driver.get(url)
            WebDriverWait(driver, 15).until(lambda x: x.find_element(By.XPATH, '//*[@id="globleBody"]/div[2]/div[1]/div[3]/div[2]/div[2]/a[2]'))
            driver.find_element(By.XPATH, '//*[@id="globleBody"]/div[2]/div[1]/div[3]/div[2]/div[2]/a[2]').click()  # 点击“注册”
            WebDriverWait(driver, 15).until(lambda x: x.find_element(By.XPATH, '//input[@name="userAccount.account.username"]'))
            driver.find_element(By.XPATH, '//input[@name="userAccount.account.username"]').send_keys(username)  # 用户名
            driver.find_element(By.XPATH, '//input[@name="userAccount.account.password"]').send_keys(password)  # 密码
            driver.find_element(By.XPATH, '//*[@id="recheckPwd"]/label/div[1]/input').send_keys(password)  # 确认密码
            try:
                mes = driver.find_element(By.XPATH, '//*[@id="password"]/label/div[2]/span[2]').get_attributes('textContent')
                if mes:
                    continue
            except AttributeError:
                pass
            driver.find_element(By.XPATH, '//*[@id="email"]/label/div[1]/input').send_keys(email)  # 邮箱
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="emailCode"]/label/div[2]/a').click()  # 点击发送验证码
            num = time.time()
            while True:
                info = driver.find_element(By.XPATH, '//*[@id="emailCode"]/label/div[2]/span[2]').get_attribute('textContent')
                if info == '验证码发送成功':
                    validation_code = get_verification_code(email)  # 获取验证码
                    break
                else:
                    time.sleep(1)
                    if time.time() - num >= 120:
                        driver.find_element(By.XPATH, '//*[@id="emailCode"]/label/div[2]/a').click()  # 点击发送验证码
                    continue

            driver.find_element(By.XPATH, '//*[@id="emailCode"]/label/div[1]/input').send_keys(validation_code)  # 输入验证码
            info = driver.find_element(By.XPATH, '//*[@id="emailCode"]/label/div[2]/span[2]').get_attribute('textContent')
            if info == '邮箱验证码输入错误':
                continue

            driver.find_element(By.XPATH, '//*[@id="mobile"]/label/div[1]/input').send_keys(create_phone())  # 输入随机手机号
            # province_select = ['110000', '120000', '130000', '140000', '150000', '210000', '220000', '230000', '310000', '320000', '330000', '340000', '350000', '360000', '370000', '410000', '420000', '430000', '440000', '450000', '460000', '500000', '510000', '520000', '530000', '540000', '610000', '620000', '630000', '640000', '650000', '710000', ' 810000', '820000']  # 省份value
            # driver.find_element(By.XPATH, '//*[@id="higherArea"]/option[@value="' + random.choice(province_select) + '"]').click()  # 随机点击省份
            driver.implicitly_wait(1)
            count = 2
            sel = []
            while True:
                try:
                    con = driver.find_element(By.XPATH, '//*[@id="province"]/option[' + str(count) + ']').get_attribute('value')
                    sel.append(con)
                    count += 1
                except NoSuchElementException:
                    break

            while True:
                try:
                    driver.find_element(By.XPATH, '//*[@id="province"]/option[@value="' + random.choice(sel) + '"]').click()  # 随机市区
                    break
                except NoSuchElementException:
                    continue
            driver.implicitly_wait(1)
            driver.find_element(By.XPATH, '//*[@id="company_catalog"]/option[@value="' + str(random.randint(1, 13)) + '"]').click()  # 用户类别
            driver.implicitly_wait(1)
            driver.find_element(By.XPATH, '//*[@id="agreement"]/div/p/label/input').click()  # 我已经阅读并同意
            driver.find_element(By.XPATH, '//*[@id="regBtn"]/label/div/a').click()  # 立即注册
            time.sleep(3)
            min_num += 1
            userinfo[username] = password
        except Exception as e:
            print(e)
            continue
    json_data = json.dumps(userinfo)
    with open('./data/海南.json', 'w') as f:
        f.write(json_data)


if __name__ == "__main__":
    main()
