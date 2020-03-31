#!/bin/bash
# -*- coding: utf-8 -*-
import os,subprocess
import shutil


cmd = "find /home/ute/robotlte/result/back_by_glutton/ -ctime 0"
child = subprocess.Popen(cmd, shell='True',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#os.system(cmd)
file = child.stdout.read().strip().split("\n")
#print(file)
for item in file:
    print(item)
    if item.find("output.xml") != -1:
        newfile = item.split("_")[-2]+"_output.xml"
        newfile = os.path.join(os.getcwd(),newfile)
        print(newfile)
        shutil.move(item, newfile)
     

