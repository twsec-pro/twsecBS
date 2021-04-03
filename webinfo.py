'''
Author: twsec
Date: 2021-03-28 15:08:08
LastEditors: twsec
LastEditTime: 2021-04-03 16:49:31
Description: web 指纹识别和主界面函数
'''
import json,os,sys,hashlib,threading,queue
import requests
import zlib
import urllib3
import time
import sys
import urllib.request
import urllib.error

sys.path.append(r'D:\code\git\twsecBS\mod')
import cdn
import subdomain
import dirfilesm
import portscan

class Downloader(object):
    def get(self,url):
        r = requests.get(url,timeout=10)
        if r.status_code != 200:
            return None
        _str = r.text
        return _str

    def post(self,url,data):
        r = requests.post(url,data)
        _str = r.text
        return _str
    
    def download(self, url,htmls):
        if url is None:
            return None
        _str = {}
        _str["url"] = url
        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return None
            _str["html"] = r.text
        except Exception as e:
            print("error!")
        htmls.append(_str)

class webcms(object):
    workQueue = queue.Queue()
    URL = ""
    threadNum = 0
    NotFound = True
    Downloader = Downloader()
    result = ""

    def __init__(self,url,threadNum = 20):
        self.URL = url
        self.threadNum = threadNum
        filename = os.path.join(sys.path[0], "data", "data.json")
        fp = open(filename,encoding="utf-8")
        webdata = json.load(fp,encoding="utf-8")
        for i in webdata:
            self.workQueue.put(i)
        fp.close()
    
    def getmd5(self, body):
        m2 = hashlib.md5()
        m2.update(body.encode())
        return m2.hexdigest()

    def th_whatweb(self):
        if(self.workQueue.empty()):
            self.NotFound = False
            return False

        if(self.NotFound is False):
            return False
        cms = self.workQueue.get()
        _url = self.URL + cms["url"]
        html = self.Downloader.get(_url)
        print ("[whatweb log]:checking %s"%_url)
        if(html is None):
            return False
        if cms["re"]:
            if(html.find(cms["re"])!=-1):
                self.result = cms["name"]
                self.NotFound = False
                return True
        else: 
            md5 = self.getmd5(html)
            if(md5==cms["md5"]):
                self.result = cms["name"]
                self.NotFound = False
                return True
    
    def run(self):
        while(self.NotFound):
            th = []
            for i in range(self.threadNum):
                t = threading.Thread(target=self.th_whatweb)
                t.start()
                th.append(t)
            for t in th:
                t.join()
        if(self.result):
            print ("[webcms]:%s cms is %s"%(self.URL,self.result))
        else:
            print ("[webcms]:%s cms NOTFound!"%self.URL)


    


def cmso2(domain):
    requests.packages.urllib3.disable_warnings()
    response = requests.get(domain,verify=False)
    #上面的代码可以随意发挥,只要获取到response即可
    #下面的代码您无需改变，直接使用即可
    whatweb_dict = {"url":response.url,"text":response.text,"headers":dict(response.headers)}
    whatweb_dict = json.dumps(whatweb_dict)
    whatweb_dict = whatweb_dict.encode()
    whatweb_dict = zlib.compress(whatweb_dict)
    data = {"info":whatweb_dict}
    res=requests.post("http://whatweb.bugscaner.com/api.go",files=data)
    dic=json.loads(res.text)
    if('CMS' in dic.keys()):
        info=str(dic['CMS'])
        info=info.replace("[","")
        info=info.replace("]","")
        info=info.replace("'","")
        print(domain+"的cms为："+info) 
    else:
        print(domain+"的cms未能识别！")
    return dic
   
def cmsfile(filename):
    f = open(filename)
    lines = f.readlines()
    i = -1
    try:
        for domain in lines:
            i=i+1
            domain=lines[i].strip('\n')
            try:
                urllib.request.urlopen(domain)
                info=str(cmso2(domain))
                print(domain+"解析到的其他信息为："+info)
            except urllib.error.HTTPError: 
                print("域名有误，请检查并按格式输入！")
                time.sleep(2) 
            except urllib.error.URLError: 
                print("域名有误，请检查并按格式输入！")
                time.sleep(2)
            time.sleep(5)    
    except Exception as e:
            print("程序运行出错！请检查并再次尝试！")
            time.sleep(2)





if __name__ == "__main__":
    try:
        demo=input("请选择功能模块a.cms识别，b.cdn判断，c.子域名扫描，d.敏感目录文件扫描，e.端口扫描服务探测（输入序号即可）：")
        if(demo=="a"):
            try:
                test = int(input("输入数字1进行单个url解析cms，输入数字2进行文件批量解析cms："))
                if(test==1):
                    try:
                        domain = input("输入要检测web指纹的url（注意不带路径如https://www.baidu.com）：")
                        try:
                            urllib.request.urlopen(domain)
                            print("开始调用本地接口检测"+domain+"的cms！")
                            webcms=webcms(domain)
                            webcms.run()
                            print("开始调用网络接口检测"+domain+"的cms！")
                            info=str(cmso2(domain))
                            print(domain+"解析到的其他信息为："+info)
                        except urllib.error.HTTPError: 
                            print("域名有误，请检查并按格式输入！")
                            time.sleep(2) 
                        except urllib.error.URLError: 
                            print("域名有误，请检查并按格式输入！")
                            time.sleep(2) 
                    except Exception as e:
                        print("程序运行出错！请检查并再次尝试！")
                        time.sleep(2)
                if(test==2):
                    threads = [20]
                    filename = input("请输入要解析的url文件路径：")
                    try:
                        t=threading.Thread(target=cmsfile(filename),args=filename)
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
        elif(demo=="b"):
            cdn.run()
        elif(demo=="c"): 
            subdomain.jkxz()
        elif(demo=="d"):
            dirfilesm.bprun()
        elif(demo=="e"):
            portscan.port()
        else:
            print("输入出错，请重试！")
            time.sleep(2)     
    except Exception as e:
            print("程序运行出错！请检查并再次尝试！")
            time.sleep(2)
