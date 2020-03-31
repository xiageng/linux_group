#---code: utf-8 ---

import sys, re
import requests
import os, shutil
from ute_admin import ute_admin
import static_para
import subprocess

target_bd = static_para.target_bd
ute_admin = ute_admin()

def login():
    print 'Login...'
    try:
        ute_admin.setup_admin(bts_host="192.168.255.1", bts_port=3600, use_ssl=True)
        print 'QT_status: Login Pass'
    except Exception, e:
        print 'QT_status: Login Fail'
        print 'QT_report: Login Fail because {}'.format(e)
        sys.exit(e)

def teardown():
    ute_admin.teardown_admin()
    print 'QT_status: TearDown Pass'

def get_sw_info():
    version = ute_admin.get_software_info()
    active_ver = version['Active SW version']
    active_ver = active_ver.replace("TL19A", "TL00")
    return active_ver

def download_package(target_bd):
    if os.path.isfile('/opt/TtiTracer/pstools.zip'):
        os.remove('/opt/TtiTracer/pstools.zip')
    url_wft = 'https://wft.int.net.nokia.com/ext/build_content/{}'.format(target_bd)
    try:
        r = requests.get(url_wft, stream=True)
        pstool_filter = r'<file title=".*pstools.zip" url="(.*?)">'
        url_pstool_download = re.findall(pstool_filter,r.content)[0]
        print "Start download pstools"
        cmd = "wget -q -P /opt/TtiTracer/ " + url_pstool_download
        os.system(cmd)
        if os.path.isfile('/opt/TtiTracer/pstools.zip'):
            if os.path.isdir('/opt/TtiTracer/pstools/'):
                shutil.rmtree('/opt/TtiTracer/pstools')
            os.system("unzip -qo /opt/TtiTracer/pstools.zip -d /opt/TtiTracer/")
    except requests.exceptions.RequestException as e:
        print 'download pstools Fail'
        print e
def  extra_zip():
    os.system("rm -rf /opt/TtiTracer/pstools")
    os.system("rm -f /opt/TtiTracer/*.zip")
    cmd = "ls -t /opt/TtiTracer/*.zip |head -n 1"
    child =subprocess.Popen(cmd,shell='True', stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    file = child.stdout.read().strip()
    print("in /opt/TtiTracer folder the newest file is :",file)
    cmd_unzip="unzip -qo " + file+" -d /opt/TtiTracer/pstools"
    print cmd_unzip
    os.system(cmd_unzip)

if __name__ == "__main__":
    #login()
    #target_bd = get_sw_info()
    #teardown()
    if target_bd:
        print target_bd
        download_package(target_bd)
    else:
        print "package_name: No softwoare build and no need download pstools"

    extra_zip()
