import os
import tkinter as tk
from tkinter import filedialog
import urllib3
import requests
from tqdm import tqdm
urllib3.disable_warnings()

root = tk.Tk()
root.withdraw()


def get_ts_list(file_path):
    ts_list = []
    with open(file_path,'r') as f:
        for line in f.readlines():
            if line.split('.')[-1] == 'ts\n':
                line = 'https://cdn4.yzzy-kb-cdn.com/20220605/16674_8bfa3672/1000k/hls/'+line
                # line = 'https://cdn4.yzzy-kb-cdn.com/20220605/16676_9bab22b1/1000k/hls/'+line
                ts_list.append(line.replace('\n', ''))
    return ts_list


# m3u8文件夹
folder_path = filedialog.askdirectory()
# 视频文件夹
video_path = filedialog.askdirectory()
headers = {
	'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
}
# m3u8文件
file_list = []
for file in os.listdir(folder_path):
    if file.split('.')[-1] == 'm3u8':
        file_list.append(file)

#
num_video=1
while True:
    if len(os.listdir(video_path))==num_video:
        break
    try:
    # num = 0
        for file_name in file_list:
            # num = num+1
            file_path = os.path.join(folder_path, file_name)
            ts_list = get_ts_list(file_path)
            # temp_path = folder_path + r'/temp'+file_name
            temp_path = folder_path + r'/temp'
            f_temp = open(temp_path+'.txt','wb')
            if not os.path.exists(temp_path):
                os.mkdir(temp_path)
            i = 0
            all_num = len(ts_list)
            s = requests.session()
            for url_ts in tqdm(ts_list):
                i = i + 1
                ts_file_path = temp_path+'/'+str(i)+'.ts'
                f_temp.write(('file '+'\''+ts_file_path+'\''+'\n').encode())
                if os.path.exists(ts_file_path):
                    continue
                r = s.get(url_ts, headers=headers, verify=False)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                with open(ts_file_path, 'wb') as f:
                    f.write(r.content)


            # commend = 'D:\\mycodetool\\ffmpeg\\bin\\ffmpeg.exe -f concat -safe 0 -i '+temp_path+'.txt'+' -c copy '+video_path.replace('/', '\\')+'\\{}.mp4'.format(file_name.replace('.m3u8','').replace(' ',''))
            # print(commend)

            # commend = r'cd C:\Users\92323 && copy /b ' + temp_path.replace('/', '\\') + r'\*.ts '+video_path.replace('/', '\\') + '\\'+file_name.replace('.m3u8','').replace(' ','')+'.mp4'
            # # commend = r'cd C:\Users\92323 && copy /b ' + temp_path.replace('/', '\\') + r'\*.ts '+video_path.replace('/', '\\') + '\\aa.mp4'
            #
            # print(commend)
            # os.system(commend)


            with open(os.path.join(video_path, file_name.replace('.m3u8', '').replace(' ', '') + '.mp4'), 'wb') as f:

                for i in range(1,1+len(os.listdir(temp_path)),1):
                    fi = open(os.path.join(temp_path,str(i)+'.ts'), 'rb')
                    f.write(fi.read())

            # for i in os.listdir(temp_path):
            #     os.remove(temp_path+'/'+i)
            # os.removedirs(temp_path)

    except Exception as e:
        print(e)
        pass

