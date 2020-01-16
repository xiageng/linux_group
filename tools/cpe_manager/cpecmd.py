# -*- coding: utf-8 -*-

import pexpect
import os
import logging
import re
import threading

class CPE_command(object):
    def __init__(self, hostip):
        self.hostip = hostip

    def cpe_attach(self):
        ue_command = 'at 1'
        regxp_message = 'INTERFACE READY INDICATION'
        _cpe_command(self.hostip, ue_command, regxp_message)

    def cpe_detach(self):
        ue_command = 'dt 1 0'
        regxp_message = 'INTERFACE RELEASE INDICATION'             # Network detached
        _cpe_command(self.hostip, ue_command, regxp_message)

    def cpe_connect(self):
        ue_command = 'AT+CGATT?'
        regxp_message = '\+CGATT\:1'
        _cpe_command(self.hostip, ue_command, regxp_message)

    def cpe_disconnect(self):
        ue_command = 'AT+CGATT?'
        regxp_message = '\+CGATT\:0'
        _cpe_command(self.hostip, ue_command, regxp_message)

def _cpe_command(hostip, ue_command, regxp_message):
    hostport='23'
    cmd='telnet '+hostip+' '+hostport
    child=pexpect.spawn(cmd)
    child.logfile = open("ue_command.txt", "w")
    i0=child.expect('login: ')
    if i0 == 0:
        child.sendline('root')
        i1=child.expect('Password: ')
        if i1 == 0:
            child.sendline('Si8a&2vV9')
            i2=child.expect('# ')
            if i2 == 0:
                child.sendline('lted_cli')
                i3 = child.expect('lted_client_init_ex success')
                if i3 == 0:
                    child.sendline('arm1log 2')
                    i4=child.expect(['DM> ', ''])
                    if i4 == 0 or i4 == 1:
                        child.sendline(ue_command)
                        child.expect([regxp_message, pexpect.EOF, pexpect.TIMEOUT])
                        print child.before+child.after
                    else:
                        print "ue command fail"
                else:
                    print "login ue command fail"
            else:
                print "login cpe fail"
        else:
            print "password wrong"
    else:
        print "telnet fail"

class CPE_ul_thoughput(object):
    def __init__(self, hostip, **kwargs):
        self.hostip = hostip

    def cpe_send_ul_throughput(self, **kwargs):
        ul_iperf_ip=kwargs.get('ul_iperf_ip', '10.0.1.1')
        ul_iperf_port=kwargs.get('ul_iperf_port', '5210')
        ul_iperf_time=kwargs.get('ul_iperf_time', '7200')
        ul_iperf_tp=kwargs.get('ul_iperf_tp', '10M')
        shell_command='iperf -u -c {} -p {} -t {} -b {} -l 1400.0B -w 100M -T 64'.format(ul_iperf_ip, ul_iperf_port, ul_iperf_time, ul_iperf_tp)
        shell_regxp='Client connecting to {}, UDP port {}'.format(ul_iperf_ip, ul_iperf_port)
        _cpe_shell(hostip=self.hostip, shell_command=shell_command, regxp_message=shell_regxp)

    def cpe_stop_ul_throughput(self):
        shell_command='killall iperf'
        shell_regxp='#'
        _cpe_shell(hostip=self.hostip, shell_command=shell_command, regxp_message=shell_regxp)

    def cpe_reboot(self):
        if '{}'.format(_cpe_connect_status(self.hostip))=='connected':
            server_addr = get_cpe_ipaddr(self.hostip)
            if server_addr is not None:
                lines = os.popen("ps -ef|grep iperf").read().splitlines()
                for line in lines:
                    if server_addr in line:
                        logging.info(line)
                        pid = line.split()[1]
                        os.system("kill -9 %s" % pid)
                        print "kill -9 %s" % pid
                    else:
                        logging.info("{} not found".format(server_addr))
                        print "{} not found".format(server_addr)
        shell_command = 'reboot'
        shell_regxp = 'Connection closed by foreign host.'
        _cpe_shell(hostip=self.hostip, shell_command=shell_command, regxp_message=shell_regxp)


def _cpe_shell(hostip, shell_command, regxp_message):
    hostport='23'
    cmd='telnet '+hostip+' '+hostport
    child=pexpect.spawn(cmd)
    child.logfile = open("ue_command.txt", "w")
    i0=child.expect('login: ')
    if i0 == 0:
        child.sendline('root')
        i1=child.expect('Password: ')
        if i1 == 0:
            child.sendline('Si8a&2vV9')
            i2=child.expect('# ')
            if i2 == 0:
                child.sendline(shell_command)
                child.expect([regxp_message, pexpect.EOF, pexpect.TIMEOUT])
                print child.before+child.after
            else:
                print "login cpe fail"
        else:
            print "password wrong"
    else:
        print "telnet fail"


def cpe_send_dl_throughput(hostip, thoughput):
    server_addr=get_cpe_ipaddr(hostip)
    import subprocess
    subprocess.Popen('iperf -c {} -u -p 5001 -b {} -l 1400.0B -w 41.0K -t 7200.0 -P 1 -f k -T 1'.format(server_addr, thoughput), shell=True)
    # t=threading.Thread(target=_execute_command, args=(server_addr, thoughput))
    # t.start()

# def _execute_command(server_addr, thoughput):
#     os.system('iperf -c {} -u -p 5001 -b {} -l 1400.0B -w 41.0K -t 7200.0 -P 1 -f k -T 1'.format(server_addr, thoughput))

def cpe_stop_dl_throughput(hostip):
    server_addr = get_cpe_ipaddr(hostip)
    lines = os.popen("ps -ef|grep iperf").read().splitlines()
    for line in lines:
        if server_addr in line:
            logging.info(line)
            pid = line.split()[1]
            os.system("kill -9 %s" % pid)
        else:
            logging.info("{} not found".format(server_addr))

def get_cpe_ipaddr(host_ip):
    # _cpe_shell(hostip=host_ip, shell_command='killall gct_lted', regxp_message='#')
    _cpe_command(host_ip, ue_command='at+cgpaddr', regxp_message='CGPADDR\:\ \d\,\"\d*\.\d*\.\d*\.\d*\"')
    with open('ue_command.txt', 'r') as f:
        lines=f.readlines()
        for line in lines:
            if '+CGPADDR:' in line:
                ip = re.findall('\d+\.\d+\.\d+\.\d+', line)[0]
                return ip

def cpe_get_current_throughput(host_ip, direction='all'):
    tput={}
    _cpe_command(host_ip, ue_command='at%GTPUT?', regxp_message='GTPUT\:\ DL\ (\d*)\,(\d*),(\d*)')
    with open('ue_command.txt', 'r') as f:
        lines=f.readlines()
        temp_tput={}
        for line in lines:
            if re.findall('GTPUT: DL', line):
                cur_rate_DL=re.findall('GTPUT: DL (\d*)', line)[0]
                cur_rate_DL=int(cur_rate_DL)*8
                temp_tput['dl']=cur_rate_DL
            elif re.findall('GTPUT: UL', line):
                cur_rate_UL=re.findall('GTPUT: UL (\d*)', line)[0]
                cur_rate_UL=int(cur_rate_UL)*8
                temp_tput['ul']=cur_rate_UL
        tput[host_ip]=temp_tput
    if direction=='all':
        return tput[host_ip]
    else:
        return tput[host_ip].get(direction)

def _cpe_connect_status(host_ip):
    connect_status={'0':'disconnected',
                    '1':'connected'}
    _cpe_command(host_ip, ue_command='AT+CGATT?', regxp_message='\+CGATT\:\d')
    with open('ue_command.txt', 'r') as f:
        lines=f.readlines()
        for line in lines:
            if re.findall('\+CGATT\:', line):
                key=re.findall('CGATT:(\d)', line)[0]
    return connect_status.get('{}'.format(key))

def send_lockcell_command(host_ip, earfcn, pci):
    _cpe_command(host_ip, ue_command='AT%GLOCKCELL=1,{},{}'.format(earfcn, pci), regxp_message='RRC Lock Celllist SET')

def netspeed():
    import time
    import commands
    status, R1 = commands.getstatusoutput('cat /sys/class/net/eth0/statistics/rx_bytes')
    status, T1 = commands.getstatusoutput('cat /sys/class/net/eth0/statistics/tx_bytes')
    time.sleep(1)
    status, R2 = commands.getstatusoutput('cat /sys/class/net/eth0/statistics/rx_bytes')
    status, T2 = commands.getstatusoutput('cat /sys/class/net/eth0/statistics/tx_bytes')
    TKBPS = (int(T2) - int(T1)) / 128
    RKBPS = (int(R2) - int(R1)) / 128
    return '{}\ntx eth0: {} kbps rx eth0: {} kbps'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), TKBPS, RKBPS)

def override_cqi(host_ip, cqi_value):
    _cpe_command(host_ip, ue_command='l1r  cfg cqi fix {}'.format(cqi_value), regxp_message='DM>')

if __name__ == '__main__':
    # cpe=CPE_command('192.168.200.1')
    # cpe.cpe_connect()
    # cpe.cpe_disconnect()
    # cpe.cpe_attach()
    # cpe.cpe_detach()
    # thoughput=CPE_ul_thoughput('192.168.200.1')
    # thoughput.cpe_send_ul_throughput()
    # thoughput.cpe_stop_ul_throughput()
    # thoughput.cpe_reboot()
    # cpe_send_dl_throughput(hostip='192.168.200.1', thoughput='100M')
    # cpe_stop_dl_throughput(hostip='192.168.200.1')
    # print cpe_get_current_throughput(hostip='192.168.200.5', direction='dl')
    # print cpe_get_current_throughput('192.168.200.1', direction='dl')
    # print get_cpe_ipaddr('192.168.200.1')
    # print _cpe_connect_status('192.168.200.1')
    print netspeed()
    pass







