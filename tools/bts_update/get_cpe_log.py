#! /user/bin/enn python
#-*- coding: utf-8 -*-

from robot.libraries.Telnet import Telnet
import logging as log
import time,os
username = "root"
password = "Si8a&2vV9"

def get_cpe_log(host='192.168.0.1',port=23,alias='gctcommand',caputertime=10,file_path='cpe.log'):
    telconn = Telnet()
    conn = telconn.open_connection(host,
                                    port=port,
                                    timeout=60,
                                    prompt='#',
                                    prompt_is_regexp=True,
                                    alias=alias)
    log.info(telconn.login(username,
                                password,
                                password_prompt='ssword:'))

    telconn.set_prompt('lted_client_init_ex success')
    telconn.execute_command("lted_cli")
    telconn.set_prompt('DM> ')
    telconn.write("arm1log 2")
    telconn.write_bare("\r\n")
    telconn.read_until('DM> ')
    telconn.write("q 2")
    time.sleep(float(caputertime))
    ret=''
    ret=telconn.read()
    telconn.write("q 0")
    telconn.switch_connection(conn)
    if os.path.splitext(file_path)[1]:
        os.makedirs(os.path.dirname(file_path))
    f=open(file_path,'wb')
    f.write(ret)
    f.close()


if __name__=='__main__':
    get_cpe_log()
