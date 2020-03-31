# -*- coding: utf-8 -*-

import os, datetime,time
import sys
import subprocess
import logging
import getopt

class remote_download(object):
    SSHD = "cmd /C net start"
    def __init__(self):
        print("gxy")
    def __save_current_environ_path(self):
        self.environ  = os.getenv("PATH")
    def check_sshd_server(self):
        logging.info("start checking if sshd is installed")
        services = self.__run_remote_cmd(self.SSHD)
        if "sshd" in services:
            logging.info("Cygwin sshd service found!")
        else:
            logging.error("Cygwin service not found in started services! Make sure that cygwin is installed and started.")

    def __run_remote_cmd(self, command):
        child = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        return iter(child.stdout.readline())
    def add_environment_variable(self,variable):
        #add new environment varialbe
        self.__save_current_environ_path()
        logging.info("get current environment：%s", self.environ)
        new_path = self.environ + variable + ";"
        print("%s", new_path)
        cmd = 'setx PATH "{}" /M'.format(new_path)
        os.system(cmd)
class crtlog_download(object):
    def __init__(self):
        pass
def get_arg_parse():
    try:
        opts,args = getopt.getopt(argv,"time",["time="])
    except:
        print("download_crt_log_html.py -time <current date>")
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            print("download_crt_log_html.py -time <current date>")
        if opt in ("-time","--time"):
            file_time = arg
        else:
            time.strftime("%Y%m%d",datetime.datetime.currenttime())
            file_time

if __name__ == "__main__":
    pass