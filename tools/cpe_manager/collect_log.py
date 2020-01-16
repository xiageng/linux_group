# -*- coding: utf-8 -*-
"""
:copyright: Nokia
:author: zhang wenchao
:maintainer: None
:contact: None
"""

from ute_fsmaccess import ute_fsmaccess
access=ute_fsmaccess()
import re
import requests
import zipfile
import os
import pandas
import logging
import subprocess as sp

proxies = {'http': '10.144.1.10:8080',
           'https': '10.144.1.10:8080'}
def _get_targetbd_version():
    access.setup_enb_fsm_access(alias='tdb')
    version=access.get_enb_sw_version(alias='tdb')
    access.teardown_enb_fsm_access(alias='tdb')
    if '_9999_' in version:
        head_version=version.split('_')[0]
        real_head=re.findall('(\D+)\d+', head_version)
        version=version.replace(head_version, '{}00'.format(real_head[0]))
    return version

def _download_pstool():
    target_bd=_get_targetbd_version()
    url_ute_cloud = 'http://files.ute.inside.nsn.com/builds/enb/base/{}/pstools.zip'.format(target_bd)
    r = requests.get(url_ute_cloud, stream=True)
    if r.status_code == 200:
        save_sw_with_progress(r, '/tmp/pstools.zip')
        _unzip_file()
        os.system('chmod +x /opt/TtiTracer/pstools/TtiTracer/onlineTtiStream/onlineTtiStream')
        os.system('chmod +x /opt/TtiTracer/pstools/TtiTracer/DevC_tti_trace_parser')
    else:
        print r.status_code

def _download_pstool2():
    target_bd=_get_targetbd_version()
    wft_web = 'https://wft.int.net.nokia.com/ext/build_content/{}'.format(target_bd)
    r = requests.get(wft_web, stream=True, proxies=proxies)
    if r.status_code == 200:
        pattern='(http\:\/\/hz.+pstools\.zip)\"'
        url_pstool=re.findall(pattern, r.content)
        download_addr=url_pstool[0]
        logging.info('download address is {}'.format(download_addr))
        r1=requests.get(download_addr, stream=True)
        if r1.status_code == 200:
            save_sw_with_progress(r1, '/tmp/pstools.zip')
            _unzip_file()
            os.system('chmod +x /opt/TtiTracer/pstools/TtiTracer/onlineTtiStream/onlineTtiStream')
            os.system('chmod +x /opt/TtiTracer/pstools/TtiTracer/DevC_tti_trace_parser')
        else:
            print r1.status_code
    else:
        print r.status_code

def download_pstools():
    _download_pstool2()

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
                    print 'Downloading progress {}%'.format(done)
                    last_done = done
    print 'Downloading finished !'


def _unzip_file():
    import shutil
    if os.path.exists('/opt/TtiTracer/pstools/'):
        shutil.rmtree('/opt/TtiTracer/pstools/')
    zip_file=zipfile.ZipFile('/tmp/pstools.zip', 'r')
    zip_file.extractall('/opt/TtiTracer/')
    zip_file.close()

def _get_mac():
    cmd='/opt/TtiTracer/pstools/TtiTracer/onlineTtiStream/onlineTtiStream -f'
    response = os.popen(cmd)
    return response

def _convert_data():
    data=[]
    for line in _get_mac().readlines():
        if len(line.split())>10:
            if 'lnCel' in line.split()[1:]:
                title=line.split()[1:]
            else:
                data.append(line.split()[1:])
    df=pandas.DataFrame(data, columns=title)
    logging.info(df.filter(regex=("lnCel|MACULTTI|MACDLTTI")))
    return df.filter(regex=("lnCel|MACULTTI|MACDLTTI"))

def get_mac_tti_address(cell="ALL", node_type='ALL'):
    macultti = 'MACULTTI'
    macdltti = 'MACDLTTI'
    value_list = []
    df=_convert_data()
    if node_type=='ALL':
        if cell=='ALL':
            for element in df.filter(regex=("MACULTTI|MACDLTTI")).to_dict('index').values():
                value_list.append(element[macultti])
                value_list.append(element[macdltti])
        else:
            for element in df.to_dict('index').values():
                if element['lnCel']==cell:
                    value_list.append(element[macultti])
                    value_list.append(element[macdltti])
    elif node_type==macultti:
        if cell=='ALL':
            for element in df.filter(regex=("MACULTTI|MACDLTTI")).to_dict('index').values():
                value_list.append(element[macultti])
        else:
            for element in df.to_dict('index').values():
                if element['lnCel']==cell:
                    value_list.append(element[macultti])
    elif node_type==macdltti:
        if cell=='ALL':
            for element in df.filter(regex=("MACULTTI|MACDLTTI")).to_dict('index').values():
                value_list.append(element[macdltti])
        else:
            for element in df.to_dict('index').values():
                if element['lnCel']==cell:
                    value_list.append(element[macdltti])
    return value_list

def _kill_15003_process():
    lines = os.popen("sudo netstat -anp | grep 15003").read().splitlines()
    for line in lines:
        if "Stream" in line:
            pid = line.split()[-1].split('/')[0]
            os.system("kill -9 %s" % pid)

def _start_ttitrace(dsp_id_group, save_log_path):
    sicftp_path='/opt/TtiTracer/pstools/TtiTracer/onlineTtiStream/onlineTtiStream'
    download_cmd = "%s -c %s -o \"%s%s%s\"" % (sicftp_path,
                                                  dsp_id_group,
                                                  save_log_path,
                                                  os.sep, os.sep)
    logging.info(download_cmd)
    process_obj = sp.Popen(download_cmd,
                           stdin=sp.PIPE,
                           shell=True,
                           stdout=sp.PIPE,
                           stderr=sp.PIPE)
    return process_obj

def start_capture_ttitrace(save_log_path, cell_id="ALL"):
    import shutil
    mac=[]
    mac_address_8bit = get_mac_tti_address(cell=cell_id)
    logging.info(mac_address_8bit)
    for element in mac_address_8bit:
        mac.append(element[2:6])
    mac=list(set(mac))
    mac_address=','.join(mac)
    if os.path.exists(save_log_path):
        shutil.rmtree(save_log_path)
    os.mkdir(save_log_path)
    obj = _start_ttitrace(mac_address,
                         save_log_path
                         )
    logging.info(os.popen("sudo netstat -anp | grep 15003").read())
    return obj, save_log_path

def stop_capture_ttitrace(process_obj):
    logging.info(os.popen("sudo netstat -anp | grep 15003").read())
    process_obj.stdin.write(os.linesep)
    logging.info(os.popen("sudo netstat -anp | grep 15003").read())
    process_obj.kill()

def capture_ttitrace_log_for_5s():
    cur_path = os.path.abspath(os.curdir)
    save_log_path=os.path.join(cur_path, 'tti')
    process_obj1, save_log_path = start_capture_ttitrace(save_log_path, cell_id="ALL")
    import time
    time.sleep(5)
    stop_capture_ttitrace(process_obj=process_obj1)

def decode_mac_ttitrace_2():
    cur_path = os.path.abspath(os.curdir)
    save_log_path = os.path.join(cur_path, 'tti')
    decode_mac_ttitrace(save_log_path)

def decode_mac_ttitrace(save_log_path):
    tti_trace_parser = "DevC_tti_trace_parser"
    pstools_for_ta = '/opt/TtiTracer/pstools/TtiTracer/'
    decode_path=os.path.join(pstools_for_ta, tti_trace_parser)
    if not os.path.exists(decode_path):
        try:
            _download_pstool()
        except:
            logging.warning("download pstools failed !")
    else:
        ttitrace_parser_tool = decode_path
    if not os.path.exists(save_log_path):
        raise Exception("log folder is not exist in %s" % save_log_path)
    import glob
    dat_list = glob.glob(os.path.join(save_log_path, '*.dat'))
    if not dat_list:
        raise Exception("not find any .dat files, nothing can be decode")
    for dat_file in dat_list:
        decode_cmd = "%s \"%s\" \"%s\" " % (ttitrace_parser_tool,
                                            dat_file,
                                            dat_file.replace(".dat", ".csv")
                                            )
        logging.info("Execute command: '%s'" % decode_cmd)

        ret = os.popen(decode_cmd).read()
        logging.info(ret)
        os.system('rm -rf {}/*.csv.harq'.format(save_log_path))

def start_enb_systemlog():
    stop_enb_systemlog()
    import shutil
    cur_path = os.path.abspath(os.curdir)
    save_log_path = os.path.join(cur_path, 'btslog')
    if os.path.exists(save_log_path):
        shutil.rmtree(save_log_path)
    os.mkdir(save_log_path)
    command_path=os.path.join(os.getcwd(), 'fsyslog')
    if os.path.exists(command_path):
        cmd='{} --max-log-size 100000000 --log-dir {}' \
            ' --ipaddr 192.168.255.126'\
            .format(command_path, save_log_path)
        os.system(cmd)
    else:
        print "current file not exists fsyslog command"

def stop_enb_systemlog():
    lines = os.popen("ps -ef | grep fsyslog").read().splitlines()
    for line in lines:
        if "192.168.255.126" in line:
            pid = line.split()[1]
            os.system("kill -9 %s" % pid)

