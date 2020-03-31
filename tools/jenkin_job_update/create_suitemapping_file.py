#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
This script have a functions:
1. create suitemapping.csv file.
    Input: local_root_path_for_case, suite_mapping_file_full_path, build_release_start_time, build_release_to_time, release_name
    Output. suitemapping.csv
Using in CMD,example:
    python create_suitemapping_file.py "d:\TestCase\Trunk_CRT\OAM2"  "D:\TestCase" "2017-08-10" "2017-09-10"  "Trunk"
If case under folder Trunk_CRT, please enter the release name "Trunk"
release name list:
| Trunk          |
| TL17           |
| SBTS00_TDD     |
| TL17ASP        |
| FL00           |
| FL17           |
| FL17SP         |
| FL17A          |
| FL17ASP        |
| SBTS00         |
| SBTS17         |
| SBTS17A        |
| SBTS17ASP      |
| SBTS17SP       |
| FL16A          |
| TL16S4         |
| L18            |
| TL17A 

Created By: GuanXiaobing 2017-09-05
"""

import os
import sys
import requests
from robot.api import TestData
import re


GET_PASSED_QC_ID_URL = "http://10.140.16.201/api/get_passed_qc_ids"

class CreateCaseFromLocal:
    def __init__(self,local_path):
        self.cases_info_list = []
        self.local_root_path = local_path
        self.deep_search_local_path(local_path)
        
    def deep_search_local_path(self,local_path):
        try:
            content_list = os.listdir(local_path)
            content_list.sort()
            for item in content_list:
                file_path = os.path.join(local_path,item)
                if os.path.isdir(file_path):
                    self.deep_search_local_path(file_path)
                else:
                    if item.endswith((".html",".tsv",".robot")):
                        self._analysis_case_file(file_path)
        except Exception,e:
            print("ERROR: deep_search failed:%s" %e)        
        
    def _analysis_case_file(self,file_):
        try:
            svn_path = str(file_).split(self.local_root_path)[-1]
            suite = TestData(source = "%s" %(file_))
            for item in suite.testcase_table.tests:
                    case_info = {}
                    case_info['suite__svnpath'] = svn_path
                    case_info['name'] = self._normalize_robot_name(item.name)
                    case_info['qc_instance_id'] = self._get_qc_instance_id(item)
                    case_info["owner__username"] = ""
                    self.cases_info_list.append(case_info)
        except Exception,e:
            print('ERROR: Anaylsis file [%s] Failed' % file_)
            print('ERROR: reason  is %s' % e)
    
    def _normalize_robot_name(self,set_name):
        set_name = re.sub('(\s*_+\s*)|\s+', ' ', set_name)
        return ' '.join(name.capitalize() for name in set_name.split(' '))
    
    def _get_qc_instance_id(self,case_object):
        qc_instance_id = 0
        for case_tag in case_object.tags.value:
            new_format_ret = re.search('QC_(\d+)', case_tag)
            if new_format_ret:
                qc_instance_id  = int(new_format_ret.group(1))
        return qc_instance_id      

def GetPassedCaseIDFromRS(s_start_time,s_end_time,release_name):
    params = {"start_time":s_start_time,"end_time":s_end_time,"release_name":release_name}
    res = requests.get(GET_PASSED_QC_ID_URL, params=params)
    return res.json()


class ActionDector:
    def __init__(self,local_root_path,suiteMapping_file_path,passed_qc_case_id_list=[]):
        create_instance = CreateCaseFromLocal(local_root_path)
        self.case_info_list = create_instance.cases_info_list
        self.create_suitemapping_file(suiteMapping_file_path,passed_qc_case_id_list)
    
    def create_suitemapping_file(self,suite_mapping_full_path="",passed_qc_case_id_list=[]):
        if os.path.isdir(suite_mapping_full_path):
            suite_mapping_full_path = os.path.join(suite_mapping_full_path,"suitemapping.csv")
        elif not suite_mapping_full_path.endswith(".csv"):
            suite_mapping_full_path = os.path.join(os.path.dirname(__file__),"suitemapping.csv")
        try:
            print suite_mapping_full_path
            cwriter = open(suite_mapping_full_path,'w+')
            cwriter.write('Test Suite,Case Name,Run,Timeout(min),instance_id,owner_name,Case Tag \n')
            for item in self.case_info_list:                
                data = str(item["suite__svnpath"]) + "," + str(item["name"]) +"," +"1" +"," +"60" +"," + str(item["qc_instance_id"]) +"," + str(item["owner__username"]) +"," + " \n"
                cwriter.write(data)
            print("Create suite mapping file successfully, path is %s " %suite_mapping_full_path) 
        except Exception,err:
            print("Create suite mapping file failed, the reason is %s" %err)
        finally:
            cwriter.close() 
            
if __name__ == "__main__":
    try:
        local_case_path = sys.argv[1]
        suitemapping_file_path = sys.argv[2]
        
        action = ActionDector(local_case_path,suitemapping_file_path)
         
    except Exception,err:
        print 'please check the using is right or wrong'
        print err
        exit(1)
