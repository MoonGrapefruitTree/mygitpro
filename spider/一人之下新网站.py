# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:02:12 2021

@author: lenovo
"""
import requests
from requests_html 
from bs4 import BeautifulSoup
import os



def get_img_index(url):#通过目录信息获得某一章节每张图片的index
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Host':'www.qiman6.com',
        'Cookie':'Hm_lvt_4936e11c417c830210d6a6defe10b813=1610590078; Hm_lpvt_4936e11c417c830210d6a6defe10b813=1610590078; UM_distinctid=176fea643103ae-0099b2c009125-4c3f207e-100200-176fea64311166; CNZZDATA1260951462=1157316124-1610588874-null%7C1610588874',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        }
    r=requests.get(url,headers=headers)
    soup=BeautifulSoup(r.text,'html.parser')
    indexes=soup.find_all('script',)
    index_d=indexes[3]
    index_z=str(index_d).split(',')[-3]
    index_f=str(index_z).split('.')
    index=str(index_f[0]).replace("'", '').split('|')
    real_index=[]
    for i in index:
        if len(i)>10:
            real_index.append(i)
    return real_index

def get_image(index): #通过每张图片的index获得图片数据
    url='https://p.pstatp.com//origin//'
    img=[]
    for i in index:
        real_url=url+str(i)
        r=requests.get(real_url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        img.append(r.content)
    return img

def save_img(cartoon_name,chapter_name,img):#将获得的数据存到电脑
    
    root='E:\\漫画\\'+str(cartoon_name)+'\\'+chapter_name+'\\'
    if not os.path.exists(root):
        os.mkdir(root)
        print('创建'+str(chapter_name))
    else:
        print(str(chapter_name)+'已存在')
            
    k=0
    for i in img:
        k=k+1
        path=root+str(k)+".jpg"
        if not os.path.exists(path):  
            f=open(path,'wb')
            f.write(i)
            print('储存完成'+str(k))
        else:
            print('图片已存在'+str(k))

def get_mean_list(number):#通过网站漫画代码获得目录
    chapter_index=[]
    chapter_name=[]
#直接菜单
    r=requests.get('http://www.qiman6.com/'+str(number)+'/')
    soup=BeautifulSoup(r.text,'html.parser')
    inname=soup.find_all('a',class_="ib")
    innames=[]
    num=-20
    for i in range(20):
        innames.append(inname[num])
        num=num+1
    for i in innames:
        chapter_name.append(i.text)
        chapter_index.append(i.get('href').replace('.','/').split('/')[-2])
#隐藏菜单     
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Host':'www.qiman6.com',
        'Cookie':'CNZZDATA1260951462=1157316124-1610588874-null|1610615875; Hm_lpvt_4936e11c417c830210d6a6defe10b813=1610616933; Hm_lvt_4936e11c417c830210d6a6defe10b813=1610590078; UM_distinctid=176fea643103ae-0099b2c009125-4c3f207e-100200-176fea64311166',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Content-Length':'14',
        'Pragma':'no-cache',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Upgrade-Insecure-Requests':'1',
        }
    mean_list='http://www.qiman6.com/bookchapter/'
    d = {'id': str(number), 'id2': '1'}
    r=requests.post(mean_list,data=d,headers=headers)
    r.raise_for_status()
    r.encoding=r.apparent_encoding
    r1=r.text.replace('{"chapterid":','')
    r2=r1.replace('"chaptername":','')
    r3=r2.replace('}','')

    r4=r3.replace('"','')
    r4=r4.replace('[', '')
    r5=r4.split(',')
    for i in range(len(r5)):
        if i%2==0:
            chapter_index.append(r5[i])
        else:
            chapter_name.append(r5[i])   
    return chapter_index,chapter_name

def get_cartoon_number(cartoon_name):#通过名字获得网站的漫画代码
    
    r=requests.get('http://www.qiman6.com/search.php?keyword='+str(cartoon_name))
    try:
        soup=BeautifulSoup(r.text,'html.parser')
        a_num=soup.find('a',title=str(cartoon_name))
        number=a_num.get('href').replace('/','')
        return int(number)
    except :
        return '没有找到你想看的哦'
    
def main():
    print('你想看什么漫画')
    name=input()
    number=get_cartoon_number(name)
    if type(number)==int:
        chapter_index,chapter_name=get_mean_list(number)
        for i in range(10):#当前下载前十章，下载全部用range(len(chapter_index))
            url='http://www.qiman6.com/'+str(number)+'/'+str(chapter_index[i])+'.html'
            index=get_img_index(url)
            img=get_image(index)
            save_img(name,chapter_name[i],img)
    else:
        print(number)

        
main()