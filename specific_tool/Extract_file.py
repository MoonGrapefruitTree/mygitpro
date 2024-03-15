import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
root = tk.Tk()
root.withdraw()


headers = {
	'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
}
#目录
folder_path = filedialog.askdirectory()
headers = {
	'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
}

contents_url = 'https://www.kundihulan.com/video/83902.html'
r = requests.get(contents_url, headers=headers)
r_test = r.text
soup = BeautifulSoup(r_test, 'html.parser')
ul_list = soup.find('ul', class_='tzt-playlist sort-list playlist')
url_list=[]
# a_list = ul_list.find('a')
for ul in ul_list:
    a = ul.find('a')
    if a != None:
        url_list.append('https://www.kundihulan.com'+a.get('href'))

print(url_list)

i = 0
for url in tqdm(url_list):
    r_url = requests.get(url,headers=headers)
    r_url_test = r_url.text
    soup_url = BeautifulSoup(r_url_test, 'html.parser')
    divbox=soup_url.findAll('div', class_='embed-responsive embed-responsive-16by9')

    player_aaaa = divbox[0].find('script',type='text/javascript').text.replace('var player_aaaa=','')

    m3u8_url = player_aaaa.split('\"url\":')[1].split(',\"url_next\":')[0].replace('\"', '').replace('\\','')

    key_url = 'https://1080p.jszyplay.com/play/'+m3u8_url.split('/')[-2]+'/enc.key'

    r_m3u8 = requests.get(m3u8_url)
    r_key = requests.get(key_url)
    i = i+1
    f_m3u8 = open(folder_path+'/'+str(i)+'.m3u8','wb')
    f_m3u8.write(r_m3u8.content)
    f_m3u8.close()
    f_key = open(folder_path + '/' + str(i) + '.key', 'wb')
    f_key.write(r_key.content)

