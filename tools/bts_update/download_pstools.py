#---code: utf-8 ---

import sys, re
import requests
import os,shutil
import static_para
import subprocess
import zipfile

target_bd = static_para.target_bd

def download_package(target_bd):
    os.system("rm -rf /opt/TtiTracer/*pstools.zip*")
    url_wft = 'https://wft.int.net.nokia.com/ext/build_content/{}'.format(target_bd)
    try:
        r = requests.get(url_wft, stream=True)
        pstool_filter = r'<file title=".*pstools.zip" url="(.*?)">'
        url_pstool_download = re.findall(pstool_filter,r.content)[0]
        print "Start download pstools"
        cmd = "wget -q -P /opt/TtiTracer/ " + url_pstool_download
        os.system(cmd)
    except requests.exceptions.RequestException as e:
        print 'download pstools Fail'
        print e
def  extra_zip():
    if os.path.isdir("/opt/TtiTracer/pstools"):
        shutil.rmtree("/opt/TtiTracer/pstools")
    cmd = "ls -t /opt/TtiTracer/*.zip |head -n 1"
    child =subprocess.Popen(cmd,shell='True', stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    file = child.stdout.read().strip()
    if file.endswith(".zip"):
        print("unzip pstools.zip file:%s"%file)
        zipfile.ZipFile(file).extractall("/opt/TtiTracer/pstools")
        os.remove(file)

if __name__ == "__main__":
    #login()
    #target_bd = get_sw_info()
    #teardown()
    if target_bd:
        print target_bd
        download_package(target_bd)
        extra_zip()
    else:
        print "package_name: No softwoare build and no need download pstools"
