"""
用于从云班课结束的任务中提取成绩。
"""
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog
import pandas as pd
root = tk.Tk()
root.withdraw()

# FolderName = filedialog.askdirectory()  #获取文件夹
FileName = filedialog.askopenfilename(title=u'选择文件', filetypes=[("HTML",".html")])  #获取文件夹中的某文件
file_read = open(FileName, encoding='utf-8')
html_content = file_read.read()
file_read.close()
html_soup = BeautifulSoup(html_content, 'html.parser')
student_boxs = html_soup.findAll(name='div', attrs={'class': 'homework-item'})
res_dict = {}
for student_box in student_boxs:
    id_box = student_box.find(name='div', attrs={'class': 'member-message'}).find(name='div')
    name_box = student_box.find(name='div', attrs={'class': 'member-message'}).find(name='span')
    id = id_box.text.upper()
    name = name_box.text.upper()
    res_dict[id] = []
    res_dict[id].append(name)
    try:
        soures_box = student_box.findAll(name='div', attrs={'class': 'appraised-type'})[1]
        source = soures_box.findAll(name='span')[-1].text.replace('分', '')
        res_dict[id].append(int(source))
    except:
        res_dict[id].append(0)

res_csv = pd.DataFrame(res_dict, index=['姓名', '得分']).T
file_path = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("CSV", ".csv")])
res_csv.to_csv(file_path+'.csv', encoding='utf-8-sig')

