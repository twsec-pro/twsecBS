'''
Author: twsec
Date: 2021-03-25 13:44:54
LastEditors: twsec
LastEditTime: 2021-04-03 17:13:52
Description: 测试代码
'''
import socket
import re
import subprocess
from bs4 import    BeautifulSoup
import requests        
import json
import urllib.request
import urllib.error
import time
import threading
from fake_useragent import UserAgent
import zlib
import urllib3
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse

import sys
import nmap
def getipo5(domain):
    flag5 = 0
    info="未知"
    browser=webdriver.PhantomJS(executable_path=r'D:\GeckoDriver\phantomjs-2.1.1-windows\bin\phantomjs.exe') 
    url = 'https://tools.ipip.net/cdn.php'
    browser.get(url)
    #Cookie = browser.get_cookies()
    #browser.close()
    #strr = ''
    #for c in Cookie:
        #strr += c['name']
        #strr += '='
        #strr += c['value']
        #strr += ';'
    cookie="LOVEAPP_SESSID=7d38b6d7a191b9a3ccf6365289fa50349882534a; __jsluid_s=ca82ab541faabfdea5f5ef674f3e237a; _ga=GA1.2.671769493.1617350155; _gid=GA1.2.268809088.1617350155; Hm_lvt_6b4a9140aed51e46402f36e099e37baf=1617350155; login_r=https%253A%252F%252Ftools.ipip.net%252F;"
    payload = {'node':663,'host':domain}
    user_agent=UserAgent().random
    headers={"User-Agent":user_agent,"Cookie":cookie}
    res = requests.post(url,data=payload,headers=headers)
    print(res.text)
domain=input()
getipo5(domain)