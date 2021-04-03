'''
Author: twsec
Date: 2021-04-01 16:06:57
LastEditors: twsec
LastEditTime: 2021-04-03 17:08:49
Description: 端口扫描与服务探测
'''

import threading,time
from socket import *
import queue
import sys
import nmap
import re
import socket


setdefaulttimeout(1)  # 设置整个 socket 层的超时时间，即某端口 1 秒内未连接成功则跳过
SIGNS = (
    # 协议 | 版本 | 关键字
    b'FTP|FTP|^220.*FTP',
    b'MySQL|MySQL|mysql_native_password',
    b'oracle-https|^220- ora',
    b'Telnet|Telnet|Telnet',
    b'Telnet|Telnet|^\r\n%connection closed by remote host!\x00$',
    b'VNC|VNC|^RFB',
    b'IMAP|IMAP|^\* OK.*?IMAP',
    b'POP|POP|^\+OK.*?',
    b'SMTP|SMTP|^220.*?SMTP',
    b'Kangle|Kangle|HTTP.*kangle',
    b'SMTP|SMTP|^554 SMTP',
    b'SSH|SSH|^SSH-',
    b'HTTPS|HTTPS|Location: https',
    b'HTTP|HTTP|HTTP/1.1',
    b'HTTP|HTTP|HTTP/1.0',
)


def sorun(queue_s,ip):
    while not queue_s.empty():
        try:
            port = queue_s.get()
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((ip, port))
            print('[+] %d is open' % port)
        except:
            pass

def somain(ip,spo,epo):
    threads = []
    threads_count = 100       # 线程数，默认 100
    queue_s = queue.Queue()
    #ip=ip
    try:
        for i in range(spo,epo+1):  # 默认扫描1-1000的端口，可以手动修改这里的端口范围
            queue_s.put(i)     # 使用 queue.Queue().put() 方法将端口添加到队列中
        for i in range(threads_count):
            threads.append(sorun(queue_s,ip))  # 扫描的端口依次添加到线程组
        for i in threads:
            i.start()
        for i in threads:
            i.join()
    except:
            pass
def nmscan(hosts,port):
    nm = nmap.PortScanner() 
    nm.scan(hosts=hosts, arguments=' -v -sS -p '+port) 
    try:
        for host in nm.all_hosts():     
            print('----------------------------------------------------')    #输出主机及主机名    
            print('Host : %s (%s)' % (host, nm[host].hostname()))     #输出主机状态，如up、down    
            print('State : %s' % nm[host].state())
            for proto in nm[host].all_protocols():         #遍历扫描协议，如tcp、udp        
                print('----------')        #输入协议名        
                print('Protocol : %s' % proto)         #获取协议的所有扫描端口        
                lport = nm[host][proto].keys()        #端口列表排序        
                list(lport).sort()        #遍历端口及输出端口与状态 
                for port in lport:             
                    print('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))
    except:
            pass

def regex(response, port):
    text = ""
    if re.search(b'<title>502 Bad Gateway', response):
        proto = {"Service failed to access!!"}
    for pattern in SIGNS:
        pattern = pattern.split(b'|')
        if re.search(pattern[-1], response, re.IGNORECASE):
            proto = "["+port+"]" + " open " + pattern[1].decode()
            break
        else:
            proto = "["+port+"]" + " open " + "Unrecognized"
    print(proto)

def request(ip,port):
    response = ''
    PROBE = 'GET / HTTP/1.0\r\n\r\n'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    result = sock.connect_ex((ip, int(port)))
    if result == 0:
        try:
            sock.sendall(PROBE.encode())
            response = sock.recv(256)
            if response:
                regex(response, port)
        except ConnectionResetError:
            pass
    else:
        pass
    sock.close()

def fwmain(ip,port):
    print("Scan report for "+ip+"\n")
    for line in port.split(','):
        request(ip,line)
        time.sleep(0.2)
    print("\nScan finished!....\n")

def port():
    try:
        test=int(input("请选择扫描端口的方法1.socket模块，2.nmap模块（输入序号即可）3.服务识别："))
        try:
            if(test==1):
                ip=input("请输入要扫描的ip（192.168.1.1）：")
                spo=int(input("请输入要扫描的开始端口："))
                epo=int(input("请输入要扫描的结束端口："))
                print("开始扫描：")
                somain(ip,spo,epo)
        except Exception as e:
            print("输入有误，请检查并按格式输入！")
            time.sleep(2) 
        try:
            if(test==2):
                ip=input("请输入要扫描的ip（192.168.1.1或者192.168.1.0/24)：")
                #ip=ip.split(" ")
                po=input("请输入要扫描的端口列表（22,25或者1-200)：")
                print("开始扫描：")
                nmscan(hosts=ip,port=po)
        except Exception as e:
            print("输入有误，请检查并按格式输入！")
            time.sleep(2)
        try:
            if(test==3):
                ip=input("请输入要扫描的ip（192.168.1.1)：")
                #ip=ip.split(" ")
                po=input("请输入要扫描的端口列表（22,25)：")
                fwmain(ip=ip,port=po)
        except Exception as e:
            print("输入有误，请检查并按格式输入！")
            time.sleep(2) 
    except Exception as e:
        print("输入有误，请检查并按格式输入！")
        time.sleep(2) 
