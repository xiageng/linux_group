# -*- coding: utf-8 -*-

import requests
import re
import time
import static_para
import sys


proxies = static_para.proxies
target_bd = static_para.target_bd


def get_build_state():
    url_wft = 'https://wft.int.net.nokia.com/ext/build_content/{}'.format(target_bd)
    sw_state = ''
    try:
        r = requests.get(url_wft, stream=True, proxies=proxies)
        sw_state = re.findall(r'<state>(.*?)</state>', r.content)[0]
        print sw_state
    except requests.exceptions.RequestException as e:
        print e
    return sw_state


def check():
    state_flag = False
    for i in xrange(2*4):
        sw_state = get_build_state()
        sw_state
        if 'release' in sw_state.lower():
            state_flag = True
            break
        else:
            time.sleep(15*60)
    return state_flag


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


if __name__ == "__main__":
    sys.stdout = Unbuffered(sys.stdout)
    state_flag = check()
    print 'QT_build_state: {}'.format(state_flag)
    if not state_flag:
        print 'package_name: software not released'
        print 'QT_report: This software has not been released!'
