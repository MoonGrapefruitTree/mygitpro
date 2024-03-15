import os
import tkinter as tk
from tkinter import filedialog

import requests
from tqdm import tqdm

root = tk.Tk()
root.withdraw()


def get_ts_list(file_path):
    ts_list = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if line.split('.')[-1] == 'ts\n':
                ts_list.append(line.replace('\n', ''))
    return ts_list


# m3u8文件夹
folder_path = filedialog.askdirectory()
# 视频文件夹
video_path = filedialog.askdirectory()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
}
num_video = 12
# m3u8文件
j = 0
session = requests.session()
while True:
    if len(os.listdir(video_path)) == num_video:
        break
    try:
        for file in os.listdir(folder_path):
            if not file.split('.')[-1] == 'm3u8':
                continue

            file_path = (folder_path + '/' + file).replace('/', '\\')
            f_temp = open(folder_path + '/temp_' + file.replace(' ', ''), 'wb')
            temp_path = folder_path + r'/temp_' + file.replace('.m3u8', '').replace(' ', '')
            if not os.path.exists(temp_path):
                os.mkdir(temp_path)

            i = 0
            with open(file_path, 'rb') as f_mu:
                # print(file_path)
                for line in tqdm(f_mu.readlines()):
                    if line.decode().__contains__('enc.key'):
                        f_temp.write(line.decode().replace('enc.key', file_path.replace('.m3u8', '.key')).replace('\\',
                                                                                                                  '/').encode())
                    elif line.decode().__contains__('.ts'):
                        i = i + 1
                        ts_file_path = (temp_path + '/' + str(i) + '.ts')
                        f_temp.write((ts_file_path.replace('/', '\\') + '\n').encode())

                        if os.path.exists(ts_file_path):
                            continue
                        # break
                        r = requests.get(line.decode()[:-1], headers=headers)
                        r.raise_for_status()
                        r.encoding = r.apparent_encoding
                        with open(ts_file_path, 'wb') as f:
                            f.write(r.content)
                            f.close()
                    else:
                        f_temp.write(line)

            f_temp.close()
            j = j + 1
            if not os.path.exists(video_path.replace('/', '\\') + '\\' + file.replace('.m3u8', '.mp4')):
                commend = r'cd C:\Users\92323 && ffmpeg -allowed_extensions ALL -i ' + folder_path.replace('/',
                                                                                                           '\\') + '\\temp_' + file.replace(
                    ' ', '') + ' -c copy ' + video_path.replace('/', '\\') + '\\' + file.replace('.m3u8', '.mp4')
                print(commend)
                os.system(commend)
    except Exception as e:
        j = j + 1
        print(e)
        pass
