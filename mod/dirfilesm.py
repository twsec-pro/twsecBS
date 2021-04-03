'''
Author: twsec
Date: 2021-03-31 15:34:49
LastEditors: twsec
LastEditTime: 2021-03-31 17:22:10
Description: 
'''
import HackRequests
from  concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import time
import json,os,sys,hashlib,threading,queue
from bs4 import    BeautifulSoup
from urllib.parse import urlparse

def dirfilebp(filename,domain):
    try:
        f = open(filename,encoding='utf8')
        lines = f.readlines()
        i = -1
        for key in lines:
            i=i+1
            key=str(lines[i].strip('\n'))
            url = domain+key
            threads = [20]
            t=threading.Thread(target=bp(url),args=url)
            for ti in threads:
                t.setDaemon(True)
                t.start()
            for ti in threads:
                t.join()      
    except Exception as e:
        print("输入有误，或文件路径找不到，请检查并按格式输入！")
        time.sleep(2)

def bp(url):
    user_agent=UserAgent().random
    header={"User-Agent":user_agent}
    try:
        h = HackRequests.hackRequests()
        res = h.http(url,headers=header)
        if (res.status_code==200):
            print("成功爆破出目录或文件："+url)
    except:
            pass

def bprun():
    filename=input("请输入要爆破的目录文件字典路径：")
    try:
        domain=input("请输入要爆破的url（格式为：http://www.baidu.com或者https://www.baidu.com）：")
        try:
            threads = [20]
            t=threading.Thread(target=dirfilebp(filename,domain),args=(filename,domain))
            for ti in threads:
                t.setDaemon(True)
                t.start()
            for ti in threads:
                t.join() 
        except Exception as e:
            print("程序运行出错！请检查并再次尝试！")
            time.sleep(2)
    except Exception as e:
        print("输入有误，或文件路径找不到，请检查并按格式输入！")
        time.sleep(2)

