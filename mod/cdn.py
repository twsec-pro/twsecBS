'''
Author: twsec
Date: 2021-03-22 16:25:38
LastEditors: twsec
LastEditTime: 2021-04-03 17:12:17
Description: 判断是否存在CDN防护
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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
 
def getipo1(domain):
    ip_list=[]
    flag1 = 0
    ipaddr = socket.getaddrinfo(domain,None)
    for item in ipaddr:
        if item[4][0] not in ip_list:
            ip_list.append(item[4][0])
            flag1 = flag1+1
    return flag1,ip_list

def getipo2(domain):
    flag2 = 0
    pi = subprocess.Popen('nslookup {}'.format(domain), shell=True, stdout=subprocess.PIPE)
    out = pi.stdout.read().decode('gbk')  # 编码根据实际结果调整
    # 判断返回值中是否有 Addresses 字段，且该字段下 ip 地址要大于等于 2 个，即说明使用了 CDN
    strs = re.findall(r'Addresses:(\s*(((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\s*)*)', out, re.S)
    if strs == []:
        return flag2
    else:
        l = strs[0][0].split('\r\n\t')
        for address in l:
            flag2 = flag2+1
        return flag2

def getipo3(domain):
    flag3 = 0
    url = 'http://cdn.chinaz.com/search/?host='+domain
    strhtml = requests.get(url) 
    soup = BeautifulSoup(strhtml.text,'lxml')
    #a = soup.find_all(text=(re.compile("可能使用CDN云加速")))
    b = soup.find_all(text=(re.compile("不属于CDN云加速")))
    if(b==[]):
        flag3=flag3+1
        return flag3
    if(b!=[]):
        return flag3

def getipo4(domain):
    flag4 = 0
    info = "未知"
    url = 'http://tools.bugscaner.com/api/whichcdn/'
    payload = {'url':domain}
    res = requests.post(url,data=payload)
    content = json.loads(res.text)
    if(str(content['secess'])=="True"):
        flag4 = flag4+1
        info=content['info']
        return flag4,info
    if(str(content['secess'])=="False"):
        return flag4,info

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
    #print(res.text)
    soup=BeautifulSoup(res.text,'lxml')
    data = soup.find_all('td')
    #print(data)
    
    a=soup.find_all(text=(re.compile("未知")))
    
    if(a!=[]):
        return flag5,info
    else:
        for item in data:
            info1 = item.find('a')
        info=info1.text
        #print(info)
        flag5=flag5+1
        return flag5,info

def cdno(domain):
    key = 0
    flag = 0
    
    url = "http://"+domain
    try : 
        urllib.request.urlopen(url) 
        try:
            flag,ip_list=getipo1(domain)
            if(flag>1):
                key=key+1
            flag=getipo2(domain)
            if(flag>0):
                key=key+1
            flag=getipo3(domain)
            if(flag>0):
                key=key+1
            flag,info1=getipo4(domain)
            if(flag>0):
                key=key+1
            flag,info2=getipo5(domain)
            if(flag>0):
                key=key+1
            
            if(key>=3):
                
                if(info2!="未知"):
                    print(domain+"存在CDN防护，且CDN服务商为"+info2+"!")
                    print(domain+"解析出的ip地址为：")
                    print(ip_list)
                if(info2=="未知"):
                    if(info1!="未知"):
                        print(domain+"存在CDN防护，且"+info1+"!")
                        print(domain+"解析出的ip地址为：")
                        print(ip_list)
                if(info2=="未知"):
                    if(info1=="未知"):
                        print(domain+"存在CDN防护，CDN服务商未知！")
                        print(domain+"解析出的ip地址为：")
                        print(ip_list)
            else:
                print(domain+"不存在CDN防护！")
                print(domain+"解析出的ip地址为：")
                print(ip_list)
        except Exception as e:
            print("程序运行出错！请检查并再次尝试！")
            time.sleep(2)
    except urllib.error.HTTPError: 
        print("域名有误，请检查并按格式输入！")
        time.sleep(2) 
    except urllib.error.URLError: 
        print("域名有误，请检查并按格式输入！")
        time.sleep(2)
     

def cdnfile(filename):
    f = open(filename)
    lines = f.readlines()
    i = -1
    try:
        for domain in lines:
            i=i+1
            domain=lines[i].strip('\n')
            cdno(domain)     
    except Exception as e:
            print("程序运行出错！请检查并再次尝试！")
            time.sleep(2)


def run():
    try:
        test = int(input("输入数字1进行单个域名解析CDN，输入数字2进行文件批量解析CDN："))
        if(test==1):
            domain = input("请输入要解析的单个域名（baidu.com或*.baidu.com）：")
            try:
                cdno(domain)
            except Exception as e:
                print("输入有误，请检查并按格式输入！")
                time.sleep(2)
        if(test==2):
            threads = [20]
            filename = input("请输入要解析的域名文件路径：")
            try:
                t=threading.Thread(target=cdnfile(filename),args=filename)
                for ti in threads:
                    t.setDaemon(True)
                    t.start()
                for ti in threads:
                    t.join()
            except Exception as e:
                print("输入有误，或文件路径找不到，请检查并按格式输入！")
                time.sleep(2)  
    except Exception as e:
        print("输入有误，请检查并按格式输入！")
        time.sleep(2) 
'''  
domain=input()
flag=cdno(domain) 
print(flag) 
'''