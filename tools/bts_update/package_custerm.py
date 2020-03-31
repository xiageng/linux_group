#! /user/bin/enn python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

import re,sys
import datetime
import getopt
#from selenium import webdriver

proxies = {'http': '10.144.1.10:8080',
           'https': '10.144.1.10:8080'}


date_column_num=5
Promo_co_num=8
def get_release(enb_type, t):
    SBTS19B_curl="https://wft.int.net.nokia.com/ALL/branches/5739"
    release=''
#    headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
#             'Cookie': "SMSESSION=UmV300mNkm6AHuhkEDFShpeLecJte1BSge4G/x7O4+XzC0R5p+Kv7sW8tUg+z2tnv11SWPp9nBCQjfHjYXp2qWXDSmiHPL5P5YsBQIVTThPyxRXWIl+o83m14fYaVyayvx8BUQcuIF6uf5jKmMwFh4AQ23IwLgNQJkQBRWV2PBZ3Z3tQDNHX9YrpaODxMhGyMs1S3m+jQByQwcxXu3CgbiJlunGuiVllo4rogQxFOuOZYHssyJdtdRfiEdKcWgp9MixX/Pgubs6GqjDinOZDt78em42Bk5kCNYPh2KFGAKdCW8vP8MO1D6MZXZDuI0p7Qp7MPCyxI/G1dJ2CPwwr/KP6ZVgQvRcaFs7wRrYV5WigeOfClZZa20o/SM8TWAaJ8QVUUzeyIziLB321f86urJsrn5dEFneiNCLI5Jzo4L+WKfZHOXev4cZ9OaZImuH48+4WuAUwVuf4/DR6dA/MtD6GvDOYSVRTXPGzRfV2hJwrfI5GuSijMxaKrl2NzBqwXZH5uoG4rdPB/Ml3a86Lk3lPEjKLdQ/7cJAZi9/NTCXQCRvFISIKo4I7jreRPKCh73RIfYbViNexRQdj4Z1VifdX3isBbRdCRCHqaAGLct6r6smgT5HXGFJBcjLh9M+AKQ7WiEU49jCs4+C5jye/0rWItCi9gZtUzM59mu2IdVzlyjKwKqzieL73FASeAB7IeoSG+n5imF82I8KQXsWBXj4ijgzz8GT/MeomLJbs2r6OHi+lT3vxiJAV6SYJNpi6QtWOSjP/K8Y0ZxPTEtCQvvNe/SOrhl1jFSnl3Jjnf6a3lYheyi/VdBNVZHBtlvKvZKvTUv9UR5GmT3EUYWj4SJCPNPqQ3pS5/TMssIEUxe2XGUDbSCZRe6HaGFD02NVP/5hjGkuAwqFENcQ9fFB0Ko70RLHAQFd7Bj9a2YTbFb+T1wAN77cuyxgUg7MPgMWZ6U+lf0gBbNZoKkbLCw01ulqJMgrxCODVjPHliT46S8uLhf0Xucd1TlkDE3duqReJXZkaMOZ96jxho8DNFILQ4C4Oje4KQ/qzphR7p/Wk95XNU0eQDxQuHIKQkllDLNg1okr30QFw5ilPadsmh7ixqIiDW3L4+OYDFZLwWoCryMN0hEkgrU6AJC1fZBloNyacHbdW9eIriJxpwaqjBylSypBI/3xScrmx; _session_id=b6c990c2f8026a9eabd810b2a8b1330f"
#    }

    headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
             'Cookie':"owa_v=cdh%3D%3E4a681abf%7C%7C%7Cvid%3D%3E1573534552580481996%7C%7C%7Cfsts%3D%3E1573534552%7C%7C%7Cdsfs%3D%3E3%7C%7C%7Cnps%3D%3E8; owa_s=cdh%3D%3E4a681abf%7C%7C%7Clast_req%3D%3E1573793078%7C%7C%7Csid%3D%3E1573792409635335517%7C%7C%7Cdsps%3D%3E0%7C%7C%7Creferer%3D%3E%28none%29%7C%7C%7Cmedium%3D%3Edirect%7C%7C%7Csource%3D%3E%28none%29%7C%7C%7Csearch_terms%3D%3E%28none%29; SMSESSION=Bui7lNTTL3gSWI4MTKYDiQv9B/sOqNGTWVJB91DU0O+t2xiQGCtHSDM/gT3/WOVe8ZQtN2RHAZXVr5SB3IVQiD+NHnwah95xrQF29UpjKt7M40CcZN2rynNnJqstEAUlgGtUI8BHUcvuOTIHsRfjm9CwCoUtITYZW0PvQstQCvHIOSMgyRhkHbpKpyRERMmxX8Lmzhyy6Twt59lPwKX6HTd4oZear9zI1qk/D0dR7+LjBytijaL+MXsjzRMfL1ABs9/jkKCi+1UhXSm1Jj6cunYzGvuQXHP7h84H4kR+JX/jdmLl2HgGK/5zbbeoaqY9p6ZOqVkQqVA32A/C1/ewhwVeB/2jtijsF0lW1gMy4XHHdJMZWwXdpf16wfR8gbYpiPajHuQr/vLKOGZh24Yyi9cxT6DAbvjA+oog6tccny8xHmElDQr0zreKf924svwPkPmKsMKUrU2RwowcyLKrIy9cNmsL5i9TbuqPyGqV8hB/fyTeXMw5iP9XxScxbevcJwZcXvuOH93w4S29VCIunpv/rnV8Z9JJIWFNhlw3Se1ScqMtTNbRLdOQEar9PXeYE64vBl0ns9HXAT8pIAWU2I8Od1uZVyDMrHe0kpSnm5IZ73ebsUk1OwvNPgkJmskaqPq1fh8xZfltIVHVa0ZDn9wJNJjhrta+SbqK+9f8rwaBNHjfMHq+C49gLCW0TmGdAEctZ3zrEaRrGNuXe28QjX6oT8jY6q8ir2vMw0cX7UmZCG89HzCBDGHdP2FggxcERYAOL0pYq6L8c+Z2oK4t/mMOMMmrHh69Vis7WhLVhV6QjzGJGBXe4oagTDIegJbyhi+yVx0sI+nmqWTUow1jYH5SAh3HuC+k6UbSRZ+AAI2RiAdbx+ftUil/MfACaIycYWFO+UL5DVxitU/FTeQAJahvpyIRqpadgngaUbNYK/YsexDo+6HJDCmKk6ZYHpLJmWdAQSnRXkRDivJbfnuZAUBg6brHkYzglJDAOu1/yN8oD7KYZY+Jh4p+hC2yeVEWC5Nt/Nv85JagfYrws0Pm72LJx/NHSZtwIFbH/Pj+4LNukSih/205o7/eg5yhPq4Mlnm9A6PEZM5/J6Z4rXD57vBXzJOpFNu37fYyFsAjClHq7ot8++tkm4gN9w8A25fFXC2NIc5ijMJ9tLwLXfLBqGwhEXRhI0Bc",
    }

    #driver = webdriver.Chrome()
    #driver.minimize_window()
    #driver.get(SBTS19B_curl)
    #data=driver.page_source
    requests.getSession()
    data = requests.get(SBTS19B_curl, headers=headers).content
    soup=BeautifulSoup(data,'html.parser', from_encoding='utf-8')
    table_result=soup.find("table",id=re.compile("table_view"))
    check_name_colum("Delivery date",table_result,date_column_num)
    check_name_colum("Promotion status", table_result, Promo_co_num)
    tr_result=table_result("tr")
    for item in tr_result:
        if not item('td'):
            continue
        td_result = item("td")[Promo_co_num]
        #print("\n\n*****************\n\n\n{}".format(str(td_result.string)))       
        if "4G_TDD_CUSTOMER" in str(td_result):
            release_time=item("td")[date_column_num].string
            print("***********\n{}".format(release_time))
            #current_time = datetime.datetime.strptime(t,"%Y-%m-%d")
            if t in release_time:
                release =item("td")[0].string
                print("4G_TDD_CUSTOMER package: {} at {}".format(release,release_time))
                break
            else:
                print("there is no 4G_TDD_CUSTOMER package at {}".format(t))
                break
    return release

def check_name_colum(column_name,table_result,column_num):
    if column_name in table_result("th")[column_num].string:
        print("{} is the {}th column".format(column_num,column_name))
    else:
        print("please chose the correct {} column".format(column_name))

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


if __name__ == "__main__":
    target_bd, cell_num, reset_time, host, proxy_flag = get_paras(sys.argv[1:])
