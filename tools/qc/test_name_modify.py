#! /user/bin/enn python
#-*- coding: utf-8 -*-

import numpy
import pandas as pd
import os,re
from robot.api import TestData

class test_name_modify(object):
    def __init__(self,case_path,qc_path):
        self.case_path = case_path
        self.qc_path = qc_path
        self.case_qc_para={}
        self.qcid_flag = False
        self.casename_flag = False

    def deep_search_local_path(self,file_path):
        content_list = os.listdir(file_path)
        for item in content_list:
            current_file_path = os.path.join(file_path,item)
            if os.path.isfile(current_file_path):
                if item.endswith((".xlsx",".xls")):
                    self.analysis_xlsx_file(current_file_path)
                if item.endswith((".robot")):
                    self.analysis_test_file(current_file_path)
            else:
                self.deep_search_local_path(current_file_path)

    def analysis_xlsx_file(self,file_path):
        df = pd.read_excel(file_path)
        row_len=len(df.index)
        for i in range(row_len):
            qc_instance_id = df["Test Instance ID"][i]
            qc_case_name = df["Test: Test Name"][i]
            qc_case_name = qc_case_name.split("]")[-1].strip()
            self.case_qc_para[qc_instance_id]=qc_case_name
            #list_item = "{}+{}\n".format(qc_instance_id,qc_case_name)
            #self.case_qc_para.append(list_item)
            #self.case_qc_para[int(qc_instance_id)] = str(qc_case_name)

    def write_to_txt(self):
        qc_file = os.path.join(self.qc_path,"qc_para.txt")
        with open(qc_file,"wb") as f:
            for key, value in self.case_qc_para.items():
                line = "{}+{}\n".format(key,value)
                f.write(line)
            f.close()

    def analysis_test_file(self,file_path):
        try:
            suite= TestData(source=file_path)
            for item in suite.testcase_table.tests:
                if self.casename_flag:
                    qc_instance_id = self.__get_qc_instance_id(item)
                    if self.case_qc_para.has_key(qc_instance_id):
                        self.__test_name_refine(file_path,qc_instance_id,self.case_qc_para[qc_instance_id])
                if self.qcid_flag:
                    case_name = item.name
                    for key, value in self.case_qc_para.items():
                        if value.find(case_name) != -1:
                            qc_id = key
                            self.__qc_id_refine(file_path,qc_id,case_name)
        except Exception,e:
            print('ERROR: Anaylsis file {} Failed'.format(file_path))
            print('ERROR: reason  is {}'.format(e))

    def __test_name_refine(self,case_path,qc_instance_id,case_name):
        f_handler = open(case_path, "rb")
        data = f_handler.readlines()
        f_handler.close()
        for data_item in data:
            #match_result = re.search("(^\*.*Test.*Cases.*\*$)",data_item)
            match_result = re.search("(\[Tags\].*QC\_{}.*)".format(qc_instance_id), data_item)
            if match_result:
                case_name_index = data.index(data_item) - 1
                data[case_name_index]="{}\n".format(case_name)
                break
        with open(case_path,"wb") as f:
            f.writelines(data)

    def __qc_id_refine(self,case_path,qc_instance_id,case_name):
        f_handler = open(case_path, "rb")
        data = f_handler.readlines()
        f_handler.close()
        for data_item in data:
            if case_name in data_item:
                tag_index = data.index(data_item) + 1
                old_qcid = re.search("QC_(\d+)", data[tag_index]).group(1)
                data[tag_index]=data[tag_index].replace("QC_{}".format(old_qcid),"QC_{}".format(qc_instance_id))
                break
        with open(case_path,"wb") as f:
                f.writelines(data)

    def __get_qc_instance_id(self,test_object):
        qc_instance_id=0
        if test_object.tags:
            for item_tag in test_object.tags.value:
                match_result = re.search("QC_(\d+)",item_tag)
                if match_result:
                    qc_instance_id = match_result.group(1)
                    qc_instance_id = int(match_result.group(1))
        return qc_instance_id

    def run_testname(self):
        self.deep_search_local_path(self.qc_path)
        self.write_to_txt()
        self.deep_search_local_path(self.case_path)

    def modify_qcid_casename(self,qcid_flag=False,casename_flag=False):
        self.qcid_flag = qcid_flag
        self.casename_flag = casename_flag

if __name__ == "__main__":
    qc_path = r"C:\linux\linux group\project\package\qc\20A"
    case_path = r"C:\project\ET\robotlte\branch\SRAN20A\ATF_HardRT"
    #case_path = r"C:\project\ET\robotlte\trunk\ATF_HardRT"
    test_case = test_name_modify(case_path,qc_path)
    test_case.modify_qcid_casename(True,False)
    test_case.run_testname()


    #test_case.deep_search_local_path(dir_path)
    #test_case.write_to_txt()