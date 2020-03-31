#! /user/bin/enn python
#-*- coding: utf-8 -*-

from robot.api import TestData
import os,re,time
import subprocess
import argparse,optparse

class CreateCaseFromLocal(object):
    def __init__(self, local_path):
        self.cases_info_list = []
        self.local_root_path = local_path
        self.deep_search_local_path(local_path)

    def deep_search_local_path(self, local_path):
        try:
            content_list = os.listdir(local_path)
            content_list.sort()
            for item in content_list:
                file_path = os.path.join(local_path, item)
                if os.path.isdir(file_path):
                    self.deep_search_local_path(file_path)
                else:
                    if item.endswith((".robot")):
                        self._analysis_case_file(file_path)
        except Exception, e:
            print("ERROR: deep_search failed:%s" % e)

    def _analysis_case_file(self, file_path):
        try:
            #svn_path = str(file_path).split(self.local_root_path)[-1]
            suite = TestData(source="%s" % (file_path))
            for item in suite.testcase_table.tests:
                case_info = {}
                case_info['suite_path'] = file_path
                case_info['name'] = item.name
                case_info['qc_instance_id'] = self._get_qc_instance_id(item)
                self.cases_info_list.append(case_info)
        except Exception, e:
            print('ERROR: Anaylsis file [%s] Failed' % file_path)
            print('ERROR: reason  is %s' % e)

    def _get_qc_instance_id(self, case_object):
        qc_instance_id = 0
        for case_tag in case_object.tags.value:
            new_format_ret = re.search('QC_(\d+)', case_tag)
            if new_format_ret:
                qc_instance_id = int(new_format_ret.group(1))
        return qc_instance_id


class UteCloudCase (object):
    def __init__(self,qc_config_path="C:\project\ET\robotlte\trunk\ATF_HardRT\cloud_case\common.qc",
                 local_path="/home/ute/robotlte/testsuite/hangzhou/trunk/ATF_HardRT/",
                 case_log_path="/home/ute/test_results"):
        self.case_list=CreateCaseFromLocal(local_path).cases_info_list
        #print("**************\n{}".format(self.case_list))
        self.case_log_path = case_log_path
        self.__createtestresult__()
        self.prepare_enviroment()
        self.robot_opt=''
        self.qc_config_path=qc_config_path

    def prepare_enviroment(self):
        cmd_install="pip install agent_reporting_portal"
        self.__runcmd__(cmd_install)
        self.get_cloud_variable_env()
    def get_cloud_variable_env(self):
        env_variable="/home/ute/testline_init_results/logs/env_variables.txt"
        lines=''
        if os.path.exists(env_variable):
            with open(env_variable,"rb") as f:
                lines=f.readlines()
            for line in lines:
                if "CM_TOPOLOGY_NAME".lower() in line.lower():
                    self.tl_type=line.split("=",1)[-1].strip()
                if "UTE_CONFIGURATION".lower() in line.lower():
                    self.tl_name = line.split(".",1)[-1].strip()
                if "ENB build".lower() in line.lower():
                    sw_re = ".*(SBTS.*_ENB_\d*_\d*_\d*).*"
                    self.SW_version =re.search(sw_re,line).group(1)
            print("++++++++++++++++\n {}-{}-{}".format(self.tl_type,self.tl_name,self.SW_version))
            if self.tl_type is None:
                print("cann't find tl type")
            if self.tl_name is None:
                print("cann't find tl name")
            if self.SW_version is None:
                print("cann't find SW version")

    def parse_parameter(self,argv_string):
        parser = argparse.ArgumentParser(
            description="please input pybot option command")
        parser.add_argument('--robot_opt', dest='robot_opt', help='robot option command',default='')
        args = parser.parse_args(argv_string)
        self.robot_opt = " ".join(args.robot_opt.split())

    def __createtestresult__(self):
        if not os.path.exists(self.case_log_path):
            os.mkdir(self.case_log_path)
        time_string=time.strftime("%Y%m%d%H%M%S")
        self.cloud_case_path = os.path.join(self.case_log_path,"Test_log_{}".format(time_string))
        if not os.path.exists(self.cloud_case_path):
            os.mkdir(self.cloud_case_path)

    def  run_case(self):
        for item_case in self.case_list:
            case_name = item_case['name'].split(".",1)[0]
            case_robot = item_case['suite_path']
            output_file = os.path.join(self.cloud_case_path,"{}_output.xml".format(case_name))
            log_file =  os.path.join(self.cloud_case_path,"{}_log.html".format(case_name))
            option_cmd = "-L Trace -o {} -l {} {}".format(output_file,log_file,self.robot_opt)
            pybot_cmd = "pybot {} {}".format(option_cmd,case_robot)
            output, err= self.__runcmd__(pybot_cmd)
            if len(err) > 0:
                if "error".lower() in err.lower():
                    print("cmd: {} executing faile,err:{}".format(pybot_cmd, err))
            if os.path.isfile(output_file):
                qc_config_file = self.__create_qc_file(case_name)
                reporting_cmd = "ute_reporting_portal send -ie -qc {} -ro {} -tl {} -v --file_path \"{}\" --sw_version \"{}\" -l \"{}\"".format(
                qc_config_file, output_file, self.tl_name, case_robot, self.SW_version, self.tl_type)
                #reporting_cmd = "ute_reporting_portal send -ie -ro {} -tl {} -v --file_path \"{}\" --sw_version \"{}\" -l \"{}\"".format(output_file,self.tl_name,case_robot,self.SW_version,self.tl_type)
                output_report,err_report=self.__runcmd__(reporting_cmd)
                if len(err_report) > 0:
                    if "Report was successfully sent to Reporting Portal" in err_report:
                        print("please ignore this error during reporting portal, finally reporting portal is successfully")
                elif "error".lower() in err_report:
                    print("cmd: {} executing faile,err:{}".format(reporting_cmd, err_report))

    def __create_qc_file(self,case_name):
        re_result = re.search("(LTE\d+).*",case_name)
        qc_test_set_name=""
        if re_result:
            qc_test_set_name = re_result.group(1)
        new_qc_file=os.path.join(self.case_log_path,"{}.qc".format(qc_test_set_name))
        if not os.path.exists(new_qc_file):
            with open(self.qc_config_path,"rb") as f:
                data = f.read()
                new_data = data.replace("CRT_R3",qc_test_set_name)
                with open(os.path.join(self.case_log_path,"{}.qc".format(qc_test_set_name)),"wb") as f_w:
                    f_w.write(new_data)
        return new_qc_file

    def __runcmd__(self,cmd):
        p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        start_time = time.time()
        p.wait()
        error = p.stderr.read()
        output = p.stdout.read()
        end_time = time.time()
        print("running cmd:{}, time is {} secs".format(cmd,end_time-start_time))
        return output, error

def robot_cloud_case(qc_config_path,local_path,case_log_path,args):
    args=args.split(" ",1)
    utecase = UteCloudCase(qc_config_path,local_path,case_log_path)
    utecase.parse_parameter(args)
    utecase.run_case()


if __name__=="__main__":
    #local_path = "/home/ute/robotlte/testsuite/hangzhou/trunk/ATF_HardRT/LTE2666"
    local_path= r"C:\linux\linux group\project\package\LTE4557"
    qc_config_path = r"C:\project\ET\robotlte\trunk\ATF_HardRT\cloud_case\common.qc"
    robot_cloud_case(qc_config_path,local_path,local_path,"--robot_opt -i CRT -e LF --dryrun")
