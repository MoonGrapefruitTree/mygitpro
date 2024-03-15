# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 13:01:19 2021

@author: Hs
"""
import requests
from bs4 import BeautifulSoup
import os
url="https://developer.aliyun.com/article/780465"



r=requests.get(url)
r.encoding=r.apparent_encoding
soup=BeautifulSoup(r.text,'html.parser')
h3_label=soup.find_all('h3')
p_label=soup.find_all('p')
title=[]
url_mp4=[]
name_mp4=[]
num=[]
for i in [1,2,3,4,5]:
    title.append(h3_label[i-1].text)
    num.append(len(p_label[i].find_all('a')))
    name_mp4.append(str(p_label[i]).replace('<p>','').split('<br/>')[0::2])
    for j in range(num[-1]):
        url_mp4.append(p_label[i].find_all('a')[j].text)
sum_num=0


for i in range(5):
    root='E:\\dataworks\\'+str(title[i])
    print(root)
    if not os.path.exists(root):
        os.mkdir(root)
        print('创建'+str(title[i]))
    else:
        print(str(title[i])+'已存在')
    for j in range(num[i]):  
        r=requests.get(url_mp4[j+sum_num])
        path=root+'\\'+str(name_mp4[i][j])+".mp4"
        if not os.path.exists(path):  
            f=open(path,'wb')
            f.write(r.content)
            print('储存完成'+str(name_mp4[i][j]))
        else:
            print('图片已存在'+str(name_mp4[i][j]))
    sum_num=sum_num+num[i]


















