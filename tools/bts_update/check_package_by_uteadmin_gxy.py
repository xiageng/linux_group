# -*- coding: utf-8 -*-
from ute_admin import ute_admin
from ta_kiss_bts import ta_kiss_bts
from ute_fsmaccess import ute_fsmaccess
from ute_admin_infomodel import ute_admin_infomodel

import time
import requests
import re
import sys
import os,subprocess
import static_para


ute_admin = ute_admin()
ta_kiss_bts = ta_kiss_bts()
ute_fsmaccess = ute_fsmaccess()
infomodel= ute_admin_infomodel()
proxies = static_para.proxies
target_bd = static_para.target_bd
cell_num = static_para.cell_num
reset_time = static_para.reset_time
host = static_para.host
proxy_flag = static_para.proxy_flag


def login():
    print 'Login...'
    try:
        ute_admin.setup_admin(bts_host=host, bts_port=3600, use_ssl=True)
        print 'QT_status: Login Pass'
    except Exception, e:
        print 'QT_status: Login Fail'
        print 'QT_report: Login Fail because {}'.format(e)
        sys.exit(e)


def teardown():
    ute_admin.teardown_admin()
    print 'QT_status: TearDown Pass'


def update_sw():
    if check_sw():
        print 'the current sw is {} already, will not update'.format(target_bd)
    else:
        sw_path = './BTSSW/'
        sw_package = sw_path + target_bd + '_release_BTSSM_downloadable.zip'
        print 'Updating...'
        try:
            ute_admin.update_software(sw_package)
            reset_finish_flag = wait_after_reset()
            if reset_finish_flag:
                for idx in xrange(30):
                    try:
                        sw_flag = check_sw()
                        print 'is package active: {}'.format(sw_flag)
                        if sw_flag:
                            print 'QT_status: Update_SW Pass'
                            break
                        else:
                            time.sleep(20)
                    except Exception, e:
                        print e
                        time.sleep(20)
                print 'QT_status: BTS_Reset_1 Pass'
            else:
                print 'QT_status: BTS_Reset_1 Fail'
        except Exception, e:
            print e
            print 'QT_status: Update_SW Fail'
            teardown()
            sys.exit(e)


def check_sw():
    version = ute_admin.get_software_info()
    active_ver = version['Active SW version']
    if target_bd.split('_', 1)[1] in active_ver:
        return True
    else:
        return False


def download_sw():
    sw_path = './BTSSW/'
    file_name = sw_path + target_bd + '_release_BTSSM_downloadable.zip'
    url_wft = 'https://wft.int.net.nokia.com/ext/build_content/{}'.format(target_bd)
    print "Downloading %s" % file_name
    try:
        r = requests.get(url_wft, stream=True, proxies=proxies)
        sw_name = r'<file title="' + target_bd + '_release_BTSSM_downloadable.zip" url="(.*?)">'
        url_download_sw = re.findall(sw_name, r.content)[0]
        print url_download_sw
        if proxy_flag == '1':
            r = requests.get(url_download_sw, stream=True, proxies=proxies)
        else:
            r = requests.get(url_download_sw, stream=True)
        if r.status_code == 200:
            save_sw_with_progress(r, file_name)
            print 'QT_status: Download_SW Pass'
        else:
            print 'QT_status: Download_SW Fail'
            print r.status_code
    except requests.exceptions.RequestException as e:
        print 'QT_status: Download_SW Fail'
        print e

def cmd_excute_process(cmd):
    process = subprocess.Popen(cmd,shell= True,stdout = subprocess.PIPE,stderr=subprocess.STDPUT)
    return_code = process.returncode
    process.communicate()
    return return_code
def get_url_download_sw(search_re):
    url_download_sw=''
    if os.path.isfile('./url_wft.html'):
        with open('./url_wft.html','rb') as handler:
            data = handler.read()
            url_download_sw = re.findall(search_re,data)[0]
            handler.close()
    return url_download_sw

def download_sw_127():
    sw_path = './BTSSW/'
    file_name = sw_path + target_bd + '_release_BTSSM_downloadable.zip'
    url_wft = 'https://wft.int.net.nokia.com/ext/build_content/{}'.format(target_bd)
    print "Downloading %s" % file_name
    if proxy_flag == '1':
        url_wft_cmd = "sshpass -p ute ssh ute@10.106.214.127 -o StrictHostKeyChecking=no curl -x " + proxies['https'] + ' ' + url_wft + '> ./url_wft.html'
    else:
        url_wft_cmd = 'sshpass -p ute ssh ute@10.106.214.127 -o StrictHostKeyChecking=no curl ' + url_wft + ' >./url_wft.html'
    cmd_excute_process(url_wft_cmd)
    sw_name = r'<file title="' + target_bd + '_release_BTSSM_downloadable.zip" url="(.*?)">'
    url_download_sw = get_url_download_sw(sw_name)
    print url_download_sw
    download_cmd = 'sshpass -p ute ssh ute@10.106.214.127 -o StrictHostKeyChecking=no wget -P /home/ute/xiageng/package/BTSSW ' + url_download_sw
    cmd_excute_process(download_cmd)
    copy_command = 'sshpass -p ute scp ute@10.106.214.127:/home/ute/xiageng/package/BTSSW/' + target_bd + '_release_BTSSM_downloadable.zip ./BTSSW/'
    os.system(copy_command)

    # try:
    #     r = requests.get(url_wft, stream=True, proxies=proxies)
    #     sw_name = r'<file title="' + target_bd + '_release_BTSSM_downloadable.zip" url="(.*?)">'
    #     url_download_sw = re.findall(sw_name, r.content)[0]
    #     print url_download_sw
    #     if proxy_flag == '1':
    #         r = requests.get(url_download_sw, stream=True, proxies=proxies)
    #     else:
    #         r = requests.get(url_download_sw, stream=True)
    #     if r.status_code == 200:
    #         save_sw_with_progress(r, file_name)
    #         print 'QT_status: Download_SW Pass'
    #     else:
    #         print 'QT_status: Download_SW Fail'
    #         print r.status_code
    # except requests.exceptions.RequestException as e:
    #     print 'QT_status: Download_SW Fail'
    #     print e

def save_sw_with_progress(r, file_name):
    total_length = r.headers.get('content-length')
    with open(file_name, "wb") as f:
        if total_length is None:
            f.write(r.content)
        else:
            dl = 0
            last_done = 0
            total_length = int(total_length)
            for data in r.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = round(dl/float(total_length), 2)*100
                if done-last_done > 2:
                    print 'Dowdloading progress {}%'.format(done)
                    last_done = done
                # sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                # sys.stdout.flush()


def reset_site(reset_result):
    for i in xrange(int(reset_time)):
        print '---{} reset site---'.format(i+1)
        ute_admin.reset_site()
        print 'QT_status: BTS_Reset_{} Pass'.format(i+2)
        onair_flag = check_onair()
        status_flag = 'Pass' if onair_flag else 'Fail'
        print 'QT_status: Check_Onair_{} {}'.format(i+2, status_flag)
        reset_result.append(onair_flag)
    return reset_result


def check_onair():
    cell_flag = False
    try:
        infomodel.setup_infomodel(address=host, port=3600, use_ssl=True)
        infomodel.connect_infomodel()
        for idx in xrange(90):
            print '{} check on air...'.format(idx + 1)
            bts_status = infomodel.get_infomodel_object(dist_name='/MRBTS-1/RAT-1/MCTRL-*/BBTOP_M-1/MRBTS_M-*')
            bts_flag = bts_status['stateInfo']['proceduralState']
            print "bts status is {}".format(bts_flag)
            if bts_flag == 'OnAir':
                try:
                    IM_CELL_ONAIR = '/MRBTS-1/RAT-1/MCTRL-*/BBTOP_M-1/MRBTS_M-1/LNBTS_M-1/CELL_M-* is [stateInfo.proceduralState=regex"[oO]nAir"]'
                    cell_get_count = infomodel.query_infomodel(query='get count '+IM_CELL_ONAIR)
                    print "{} cell is on air".format(cell_get_count)
                    if cell_get_count == int(cell_num):
                        cell_flag = True
                        break
                except Exception, e:
                    print '=====cell exception======'
                    print e
            time.sleep(10)
        infomodel.disconnect_infomodel()
    except Exception, e:
        print '=====infomodel exception====='
        print e
        print "infomodel setup failed!"
    finally:
        infomodel.teardown_infomodel()
        return cell_flag


def sucess_rate(reset_result):
    sucess = reset_result.count(True)
    fail = reset_result.count(False)
    total = sucess + fail
    sucess_rate = format(round(sucess/float(total), 2), '.0%')
    print 'QT_report: Package Name: {}'.format(target_bd)
    print 'QT_report: Reset site: {} times'.format(total)
    print 'QT_report: Sucess: {} times, Fail: {} times'.format(sucess, fail)
    print 'QT_report: Sucess rate: {}'.format(sucess_rate)


class Unbuffered(object):
    def __init__(self, stream):
       self.stream = stream

    def write(self, data):
       self.stream.write(data)
       self.stream.flush()

    def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def abort_sw():
    ute_admin.abort_software_update()


def reset_admin():
    ute_admin.reset_admin()


def wait_after_reset():
    host1 = '192.168.255.129'
    host2 = host
    reset_finish_flag = False
    for idx in xrange(90):
        try:
            ute_fsmaccess.wait_until_host_is_available(host1)
            ute_fsmaccess.wait_until_host_is_available(host2)
            reset_finish_flag = True
            break
        except Exception, e:
            time.sleep(10)
    return reset_finish_flag


def rollback_software():
    ute_admin.rollback_software()


if __name__ == "__main__":
    sys.stdout = Unbuffered(sys.stdout)
    print 'cell_num: {}'.format(cell_num)
    print 'reset_time: {}'.format(reset_time)
    print 'host: {}'.format(host)
    print 'proxy_flag: {}'.format(proxy_flag)
    if target_bd:
        print 'package_name: ' + target_bd
        download_sw_127()
        sys.exit(0)
        login()
        update_sw()
        onair_flag = check_onair()
        if not onair_flag:
            print 'QT_report: Site not on air after updating to {}!'.format(target_bd)
            print 'QT_report: This package is not recommended!'
            status_flag = 'Pass' if onair_flag else 'Fail'
            print 'QT_status: Check_Onair_1 {}'.format(status_flag)
        else:
            reset_result = [onair_flag, ]
            reset_result = reset_site(reset_result)
            sucess_rate(reset_result)
        teardown()
    else:
        print 'package_name: No software build'
        print 'QT_report: There is no software build for this date!'



