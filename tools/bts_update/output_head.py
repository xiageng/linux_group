#! /user/bin/enn python
#-*- coding: utf-8 -*-
import os
import subprocess

def handle_output_head():
    file_path='/home/ute/robotlte/result'
    cmd = 'ls --full-time {}/back_by_glutton | sed -n "/2019-09-24/p"'.format(file_path)
    child = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    list_files = child.stdout.read().splitlines()
    for line in list_files:
        item = line.strip().split()[-1]
        flag=check_file("{}/back_by_glutton/{}".format(file_path,item))
        if flag:
            newitem = item.split('_')[-2]+'_output.xml'
            newfile = os.path.join("{}/xiageng".format(file_path),newitem)
            cmd='cp {}/back_by_glutton/{} {}'.format(file_path,item,newfile)
            print("current cmd:{}".format(cmd))
            os.system(cmd)
        else:
            print("there is no match file\n")

def check_file(file):
    with open(file,"rb") as f:
        output=f.read()
        if "LTE5141" in output:
            if "SBTS20A" in output:
                return True
    return False
if __name__=="__main__":
    handle_output_head()