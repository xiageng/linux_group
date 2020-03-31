#---code: utf-8 ---
from __future__ import print_function
import argparse
import sys, re
import requests,urllib
import os,socket
import datetime
import zipfile

socket.setdefaulttimeout(600)
def report_hook(bk_num, bk_size, total_size):
    per = 100 * bk_num * bk_size / total_size
    if per%2:
        print("\r" + "Download progress:%d%%" % per, end="")
        #print("\r" + "Download progress:%s%d%%" % (">" * int(50*bk_num * bk_size / total_size), per), end="")

class SWPackage(object):
    def __init__(self,pk_name,pk_branch,pk_date):
        self.pk_name = pk_name
        self.pk_date = pk_date
        self.pk_branch = pk_branch
        self.cur_abs_path = os.path.curdir
        self.preparedir()

    def preparedir(self):
        if not os.path.isdir('./btssw'):
            os.mkdir('btssw')
        self.pk_file = os.path.join(self.cur_abs_path + '/btssw',self.pk_name + "_release_BTSSM_downloadable_A53.zip")
        self.pstools_file = os.path.join(self.cur_abs_path + '/btssw', self.pk_name + "_pstools.zip")

    def download_package_name(self):
        url_wft = 'https://wft.int.net.nokia.com/ext/build_content/{}'.format(self.pk_name)
        url_sw,url_pstool = self.__parse_download_url(url_wft)
        print("Start download bts sw package:")
        self.download_file(url_sw,self.pk_file)
        print("Start download pstools.zip file:")
        self.download_file(url_pstool, self.pstools_file)

    def download_files(self,file_url,file_name):
        try:
            r = requests.get(file_url,stream=True)
            if r.status_code == 200:
                print("Start download files: %s" % file_name)
                total_length = int(r.headers.get("content-length"))
                with open(file_name,"wb") as f:
                    if total_length is None:
                        f.write(r.content)
                    else:
                        done=0
                        for chunk in r.iter_content(chunk_size=4096):
                            #done_ratio = round(done/float(total_length),2)*100
                            if chunk:
                                done = done + len(chunk)
                                f.write(chunk)
                                print("\r" + "Dowdloading progress:%s%.2f%%" % (">"*int(done*50/total_length),float(done*100/total_length)),end="")
        except requests.exceptions.RequestException as e:
            print("download_status: get package and pstools files Fail")
            print("error:%s", e)

    def download_file(self,file_url,file_name):
        urllib.urlretrieve(file_url,file_name,reporthook=report_hook)

    def __parse_download_url(self,url_wft):
        try:
            r = requests.get(url_wft,stream=True)
            sw_name = r'<file title="' + self.pk_name + '_release_BTSSM_downloadable_A53.zip" url="(.*?)">'
            url_download_sw = re.findall(sw_name, r.content)[0]
            pstool_filter = r'<file title=".*_pstools.zip" url="(.*?)">'
            url_download_pstool = re.findall(pstool_filter, r.content)[0]
            print("sw package url: %s , pstool url: %s"%(url_download_sw,url_download_pstool))
            return url_download_sw,url_download_pstool
        except requests.exceptions.RequestException as e:
            print("url_status: get package and pstool url Fail")
            print("error:%s",e)

    def download_package_date_branch(self):
        release_url = self.get_url_date_branch()
        try:
            r = requests.get(release_url)
            if r.status_code == 200 or r.status_code == 304:
                pk_name = r.content
            else:
                print('get coop release fail')
        except requests.exceptions.RequestException as e:
            print(e)
        if not pk_name:
            print("there is no sw package of %s in %s ",pk_branch,pk_date)
            sys.exit(1)
        else:
            self.download_package_name()

    def get_url_date_branch(self,pk_date,pk_branch):
        enb_product = 'sbts'
        enb_branch = {'trunk': 'sbts00',
                      '19a': 'sbts19a',
                      '19b': 'sbts19b'
                      }
        sbts_branch = enb_branch[pk_branch]
        date = datetime.datetime.strptime(pk_date, '%Y%m%d')
        coop_url = 'http://coop.china.nsn-net.net:3000/'
        release_url = coop_url + 'api/promotion/get?bl=sran&product={}&branch={}&time={}&promotion_step=qt;4g_tdd'.format(
            enb_product, sbts_branch, date)
        print(release_url)
        return release_url

    def extract_pstools(self):
        if os.path.isfile(self.pstools_file):
            f = zipfile.ZipFile(self.pstools_file)
            extract_dir = os.path.dirname(self.pstools_file) + "/pstools"
            f.extractall(path=extract_dir)
            f.extractall(path="/opt/TtiTracer/pstools")
        else:
            print("thers is no pstools.zip file, please download pstools")

def parse_cmd():
    parser = argparse.ArgumentParser(description="download sw package based on QC promotion or package name and pstools")
    #parser.add_argument('-pstools', dest='pstools', help='please input pstools version',default='')
    group=parser.add_mutually_exclusive_group()
    group.add_argument('-pn', dest='pk_name', help='please input package name',default='')
    group.add_argument('-pd', dest='pk_date_branch', nargs=2,
                        help='please input package date and branch,for example:trunk 20190101')
    args = parser.parse_args()
    pk_branch = ""
    pk_date = ""
    if args.pk_date_branch:
        branch_list = ["TRUNK","19A","19B"]
        if args.pk_date_branch[0].upper() in branch_list:
            pk_branch = args.pk_date_branch[0]
            pk_date = args.pk_date_branch[1]
        else:
            pk_date = args.pk_date_branch[0]
            pk_branch = args.pk_date_branch[1]
        if not pk_date.isdigit():
            print("% format is not correct,has other char, please input correct format,",pk_date)
            sys.exit(1)
    print(args.pk_name, pk_branch, pk_date)
    return args.pk_name, pk_branch, pk_date

if __name__ == "__main__":
    pk_name, pk_branch, pk_date = parse_cmd()
    bts_package = SWPackage(pk_name,pk_branch,pk_date)
    if pk_name:
        bts_package.download_package_name()
    else:
        bts_package.download_package_date_branch()
    bts_package.extract_pstools()
    #
    # #target_bd = get_release_version(release_url)
    # print pk_name
    # print 'start download package in download_package.py'
    # download_package(target_pn)
    # unzip_pstools(target_pn)
