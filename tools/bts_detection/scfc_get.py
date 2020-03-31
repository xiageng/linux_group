#! /user/bin/enn python
#-*- coding: utf-8 -*-

import os
#import ute_admin
from sys import argv
from ute_admin import ute_admin
ute_admin = ute_admin()
def get_scfc(btsid, vm_ip,user,pw):
    scfc_path = os.path.join(os.getcwd(), "scfc")
    if not os.path.exists(scfc_path):
        os.mkdir(scfc_path)
    ute_admin.setup_admin(bts_host="192.168.255.1", bts_port=443, use_ssl=True, remote_host=vm_ip,
                          remote_host_username=user,remote_host_password=pw,alias="gxy")
    scfc_file = os.path.join(scfc_path, "{}_scfc.xml".format(btsid))
    ute_admin.collect_scf(scfc_file, alias="gxy")
    ute_admin.teardown_admin(alias="gxy")

if __name__=="__main__":
    btsid=argv[1]
    vm_ip=argv[2]
    user=argv[3]
    pw=argv[4]
    get_scfc(btsid, vm_ip,user,pw)