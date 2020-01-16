#-*- encoding: utf-8 -*-
#author : zhangwenchao
#CreateDate : 2018-11-5
#version 1.0


import os
import glob
import re
from Tkinter import *
import ttk
from tkFileDialog import *

file_types=['bts.log.*', '*.LOG']

def get_log_file(file_path):
    listed=[]
    for type in file_types:
        temp_list = glob.glob('{}'.format(os.path.join(file_path, type)))
        listed.extend(temp_list)
    return listed

def filter_keyword(file_path, keyword):
    dicted={}
    for filename in get_log_file(file_path):
        with open(filename, 'r') as fread:
            listed=[]
            # lines = fread.readlines()
            # file_name=os.path.basename(filename)
            for line in fread:
                k = re.compile(keyword,re.I)
                rs = re.findall(k, line)
                if rs:
                    listed.append(line)
            dicted[filename]=listed
    return dicted

def wirte_dict_into_txt(file_path, keyword1, condition='', keyword2=''):
    if condition=='':
        keyword=keyword1
    elif condition=='|' and keyword2!='':
        keyword='{}|{}'.format(keyword1, keyword2)
    elif condition=='&' and keyword2!='':
        keyword='{}.+{}|{}.+{}'.format(keyword1,keyword2,keyword2,keyword1)
    else:
        keyword=None
    if keyword is not None:
        dicted=filter_keyword(file_path, keyword)
        if os.path.exists('filter.txt'):
            os.remove('filter.txt')
        file = open('filter.txt', 'a')
        for key in dicted.keys():
            if len(dicted[key]):
                file.write('{}\n{}\n{}\n'.format('='*40, key.split('/')[-1], '='*40))
                file.writelines(dicted[key])
        file.close()
        print "handle finished !"
    else:
        print 'keyword condition is None!'

def handle_log():
    global path, textpad, filter1, filter2, condition
    root1 = Tk()
    root1.wm_title('handle LOG')
    Label(root1, text='log file dir:').grid(row=0, column=0, sticky=W)
    path = StringVar()
    path.set('')
    h1 = Entry(root1, textvariable=path)
    h1.grid(row=0, column=1, sticky=W)
    h1['width'] = 53
    b1 = Button(root1, text='browse', command=selectpath)
    b1['width'] = 5
    b1.grid(row=0, column=2, sticky=E)
    Label(root1, text='filter 1:').grid(row=1, column=0, sticky=W)
    filter1 = StringVar()
    h2 = Entry(root1, textvariable=filter1)
    h2.grid(row=1, column=1, sticky=W)
    h2['width'] = 53
    Label(root1, text='condition:').grid(row=4, column=0, sticky=W)
    condition = StringVar()
    h3 = ttk.Combobox(root1, width=12, textvariable=condition, state='readonly')
    h3['values']= ('', '|', '&')
    h3['width'] = 5
    h3.grid(row=4, column=1, stick=W)
    Label(root1, text='filter 2:').grid(row=3, column=0, sticky=W)
    filter2 = StringVar()
    h4 = Entry(root1, textvariable=filter2)
    h4.grid(row=3, column=1, sticky=W)
    h4['width'] = 53
    b2 = Button(root1, text='enter', command=display_text)
    b2.grid(row=1, column=2, rowspan=4, sticky=E)
    b2['height']=3
    b2['width']=5
    textpad=Text(root1, undo=True)
    textpad.grid(row=5, column=0,columnspan=3)
    scroll=Scrollbar()
    scroll.grid(row=5, column=3, sticky='ns')
    textpad.config(yscrollcommand=scroll.set)
    scroll.config(command=textpad.yview)
    root1.resizable(width=False, height=False)
    root1.mainloop()

def selectpath():
    path_= askdirectory()
    path.set(path_)

def display_text():
    wirte_dict_into_txt(path.get(), filter1.get(), condition.get(), filter2.get())
    textpad.delete(1.0, END)
    f = open('filter.txt', 'r')
    textpad.insert(1.0, f.read())
    f.close()
    search(filter1.get())

def copy():
    textpad.event_generate("<<Copy>>")


def search(search_str):
    textpad.tag_remove('match', '1.0', END)
    length = IntVar()
    if search_str:
        pos='1.0'
        while True:
            pos= textpad.search(search_str, pos, END, count=length, nocase=1)
            if not pos:break
            lastpos= '{0}+{1}c'.format(pos, length.get())
            textpad.tag_add('match', pos, lastpos)
            pos = textpad.index(lastpos)
        textpad.tag_config('match', background='yellow')

if __name__ == '__main__':
    handle_log()
    pass
