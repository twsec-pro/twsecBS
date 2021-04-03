'''
Author: twsec
Date: 2021-03-30 16:20:51
LastEditors: twsec
LastEditTime: 2021-03-31 17:30:31
Description: 子域名扫描和爆破
'''
import HackRequests
import requests
from  concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import time
import json,os,sys,hashlib,threading,queue
from bs4 import    BeautifulSoup
from urllib.parse import urlparse

def bp(url):
    user_agent=UserAgent().random
    header={"User-Agent":user_agent}
    try:
        h = HackRequests.hackRequests()
        res = h.http(url,headers=header)
        if (res.status_code==200):
            print("成功爆破出子域名："+url)
    except:
            pass

def zymbp(filename,domain):
    try:
        f = open(filename,encoding='utf8')
        lines = f.readlines()
        i = -1
        for key in lines:
            i=i+1
            key=lines[i].strip('\n')
            url = "http://"+key+"."+domain
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

def bprun():
    filename=input("请输入要爆破的子域名字典路径：")
    try:
        domain=input("请输入要爆破的域名（格式为：baidu.com）：")
        try:
            threads = [20]
            t=threading.Thread(target=zymbp(filename,domain),args=(filename,domain))
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

def bing_search(site,pages):
    subdomain=[]
    user_agent=UserAgent().random
    headers={'User-Agent':user_agent,'Accept':'*/*','Accept_Language':'en-US,en;q=0.5','Accept-Encoding':'gzip,deflate','referer':"http://cn.bing.com/search?q=email+site%3abaidu.com&qs=n&sp=-1&pq=emailsite%3abaidu.com&first=2&FORM=PERE1"}
    for i in range(1,int(pages)+1):
        url="https://cn.bing.com/search?q=site%3a"+site+"&go=Search&qs=Search&qs=ds&first="+str((int(i)-1)*10)+"&FORM=PERE"
        conn=requests.session()
        conn.get('http://cn.bing.com',headers=headers)
        html=conn.get(url,stream=True,headers=headers,timeout=8)
        soup=BeautifulSoup(html.content,'html.parser')
        job_bt=soup.findAll('h2')
        for i in job_bt:
            link=i.a.get('href')
            domain=str(urlparse(link).scheme+"://"+urlparse(link).netloc)
            if(domain in subdomain):
                pass
            else:
                subdomain.append(domain)
                print("成功搜索出子域名："+domain)

def runbing():
    try:
        site=input("请输入要查询的域名（格式为：baidu.com）：")
        page=int(input("请输入查询的页数："))
        try:
            bing_search(site,page)
        except Exception as e:
            print("程序运行出错！请检查并再次尝试！")
            time.sleep(2)
    except Exception as e:
        print("输入有误，请检查并按格式输入！")
        time.sleep(2)

def jkxz():
    try:
        a=int(input("请输入序号选择爆破或者搜索方式进行子域名扫描（1.爆破，2.搜索）："))
        if(a==1):
            bprun()
        if(a==2):
            runbing()
    except Exception as e:
        print("输入有误，请检查并按格式输入！")
        time.sleep(2)