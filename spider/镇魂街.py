# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 10:54:10 2020

@author: Hs
"""

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import os
import time
import random


#获得网页url

def geturl(base_num,page=1):
    base_url=r'http://www.pufei8.com/manhua/20/'
    change_url=str(base_num)+'?page='+str(page)
    return base_url+change_url

#获得目录的url
def getmean(url):
    opt = webdriver.ChromeOptions()          # 创建chrome对象
    opt.add_argument('headless')          # 把chrome设置成wujie面模式，不论windows还是linux都可以，自动适配对应参数
    driver = webdriver.Chrome(options=opt)    # 指定chrome驱动程序位置和chrome选项
    driver.get(url)          # 访问网页
    time.sleep(15+random.random())           # 等待5秒
    content = driver.page_source 
    soup=BeautifulSoup(content,'html.parser')
    div=soup.find_all('div',class_=['plist','pmedium'])[0]
    a_s=div.find_all('a')
    lst=[]
    for a in a_s:
        str1=str(a['href']).split('/')[-1]
        lst.append(str1)
    return lst

#request获得图片内容
def getimg(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.content
    except:
        return '获取网页失败'

#webdriver抓取漫画网页内容

def get_url_text(url):
    opt = webdriver.ChromeOptions()          # 创建chrome对象
    opt.add_argument('headless')          # 把chrome设置成wujie面模式，不论windows还是linux都可以，自动适配对应参数
    driver = webdriver.Chrome(options=opt)    # 指定chrome驱动程序位置和chrome选项
    try:
        driver.get(url)          # 访问网页
        time.sleep(3+random.random())           # 等待5秒
        content = driver.page_source 
        return content
    except:
        return '网页不存在'
        
#分析网页内容

def Analysisweb(html,attrs='html.parser'):
    soup=BeautifulSoup(html,attrs)
    title=soup.find_all('title')[0].string
    url=soup.find_all('div',class_='viewimages')[0].contents[1]['src']
    return title,url

#将所得列表储存到csv文件

def savecsv(path,lst1):
   pass


def get_one_img(url):
    

    html=get_url_text(url)
    
    path_add,url_img=Analysisweb(html)
    
    img=getimg(url_img)
    
    root='E:\\漫画\\镇魂街\\'+path_add+'\\'
    
    path='E:\\漫画\\镇魂街\\'+path_add+'\\'+str(url.split('=')[-1])+".jpg"
    
    if not os.path.exists(root):
        
        os.mkdir(root)
        
    if not os.path.exists(path):  
        
        f=open(path,'wb')
        
        f.write(img)
        
        print('储存完成'+str(url.split('=')[-1]))
        
    else:
        
        print('文件已存在'+str(url.split('=')[-1]))

def main():
    lst=getmean('http://www.pufei8.com/manhua/20/')
    print('共有'+str(len(lst))+'章')
    chart=1
    for num in lst[6:-1]:
        soup=BeautifulSoup(get_url_text(geturl(base_num=num)),'html.parser')
        if not soup=='网页不存在':
            pages=len(soup.find_all('option'))
            print('第'+str(chart)+'章：共'+str(int(pages/2))+'页')
            chart=chart+1
            for page in range(1,int(pages/2)+1):
                url=geturl(base_num=num,page=page)
                get_one_img(url)
        else:
            continue

main()