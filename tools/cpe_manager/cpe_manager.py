# -*- coding: utf-8 -*-
"""
author：zhangwenchao
version:1.2         #update auto conect ue tput
version:1.3         #read config.ini file
version 1.4         #add get all status button
version 2.0         #decrepit html get info
"""

from Tkinter import *
import ttk
from tkMessageBox import *
import cpecmd
import cpe
import ConfigParser
import os
import re
import ssh_command
import collect_log
import handle_data

hostip={'1': 'hostip_1',
    '2': 'hostip_2',
    '3': 'hostip_3',
    '4': 'hostip_4',
    '5': 'hostip_5',
    '6': 'hostip_6',
    '7': 'hostip_7',
    '8': 'hostip_8',
    '9': 'hostip_9',
    '10': 'hostip_10',
    '11': 'hostip_11',
    '12': 'hostip_12',
    '13': 'hostip_13',
    '14': 'hostip_14',
    '15': 'hostip_15',
    '16': 'hostip_16'}

targetip={'1': 'targetip_1',
    '2': 'targetip_2',
    '3': 'targetip_3',
    '4': 'targetip_4',
    '5': 'targetip_5',
    '6': 'targetip_6',
    '7': 'targetip_7',
    '8': 'targetip_8',
    '9': 'targetip_9',
    '10': 'targetip_10',
    '11': 'targetip_11',
    '12': 'targetip_12',
    '13': 'targetip_13',
    '14': 'targetip_14',
    '15': 'targetip_15',
    '16': 'targetip_16'}

ultput={'1': 'ultput_1',
    '2': 'ultput_2',
    '3': 'ultput_3',
    '4': 'ultput_4',
    '5': 'ultput_5',
    '6': 'ultput_6',
    '7': 'ultput_7',
    '8': 'ultput_8',
    '9': 'ultput_9',
    '10': 'ultput_10',
    '11': 'ultput_11',
    '12': 'ultput_12',
    '13': 'ultput_13',
    '14': 'ultput_14',
    '15': 'ultput_15',
    '16': 'ultput_16'}

dltput={'1': 'dltput_1',
    '2': 'dltput_2',
    '3': 'dltput_3',
    '4': 'dltput_4',
    '5': 'dltput_5',
    '6': 'dltput_6',
    '7': 'dltput_7',
    '8': 'dltput_8',
    '9': 'dltput_9',
    '10': 'dltput_10',
    '11': 'dltput_11',
    '12': 'dltput_12',
    '13': 'dltput_13',
    '14': 'dltput_14',
    '15': 'dltput_15',
    '16': 'dltput_16'}

var={'1': 'var1',
    '2': 'var2',
    '3': 'var3',
    '4': 'var4',
    '5': 'var5',
    '6': 'var6',
    '7': 'var7',
    '8': 'var8',
    '9': 'var9',
    '10': 'var10',
    '11': 'var11',
    '12': 'var12',
    '13': 'var13',
    '14': 'var14',
    '15': 'var15',
    '16': 'var16'}


def attach(k):
    try:
        command=cpecmd.CPE_command(hostip[k].get())
        command.cpe_disconnect()
        command.cpe_attach()
        pci=_get_lte_pci(hostip[k].get())
        labelframe1 = ttk.LabelFrame(tab1, text='ue{} info'.format(k), height=200, width=500)  # 信息区
        labelframe1.grid(row=17, column=0, columnspan=7, padx=10, pady=10)
        labelframe1.propagate(0)  # 使组件大小不变，此时width才起作用
        ttk.Label(labelframe1, text="{} ue attach PCI {} success!\n".format(hostip[k].get(), pci), font=('Mincho, 10')).pack(fill="both", expand="yes")
        return 'success'
    except:
        labelframe1 = ttk.LabelFrame(tab1, text='ue{} info'.format(k), height=200, width=500)  # 信息区
        labelframe1.grid(row=17, column=0, columnspan=7, padx=10, pady=10)
        labelframe1.propagate(0)  # 使组件大小不变，此时width才起作用
        ttk.Label(labelframe1, text="{} ue attach fail due to ltestatus is {} !\n".format(hostip[k].get(), cpecmd._cpe_connect_status(hostip[k].get())), font=('Mincho, 10')).pack(fill="both", expand="yes")
        return 'fail'

def detach(k):
    try:
        command=cpecmd.CPE_command(hostip[k].get())
        command.cpe_connect()
        command.cpe_detach()
        labelframe1 = ttk.LabelFrame(tab1, text='ue{} info'.format(k), height=200, width=500)  # 信息区
        labelframe1.grid(row=17, column=0, columnspan=7, padx=10, pady=10)
        labelframe1.propagate(0)  # 使组件大小不变，此时width才起作用
        ttk.Label(labelframe1, text="{} ue detach success!\n".format(hostip[k].get()), font=('Mincho, 10')).pack(fill="both", expand="yes")
        return 'success'
    except:
        labelframe1 = ttk.LabelFrame(tab1, text='ue{} info'.format(k), height=200, width=500)  # 信息区
        labelframe1.grid(row=17, column=0, columnspan=7, padx=10, pady=10)
        labelframe1.propagate(0)  # 使组件大小不变，此时width才起作用
        ttk.Label(labelframe1, text="{} ue attach fail due to ltestatus is {}!\n".format(hostip[k].get(), cpecmd._cpe_connect_status(hostip[k].get())), font=('Mincho, 10')).pack(fill="both", expand="yes")
        return 'fail'

def send_ul_tput(k):
    ul_thoughput = cpecmd.CPE_ul_thoughput(hostip[k].get())
    target_ip=targetip[k].get()
    ul_tput=ultput[k].get()
    if '{}'.format(target_ip)!='':
        ul_thoughput.cpe_send_ul_throughput(ul_iperf_ip=target_ip, ul_iperf_tp=ul_tput)
        labelframe1 = ttk.LabelFrame(tab1, text='ue{} info'.format(k), height=200, width=500)  # 信息区
        labelframe1.grid(row=17, column=0, columnspan=7, padx=10, pady=10)
        labelframe1.propagate(0)  # 使组件大小不变，此时width才起作用
        ttk.Label(labelframe1, text="{} send throughput {} to {}\n".format(hostip[k].get(), ul_tput, target_ip), font=('Mincho, 10')).pack(fill="both", expand="yes")

    else:
        ul_thoughput.cpe_send_ul_throughput(ul_iperf_tp=ul_tput)
        labelframe1 = ttk.LabelFrame(tab1, text='ue{} info'.format(k), height=200, width=500)  # 信息区
        labelframe1.grid(row=17, column=0, columnspan=7, padx=10, pady=10)
        labelframe1.propagate(0)  # 使组件大小不变，此时width才起作用
        ttk.Label(labelframe1, text="{} send throughput {} to {}\n".format(hostip[k].get(), ul_tput, '10.0.1.1'), font=('Mincho, 10')).pack(fill="both", expand="yes")

def stop_ul_tput(k):
    ul_thoughput = cpecmd.CPE_ul_thoughput(hostip[k].get())
    ul_thoughput.cpe_stop_ul_throughput()
    labelframe1 = ttk.LabelFrame(tab1, text='ue{} info'.format(k), height=200, width=500)  # 信息区
    labelframe1.grid(row=17, column=0, columnspan=7, padx=10, pady=10)
    labelframe1.propagate(0)  # 使组件大小不变，此时width才起作用
    ttk.Label(labelframe1, text="{} stop ul throughput\n".format(hostip[k].get()), font=('Mincho, 10')).pack(fill="both", expand="yes")

def send_dl_tput(k):
    cpecmd.cpe_send_dl_throughput(hostip=hostip[k].get(), thoughput=dltput[k].get())
    labelframe1 = ttk.LabelFrame(tab1, text='ue{} info'.format(k), height=200, width=500)  # 信息区
    labelframe1.grid(row=17, column=0, columnspan=7, padx=10, pady=10)
    labelframe1.propagate(0)  # 使组件大小不变，此时width才起作用
    ttk.Label(labelframe1, text="{} send dl throughput {}\n".format(hostip[k].get(), dltput[k].get()), font=('Mincho, 10')).pack(fill="both", expand="yes")

def stop_dl_tput(k):
    cpecmd.cpe_stop_dl_throughput(hostip=hostip[k].get())
    labelframe1 = ttk.LabelFrame(tab1, text='ue{} info'.format(k), height=200, width=500)  # 信息区
    labelframe1.grid(row=17, column=0, columnspan=7, padx=10, pady=10)
    labelframe1.propagate(0)  # 使组件大小不变，此时width才起作用
    ttk.Label(labelframe1, text="{} stop dl throughput\n".format(hostip[k].get()), font=('Mincho, 10')).pack(fill="both", expand="yes")

def get_dl_tput(k):
    try:
        dl_tput = cpe_get_current_throughput(host_ip=hostip[k].get(), direction='dl')
    except:
        dl_tput=cpecmd.cpe_get_current_throughput(host_ip=hostip[k].get(), direction='dl')
    labelframe2 = ttk.LabelFrame(tab1, text='ue{} Tput'.format(k),  height=200, width=300)
    labelframe2.grid(row=17, column=8, columnspan=5, padx=10, pady=10)
    labelframe2.propagate(0)
    if len(str(dl_tput))<4:
        ttk.Label(labelframe2, text="dl throughput:{}bit/s\n".format(dl_tput), font=('Mincho, 10')).pack(fill="both", expand="yes")
    elif len(str(dl_tput))>3 and len(str(dl_tput))<7:
        dl_tput=round(float(dl_tput/1000.00), 2)
        ttk.Label(labelframe2, text="dl throughput:{}Kbit/s\n".format(dl_tput), font=('Mincho, 10')).pack(fill="both", expand="yes")
    else:
        dl_tput = round(float(dl_tput/1000.00/1000.00), 2)
        ttk.Label(labelframe2, text="dl throughput:{}Mbit/s\n".format(dl_tput), font=('Mincho, 10')).pack(fill="both", expand="yes")


def get_ul_tput(k):
    try:
        ul_tput = cpe_get_current_throughput(host_ip=hostip[k].get(), direction='ul')
    except:
        ul_tput=cpecmd.cpe_get_current_throughput(host_ip=hostip[k].get(), direction='ul')
    labelframe2 = ttk.LabelFrame(tab1, text='ue{} Tput'.format(k),  height=200, width=300)
    labelframe2.grid(row=17, column=8, columnspan=5, padx=10, pady=10)
    labelframe2.propagate(0)
    if len(str(ul_tput))<4:
        ttk.Label(labelframe2, text="ul throughput:{}bit/s\n".format(ul_tput), font=('Mincho, 10')).pack(fill="both", expand="yes")
    elif len(str(ul_tput))>3 and len(str(ul_tput))<7:
        ul_tput=round(float(ul_tput/1000.00), 2)
        ttk.Label(labelframe2, text="ul throughput:{}Kbit/s\n".format(ul_tput), font=('Mincho, 10')).pack(fill="both", expand="yes")
    else:
        ul_tput = round(float(ul_tput/1000.00/1000.00), 2)
        ttk.Label(labelframe2, text="ul throughput:{}Mbit/s\n".format(ul_tput), font=('Mincho, 10')).pack(fill="both", expand="yes")

def get_all_ue_tput():
    ip_list = _parse_config_file_ip_list()
    str=_get_all_connect_ue_throughput(ip_list)
    labelframe2 = ttk.LabelFrame(tab1, text='all connect ue Tput', height=200, width=300)
    labelframe2.grid(row=17, column=8, columnspan=5, padx=10, pady=10)
    labelframe2.propagate(0)
    ttk.Label(labelframe2, text="{}\n{}".format(str, cpecmd.netspeed()), font=('Mincho, 10')).pack(fill="both", expand="yes")

def get_all_status():
    temp_list=[]
    ip_list = _parse_config_file_ip_list()
    for k, ip in enumerate(ip_list, start=1):
        try:
            lteMainStatusGet = _get_lte_info(hostip[k].get(), 'lteMainStatusGet')
            temp_list.append('ue{} ltestatus: {}\n'.format(k,lteMainStatusGet))
        except:
            temp_list.append('ue{} ltestatus: null\n'.format(k))
    str = "".join(temp_list)
    labelframe1 = ttk.LabelFrame(tab1, text='all ue status', height=200, width=500)
    labelframe1.grid(row=17, column=0, columnspan=7, padx=10, pady=10)
    labelframe1.propagate(0)
    ttk.Label(labelframe1, text="{}".format(str), font=('Mincho, 10')).pack(fill="both", expand="yes")


def cpe_get_current_throughput(host_ip, direction):
    tput = {'dl': 'systemDataRateDlCurrent',
            'ul': 'systemDataRateUlCurrent'}
    cpe_0 = cpe.CPE(host_ip)
    cpe_0.login()
    type_name=tput[direction]
    throughput=cpe_0.get_node_info(type_name)
    return int(throughput['items'][0][type_name])*8

def _get_all_connect_ue_throughput(ip_list):
    tput_list=[]
    for i, ip in enumerate(ip_list, start=1):
        try:
            dl_tput = cpe_get_current_throughput(host_ip=hostip[i].get(), direction='dl')
        except:
            dl_tput = cpecmd.cpe_get_current_throughput(host_ip=hostip[i].get(), direction='dl')
        dl_length= len(str(dl_tput))
        if dl_length<4:
            dl_tput='{}bit/s'.format(dl_tput)
        elif dl_length>3 and dl_length<7:
            dl_tput='{}Kbit/s'.format(round(float(dl_tput/1000.0), 2))
        else:
            dl_tput = '{}Mbit/s'.format(round(float(dl_tput/1000.0/1000.0), 2))
        try:
            ul_tput = cpe_get_current_throughput(host_ip=hostip[i].get(), direction='ul')
        except:
            ul_tput = cpecmd.cpe_get_current_throughput(host_ip=hostip[i].get(), direction='ul')
        ul_length = len(str(ul_tput))
        if ul_length<4:
            ul_tput='{}bit/s'.format(ul_tput)
        elif ul_length>3 and ul_length<7:
            ul_tput='{}Kbit/s'.format(round(float(ul_tput/1000.0), 2))
        else:
            ul_tput = '{}Mbit/s'.format(round(float(ul_tput/1000.0/1000.0), 2))
        tput_list.append('ue{} dl: {} ul: {}\n'.format(i, dl_tput, ul_tput))
    str_connect="".join(tput_list)
    return str_connect

def _get_lte_pci(hostip):
    return _get_lte_info(hostip, 'ltePciGet')

def _get_lte_info(hostip, typy_name):
    cpe_0 = cpe.CPE(hostip, 3)
    cpe_0.login()
    pci = cpe_0.get_node_info(typy_name)
    return pci['items'][0][typy_name]

def _get_lte_wanStatus(hostip):
    cpe_0 = cpe.CPE(hostip, 3)
    cpe_0.login()
    wanStatus=cpe_0.get_form_info('wanStatus')
    return wanStatus['items'][0]['apnIp']

def get_lte_status(k):
    lteMainStatusGet = _get_lte_info(hostip[k].get(), 'lteMainStatusGet')
    lteDlFrequencyGet=_get_lte_info(hostip[k].get(), 'lteDlFrequencyGet')
    lteUlFrequencyGet=_get_lte_info(hostip[k].get(), 'lteUlFrequencyGet')
    lteBandwidthGet=_get_lte_info(hostip[k].get(), 'lteBandwidthGet')
    lteRssi0Get=_get_lte_info(hostip[k].get(), 'lteRssi0Get')
    lteRsrp0Get=_get_lte_info(hostip[k].get(), 'lteRsrp0Get')
    lteRsrp1Get=_get_lte_info(hostip[k].get(), 'lteRsrp1Get')
    lteRsrq0Get=_get_lte_info(hostip[k].get(), 'lteRsrq0Get')
    ltePciGet = _get_lte_info(hostip[k].get(), 'ltePciGet')
    lteSinrGet = _get_lte_info(hostip[k].get(), 'lteSinrGet')
    lteTxpowerGet = _get_lte_info(hostip[k].get(), 'lteTxpowerGet')
    lteLockpcilistGet= _get_lte_info(hostip[k].get(), 'lteLockpcilistGet')
    ipaddress = _get_lte_wanStatus(hostip[k].get())
    labelframe3 = ttk.LabelFrame(tab1, text='ue{} status'.format(k), height=220, width=330)
    labelframe3.grid(row=17, column=13, rowspan=2, columnspan=5, padx=10, pady=10)
    labelframe3.propagate(0)
    ttk.Label(labelframe3, text="lteMainStatus:  {}\n"
                                "lteDlFrequency: {} MHz\n"
                                "lteUlFrequency: {} MHz\n"
                                "lteBandwidth:    {} MHz\n"
                                "lteRssi0:           {} dBm\n"
                                "lteRsrp0:          {} dBm\n"
                                "lteRsrp1:          {} dBm\n"
                                "lteRsrq0:          {} dB\n"
                                "ltePci:                {}\n"
                                "lteSinr:              {} dB\n"
                                "lteTxpower:      {} dBm\n"
                                "lteLockpcilist:    {}\n"
                                "IP Address:      {}\n"
              .format(lteMainStatusGet, lteDlFrequencyGet, lteUlFrequencyGet,
                      lteBandwidthGet, lteRssi0Get, lteRsrp0Get, lteRsrp1Get,
                      lteRsrq0Get, ltePciGet, lteSinrGet, lteTxpowerGet, lteLockpcilistGet, ipaddress)
              , font=('Mincho, 10')).pack(fill="both", expand="yes")

def callback():
    showinfo(title='4G_RAN_L2_HZH_SG11', message='version:6.6\n版权归4G_RAN_L2_HZH_SG11所有\n您的反馈，是我们前进的动力！\n')

def attach_all(ip_list):
    temp_list = []
    for k, ip in enumerate(ip_list, start=1):
        status=attach(k)
        temp_list.append('{} attach {}\n'.format(hostip[k].get(), status))
    temp = "".join(temp_list)
    showinfo(title='ue_attach', message=temp)

def detach_all(ip_list):
    temp_list = []
    for k, ip in enumerate(ip_list, start=1):
        status=detach(k)
        temp_list.append('{} detach {}\n'.format(hostip[k].get(), status))
    temp = "".join(temp_list)
    showinfo(title='ue_detach', message=temp)

def send_dl_tput_all(ip_list):
    temp_list = []
    for k in range(1, len(ip_list)+1):
        cpecmd.cpe_send_dl_throughput(hostip=hostip[k].get(), thoughput=dltput[k].get())
        temp_list.append('{} send dl tput success\n'.format(hostip[k].get()))
    temp = "".join(temp_list)
    showinfo(title='ul_throughput', message=temp)

def send_ul_tput_all(ip_list):
    temp_list=[]
    for k in range(1, len(ip_list) + 1):
        ul_thoughput = cpecmd.CPE_ul_thoughput(hostip[k].get())
        ul_thoughput.cpe_send_ul_throughput(ul_iperf_ip=targetip[k].get(), ul_iperf_tp=ultput[k].get())
        temp_list.append('{} send ul tput success\n'.format(hostip[k].get()))
    temp="".join(temp_list)
    showinfo(title='ul_throughput', message=temp)

def stop_dl_tput_all(ip_list):
    for ip in ip_list:
        cpecmd.cpe_stop_dl_throughput(hostip=ip)


def stop_ul_tput_all(ip_list):
    for ip in ip_list:
        ul_thoughput = cpecmd.CPE_ul_thoughput(ip)
        ul_thoughput.cpe_stop_ul_throughput()

def reboot_all(ip_list):
    for ip in ip_list:
        ul_thoughput = cpecmd.CPE_ul_thoughput(ip)
        ul_thoughput.cpe_reboot()

def main(ip_list):
    global root, tab1, tab2, earfcn, pci_entry, cqi, chosen, len_size
    root=Tk()
    root.wm_title('CPE')
    menuBar = Menu(root)
    root.config(menu=menuBar)
    fileMenu2 = Menu(menuBar)
    fileMenu2.add_command(label="attach_all", command=lambda: attach_all(ip_list))
    fileMenu2.add_command(label="detach_all", command=lambda: detach_all(ip_list))
    fileMenu2.add_command(label="send_dl_tput_all", command=lambda: send_dl_tput_all(ip_list))
    fileMenu2.add_command(label="stop_dl_tput_all", command=lambda: stop_dl_tput_all(ip_list))
    fileMenu2.add_command(label="send_ul_tput_all", command=lambda: send_ul_tput_all(ip_list))
    fileMenu2.add_command(label="stop_ul_tput_all", command=lambda: stop_ul_tput_all(ip_list))
    fileMenu2.add_command(label="reboot_all", command=lambda: reboot_all(ip_list))
    fileMenu2.add_command(label="clean_dead_iperf", command=lambda: del_dead_iperf_process(ip_list))
    menuBar.add_cascade(label="command", menu=fileMenu2)
    fileMenu3 = Menu(menuBar)
    fileMenu3.add_command(label="download pstool", command=collect_log.download_pstools)
    fileMenu3.add_command(label="collect ttitrace(5s local)", command=collect_log.capture_ttitrace_log_for_5s)
    fileMenu3.add_command(label="decode ttitrace", command=collect_log.decode_mac_ttitrace_2)
    fileMenu3.add_command(label="get key value of ttitrace", command=tract_key_value_from_ttitrace)
    fileMenu3.add_command(label="start collect btslog", command=collect_log.start_enb_systemlog)
    fileMenu3.add_command(label="stop collect btslog", command=collect_log.stop_enb_systemlog)
    menuBar.add_cascade(label="collect log", menu=fileMenu3)
    fileMenu1 = Menu(menuBar)
    fileMenu1.add_command(label="author", command=callback)
    menuBar.add_cascade(label="about", menu=fileMenu1)

    tabControl = ttk.Notebook(root)
    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text='Basic function')
    tabControl.grid()
    tab2 = ttk.Frame(tabControl)
    tabControl.add(tab2, text='Extended function')

    # root.geometry("1000x100+100+100")  # size+location_x+location_y
    # for i in range(1,num+1):
    #     frame_row(root, i)
    for i, ip in enumerate(ip_list, start=1):
        frame_row(tab1, i, ip)

    labelframe1 = ttk.LabelFrame(tab1, text='ue info', height=200, width=500)
    labelframe1.grid(row=17, column=0, columnspan=7, padx=10, pady=10)
    labelframe1.propagate(0)
    ttk.Label(labelframe1, text = "  ",font = ('Mincho, 10')).pack(fill="both", expand="yes")

    labelframe2 = ttk.LabelFrame(tab1, text='ue Tput', height = 200, width=300)
    labelframe2.grid(row=17, column=8, columnspan=5, padx=10, pady=10)
    labelframe2.propagate(0)
    ttk.Label(labelframe2, text = "  ",font = ('Mincho, 10')).pack(fill="both", expand="yes")

    labelframe3 = ttk.LabelFrame(tab1, text='ue status', height=200, width=300)
    labelframe3.grid(row=17, column=13, columnspan=5, padx=10, pady=10)
    labelframe3.propagate(0)
    ttk.Label(labelframe3, text="  ", font=('Mincho, 10')).pack(fill="both", expand="yes")
    Button(tab1, text='get_all_tput', command=get_all_ue_tput).grid(row=18, column=10)
    Button(tab1, text='status all', command=get_all_status).grid(row=18, column=1)

    Label(tab2, text='earfcn: ').grid(row=1, column=0, sticky=W)
    earfcn=Entry(tab2, text=" ")
    earfcn['width'] = 6
    earfcn.grid(row=1, column=1)
    e1 = StringVar()
    Label(tab2, text='PCI: ').grid(row=1, column=2)
    pci_entry=Entry(tab2, textvariable=e1)
    e1.set('-1')
    pci_entry['width'] = 4
    pci_entry.grid(row=1, column=3)
    for i, ip in enumerate(ip_list, start=1):
        checkbutton_row(tab2, i)
    Button(tab2, text='send_lockcell', width=10, command=send_lock_cell).grid(row=1, column=20)
    Button(tab2, text='send_unlockcell', width=12, command=send_unlock_cell).grid(row=1, column=21)
    Button(tab2, text='iperf.bat', width=10, command=iperf_file).grid(row=1, column=22)

    Label(tab2, text='override CQI: ').grid(row=2, column=0, sticky=W)
    e6 = StringVar()
    cqi = Entry(tab2, textvariable=e6)
    cqi['width'] = 3
    cqi.grid(row=2, column=1)
    Label(tab2, text='range(0~15)', fg='grey').grid(row=2, column=2, columnspan=3)
    Button(tab2, text='override_CQI', width=10, command=override_cqi).grid(row=2, column=20)

    Label(tab2, text='remote ip: ').grid(row=3, column=0, sticky=W)
    e7 = StringVar()
    chosen = ttk.Combobox(tab2, width=2, textvariable=e7)
    chosen['values']= _parse_config_file_remoteip()
    chosen['width'] = 13
    chosen.grid(row=3, column=1, columnspan=3, sticky=W)
    Button(tab2, text='check_netspeed', width=11, command=remote_netspeed).grid(row=3, column=2, columnspan=18, sticky=E)
    Button(tab2, text='send_iperf', width=10, command=remote_send_iperf).grid(row=3, column=20)
    e8 = StringVar()
    e8.set('1400B')
    len_size = Entry(tab2, textvariable=e8)
    len_size['width'] = 7
    len_size.grid(row=3, column=21, sticky=W)
    Label(tab2, text='#len size', fg='grey').grid(row=3, column=21, sticky=E)
    Button(tab2, text='stop_iperf', width=10, command=kill_remote_iperf).grid(row=3, column=22)

    #root.iconbitmap('phone.ico')
    root.resizable(width=False, height=False)
    root.mainloop()

def checkbutton_row(root, i):
    var[i] = IntVar()
    c1 = Checkbutton(root, text="ue{}".format(i), variable=var[i])
    c1.select()
    c1.grid(row=1, column=i+4)

def tract_key_value_from_ttitrace():
    cur_path = os.path.abspath(os.curdir)
    save_log_path = os.path.join(cur_path, 'tti')
    import glob
    csv_list = glob.glob(os.path.join(save_log_path, '*.csv'))
    if len(csv_list)>0:
        handle_data.tract_key_value_from_ttitrace(save_log_path)

def send_lock_cell():
    select_list=[]
    for i, ip in enumerate(ip_list, start=1):
        if var[i].get() == 1:
            select_list.append(hostip[i].get())
    if len(select_list):
        for ip in select_list:
            cpecmd.send_lockcell_command(host_ip=ip, earfcn=earfcn.get(), pci=pci_entry.get())

def send_unlock_cell():
    select_list=[]
    for i, ip in enumerate(ip_list, start=1):
        if var[i].get() == 1:
            select_list.append(hostip[i].get())
    if len(select_list):
        for ip in select_list:
            cpecmd.send_lockcell_command(host_ip=ip, earfcn=0, pci=0)



def iperf_file():
    select_list = []
    cmd_list=[]
    for i, host_ip in enumerate(ip_list, start=1):
        if var[i].get() == 1:
            select_list.append(host_ip)
            try:
                ip_address=_get_lte_wanStatus(hostip=hostip[i].get())
            except:
                ip_address = cpecmd.get_cpe_ipaddr(host_ip=hostip[i].get())
            dtput=dltput[i].get()
            if ip_address:
                iperf_cmd = 'start iperf.exe -c {} -u -P 1 -i 1 -p 54{}0 -l 1400.0B -f k -b {} -t 7200 -T 1\n'.format(ip_address, i, dtput)
                cmd_list.append(iperf_cmd)
    with open('iperf_start.bat', "w") as f:
        f.writelines(cmd_list)
    f.close()

def override_cqi():
    select_list=[]
    for i, ip in enumerate(ip_list, start=1):
        if var[i].get() == 1:
            select_list.append(ip)
    if len(select_list):
        for ip in select_list:
            cpecmd.override_cqi(host_ip=ip, cqi_value=cqi.get())

def remote_netspeed():
    sys_ip=chosen.get()
    speed=ssh_command.get_netspeed(sys_ip)
    labelframe4 = ttk.LabelFrame(tab2, text='remote pc netspeed', height=60, width=300)
    labelframe4.grid(row=1, column=25, rowspan=3, padx=10, pady=10, sticky=N)
    labelframe4.propagate(0)
    ttk.Label(labelframe4, text="{}".format(speed), font=('Mincho, 10')).pack(fill="both", expand="yes")

def remote_send_iperf():
    sys_ip = chosen.get()
    for i, host_ip in enumerate(ip_list, start=1):
        if var[i].get() == 1:
            try:
                ip_address = _get_lte_wanStatus(hostip=hostip[i].get())
            except:
                ip_address = cpecmd.get_cpe_ipaddr(host_ip=hostip[i].get())
            dtput = dltput[i].get()
            if ip_address:
                ssh_command.send_iperf_data_via_remoteip(sys_ip, active_s1_ip=ip_address, trans_data=dtput, len_size=len_size.get())

def kill_remote_iperf():
    sys_ip = chosen.get()
    for i, host_ip in enumerate(ip_list, start=1):
        if var[i].get() == 1:
            try:
                ip_address = _get_lte_wanStatus(hostip=hostip[i].get())
            except:
                ip_address = cpecmd.get_cpe_ipaddr(host_ip=hostip[i].get())
            if ip_address:
                ssh_command.kill_inactive_iperf(sys_ip, inactive_s1_ip=ip_address)


def frame_row(root, i,ip):
    Label(root, text='ue{}_ip: '.format(i)).grid(row=int(i), column=0, sticky=W)
    e1 = StringVar()
    hostip[i] = Entry(root, textvariable=e1)
    e1.set('{}'.format(ip))
    hostip[i].grid(row=int(i), column=1)
    hostip[i]['width'] = 13
    Button(root, text='attach', activeforeground='Green', command=lambda: attach(i)).grid(row=int(i), column=2)
    Button(root, text='detach', command=lambda: detach(i)).grid(row=int(i), column=3)
    Label(root, text='target_ip: ').grid(row=int(i), column=4)
    e2 = StringVar()
    targetip[i] = Entry(root, textvariable=e2)
    e2.set(_parse_config_file_default_value('default_ultarget_ip'))
    targetip[i].grid(row=int(i), column=5)
    targetip[i]['width'] = 13
    Label(root, text='send_ul_tput: ').grid(row=int(i), column=6)
    e3 = StringVar()
    ultput[i] = Entry(root, textvariable=e3)
    e3.set(_parse_config_file_default_value('default_ul_thp'))
    ultput[i].grid(row=int(i), column=7)
    ultput[i]['width'] = 4
    Button(root, text='ul_send_tput', command=lambda: send_ul_tput(i)).grid(row=int(i), column=8)
    Button(root, text='ul_stop', command=lambda: stop_ul_tput(i)).grid(row=int(i), column=9)
    Label(root, text='send_dl_tput: ').grid(row=int(i), column=10)
    e4 = StringVar()
    dltput[i] = Entry(root, textvariable=e4)
    e4.set(_parse_config_file_default_value('default_dl_thp'))
    dltput[i].grid(row=int(i), column=11)
    dltput[i]['width'] = 4
    Button(root, text='dl_send_tput', command=lambda: send_dl_tput(i)).grid(row=int(i), column=12)
    Button(root, text='dl_stop', command=lambda: stop_dl_tput(i)).grid(row=int(i), column=13)
    Button(root, text='get_dl_tput', command=lambda: get_dl_tput(i)).grid(row=int(i), column=14)
    Button(root, text='get_ul_tput', command=lambda: get_ul_tput(i)).grid(row=int(i), column=15)
    Button(root, text='get_ue{}_status'.format(i), command=lambda: get_lte_status(i)).grid(row=int(i), column=16)

def del_dead_iperf_process(ip_list):
    active_ip_list=[]
    for ip in ip_list:
        active_ip=_get_lte_wanStatus(ip)
        active_ip_list.append(active_ip)
    iperfip_list = []
    lines = os.popen("ps -ef| grep iperf").read().splitlines()
    for line in lines:
        ip = re.findall('iperf -c (\d+\.\d+\.\d+\.\d+)', line)
        if ip:
            iperfip_list.append(ip[0])
    iperfip_list = list(set(iperfip_list))
    if active_ip_list:
        for element in active_ip_list:
            try:
                iperfip_list.remove(element)
            except:
                pass
    dead_ip_list=iperfip_list
    lines = os.popen("ps -ef| grep iperf").read().splitlines()
    for line in lines:
        for ip in dead_ip_list:
            if ip in line :
                pid = re.findall('ute\s+(\d+)\s.+iperf \-c {}'.format(ip), line)[0]
                os.system("sudo kill -9 %s" % pid)

def _parse_config_file_ip_list():
    ip_list=[]
    config=ConfigParser.ConfigParser()
    config.read('config.ini')
    for option in config.options('ip_list'):
        if '{}'.format(config.get('ip_list', option)) !='':
            ip_list.append(config.get('ip_list', option))
    return ip_list

def _parse_config_file_remoteip():
    remote_list = []
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    for option in config.options('remote_ip'):
        if '{}'.format(config.get('remote_ip', option)) != '':
            remote_list.append(config.get('remote_ip', option))
    remote_str=" ".join(remote_list)
    return remote_str

def _parse_config_file_default_value(key):
    default_value={}
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    for option in config.options('default_value'):
        default_value[option]=config.get('default_value', option)
    return default_value.get(key)

if __name__ == '__main__':
    ip_list = _parse_config_file_ip_list()
    main(ip_list)
    pass



