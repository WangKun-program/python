# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-09-28 09:43:32
# @Descripttion: 商标信息查询

import time

import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent


def proxy(headers):
    while True:
        proxy_url = 'http://17610040106.v4.dailiyun.com/query.txt?key=NP86444E99&word=&count=1&rand=false&ltime=0&norepeat=false&detail=false'
        response = requests.get(proxy_url, headers=headers)
        proxies = response.text.strip()
        if proxies:
            break
        else:
            time.sleep(15)
    print(proxies)
    return proxies


def getDriver(headers):
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
    options.add_argument(
        '--user-agent={}'.format(generate_user_agent()))
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(proxy(headers)))  # 代理IP
    browser = webdriver.Chrome(options=options, executable_path='C:/Program Files/Google/Chrome/Application/chromedriver.exe')
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
    })
    # with open('stealth.min.js') as f:
    #     js = f.read()
    # browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": js
    # })
    # browser.implicitly_wait(10)

    return browser


def main():
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    value = '华为技术有限公司'
    url = 'http://sbj.cnipa.gov.cn/'
    headers = {
        "User-Agent": generate_user_agent()
    }
    driver = getDriver(headers)
    driver.get(url)
    time.sleep(5)

    move1 = driver.find_element_by_xpath('//div[@class="bscont2 bscont"]/div[@class="bacontinner"]/a')
    ActionChains(driver).move_to_element(move1).click(move1).perform()
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="TRS_Editor"]//img')))

    # Click"我接受"
    move2 = driver.find_element_by_xpath('//div[@class="TRS_Editor"]//img')
    ActionChains(driver).move_to_element(move2).click(move2).perform()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(),"商标综合查询")]')))

    # Click on "商标综合查询"
    move3 = driver.find_element_by_xpath('//p[contains(text(),"商标综合查询")]')
    ActionChains(driver).move_to_element(move3).click(move3).perform()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="submitForm"]//tbody/tr[4]//input')))

    # Positioning input box and input value
    element = driver.find_element_by_xpath('//*[@id="submitForm"]//tbody/tr[4]//input')
    ActionChains(driver).move_to_element(element).click(element).send_keys(value).perform()

    # Click "查询"
    move4 = driver.find_element_by_xpath('//div[@class="bottonbox"]/input[2]')
    ActionChains(driver).move_to_element(move4).click(move4).perform()
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    result = driver.page_source
    print(result)


if __name__ == '__main__':
    main()
