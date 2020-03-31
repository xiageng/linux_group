#! /user/bin/enn python
#-*- coding: utf-8 -*-

from robot.libraries.Telnet import Telnet
import logging as log
import subprocess
import time
username = "admin02"
password = "0000"

def cmd_excute_process(cmd):
    process = subprocess.Popen(cmd,shell= True,stdout = subprocess.PIPE,stderr=subprocess.STDOUT)
    return_code = process.returncode
    process.communicate()
    return return_code

def start_ul_iperf():
    cmd = "sshpass -p 0000 ssh admin02@10.70.87.24 C:/Users/admin02/Desktop/xiageng/ul_tput.bat"
    output = cmd_excute_process(cmd)
    print(output)
def kill_iperf():
    cmd = "sshpass -p 0000 ssh admin02@10.70.87.24 C:/Users/admin02/Desktop/xiageng/ul_tput_stop.bat"
    output = cmd_excute_process(cmd)
    print(output)

if __name__=='__main__':
    start_ul_iperf()
