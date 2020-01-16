# -*- coding: utf-8 -*-

import paramiko
import time
import re
import os

def ssh(sys_ip, cmds, username='ute',password='ute'):
    try:
        #创建ssh客户端
        client = paramiko.SSHClient()
        #第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #密码方式远程连接
        client.connect(sys_ip, 22, username=username, password=password, timeout=20)
        #互信方式远程连接
        #key_file = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
        #ssh.connect(sys_ip, 22, username=username, pkey=key_file, timeout=20)
        #执行命令
        stdin, stdout, stderr = client.exec_command(cmds)
        #获取命令执行结果,返回的数据是一个list
        result = stdout.readlines()
        return result
    except Exception, e:
        print e
    finally:
        client.close()

def _ssh2(sys_ip, cmds, username='ute',password='ute'):
    try:
        #创建ssh客户端
        client = paramiko.SSHClient()
        #第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #密码方式远程连接
        client.connect(sys_ip, 22, username=username, password=password, timeout=20)
        #互信方式远程连接
        #key_file = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
        #ssh.connect(sys_ip, 22, username=username, pkey=key_file, timeout=20)
        #执行命令
        client.exec_command(cmds)
    except Exception, e:
        print e
    finally:
        client.close()
def get_netspeed(sys_ip):
    R1=ssh(sys_ip, cmds='cat /sys/class/net/eth0/statistics/rx_bytes')[0]
    T1 = ssh(sys_ip, cmds='cat /sys/class/net/eth0/statistics/tx_bytes')[0]
    time.sleep(0.77)    #远程的时候有延时，改1秒为0.77秒
    R2 = ssh(sys_ip, cmds='cat /sys/class/net/eth0/statistics/rx_bytes')[0]
    T2 = ssh(sys_ip, cmds='cat /sys/class/net/eth0/statistics/tx_bytes')[0]
    TKBPS = (int(T2) - int(T1)) / 128
    RKBPS = (int(R2) - int(R1)) / 128
    return '{}\n tx eth0: {} kbps rx eth0: {} kbps'.format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), TKBPS, RKBPS)

def kill_inactive_iperf(sys_ip, inactive_s1_ip):
    lines = ssh(sys_ip, cmds="ps -ef| grep iperf")
    for line in lines:
        if inactive_s1_ip in line:
            pid = re.findall('ute\s+(\d+)\s.+iperf \-c {}'.format(inactive_s1_ip), line)[0]
            ssh(sys_ip, "sudo kill -9 %s" % pid)

def send_iperf_data_via_remoteip(sys_ip, active_s1_ip, trans_data, len_size, duration_time='7200'):
    cmd='iperf -c {} -u -p 5001 -b {} -l {} -w 41.0K -t {} -P 1 -f k -T 1'.format(active_s1_ip, trans_data, len_size, duration_time)
    _ssh2(sys_ip, cmds=cmd)

