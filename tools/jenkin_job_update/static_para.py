# -*- coding: utf-8 -*-

import requests
import getopt
import datetime
import sys


proxies = {'http': '10.144.1.10:8080',
           'https': '10.144.1.10:8080'}

def get_release(enb_type, t):
    # 访问coop api，获取某天最新的release版本
    enb_product = {'tl00': 'sbts',
                   'tl19a': 'sbts',
                   'tl19b': 'sbts',
                   }
    enb_branch = {'tl00': 'sbts00',
                  'tl19a': 'sbts19a',
                  'tl19b': 'sbts19b'
                  }
    p = enb_product[enb_type.split('_')[1]]
    enb_type_0 = enb_type.split('_', 1)[0]
    enb_type_1 = enb_type.split('_', 1)[1]
    b = enb_branch.get(enb_type_1, enb_type_1)
    try:
        date = datetime.datetime.strptime(t, '%Y-%m-%d')
    except ValueError:
        date = datetime.datetime.strptime(t, '%Y/%m/%d')
    coop_url = 'http://coop.china.nsn-net.net:3000/'
    release = ''
    max_try = 15
    while not release and max_try:
        if enb_type_0 == 'cit' and max_try < 15:
            return release
            break
        t = date.strftime('%Y%m%d')
        release_url = coop_url + 'api/promotion/get?bl=sran&product={}&branch={}&time={}&promotion_step=qt;4g_tdd'.format(p, b, t)
        try:
            r = requests.get(release_url, timeout=(7, None))
            if r.status_code == 200:
                release = r.content
            else:
                print 'get coop release fail'
        except requests.exceptions.RequestException as e:
            print e
        date = date - datetime.timedelta(days=1)
        max_try = max_try - 1
        if release:
            return release
            break


def get_paras(argv):
    target_bd = ''
    cell_num = '3'
    reset_time = '4'
    host = '192.168.255.1'
    proxy = False
    try:
        opts, args = getopt.getopt(argv, "hpn:pd:pt:cn:rt:host:proxy",
                                   ["pn=", "pd=", "pt=", "cn=", "rt=", "host=", "proxy="])
        print opts, args
    except getopt.GetoptError:
        print 'check_package_by_uteadmin.py -pn <package name> -pt <package date> -cn <cell number> -rt <reset times> -host <host> -proxy <proxy>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'check_package_by_uteadmin.py -pn <package name> -pt <package date> -cn <cell number> -rt <reset times> -host <host> -proxy <proxy>'
            sys.exit()
        elif opt in ("-pn", "--pn"):
            target_bd = arg
        elif opt in ("-pd", "--pd"):
            target_bd_date = arg
        elif opt in ("-pt", "--pt"):
            target_bd_type = arg
        elif opt in ("-cn", "--cn"):
            cell_num = arg
        elif opt in ("-rt", "--rt"):
            reset_time = arg
        elif opt in ("-host", "--host"):
            host = arg
        elif opt in ("-proxy", "--proxy"):
            proxy = arg
    if not target_bd:
        target_bd = get_release(target_bd_type, target_bd_date)
    return target_bd, cell_num, reset_time, host, proxy


target_bd, cell_num, reset_time, host, proxy_flag = get_paras(sys.argv[1:])
