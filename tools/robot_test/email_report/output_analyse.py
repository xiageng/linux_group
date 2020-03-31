#! /user/bin/enn python
#-*- coding: utf-8 -*-
import os,re,subprocess,time
from robot.utils import ETSource
from robot.result.resultbuilder import ExecutionResult, ExecutionResultBuilder
from robot.result.executionresult import Result
from htmltemplate import *
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class Log_analysis(object):

    def __init__(self,log_path):
        self.log_dir=log_path
        #self.log_dir_create()

    def log_dir_create(self):
        log_cdrt=os.path.join(self.log_dir,"CDRT")
        log_crt = os.path.join(self.log_dir, "CRT")
        log_cit = os.path.join(self.log_dir, "CIT")
        if os.path.exists(log_cdrt):
            os.system("rm -rf {}/*".format(log_cdrt))
        else:
            os.mkdir(log_cdrt)
        self.__dir_crete__(log_crt)
        self.__dir_crete__(log_cit)

    def __dir_crete__(self,path):
        if os.path.exists(path):
            os.system("rm -rf {}/*".format(path))
            os.mkdir(os.path.join(path,"trunk"))
            os.mkdir(os.path.join(path, "branch"))
        else:
            os.mkdir(path)
            os.mkdir(os.path.join(path, "trunk"))
            os.mkdir(os.path.join(path, "branch"))

    def case_type_check(self,log_folder):
        #log_folder = os.path.join(self.log_dir,"log")
        dir_list=os.listdir(log_folder)
        for item in dir_list:
            item_path = os.path.join(log_folder,item)
            if os.path.isdir(item_path) and item.startswith("Test_log"):
                case_type,version =self.__log_folder_type(item_path)
                print("log folder:{},version:{},case_type:{}".format(item,version,case_type))
                dest_path = os.path.join(self.log_dir, "{}".format(case_type))
                dest_path=os.path.join(dest_path,"{}".format(version))
                os.system("mv -f {}/* {}".format(item_path,dest_path))

    def __log_folder_type(self,path):
        item_list=os.listdir(path)
        output_list=[]
        crt_num=0
        cit_num=0
        cdrt_num=0
        version=''
        for item in item_list:
            if item.endswith("output.xml"):
                with open(os.path.join(path,item)) as f:
                    data = f.read()
                    if "CRT" in data:
                        crt_num = crt_num + 1
                    if "CIT" in data:
                        cit_num= cit_num+1
                    if "CDRT" in data:
                        cdrt_num= cdrt_num+1
                    if crt_num or cit_num or cdrt_num:
                        output_list.append(item)
                        enb_build= re.search("(SBTS.*_ENB_\d+_\d+_\d+)",data)
                        if (enb_build):
                            enb_version=enb_build.group(1)
                            if "ENB_9999" in data:
                                version="trunk"
                            elif "ENB_0000" in data:
                                version="branch"
        output_lenth=len(output_list)
        if output_lenth==2 and cit_num==2 and crt_num==0:
            if version=="trunk":
                return "CIT","trunk"
            else:
                return "CRT","branch"
        elif output_lenth==5 and cdrt_num==5:
            return "CDRT",version
        elif output_lenth==crt_num:
            return "CRT",version

    def __runcmd__(self,cmd):
        p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        start_time = time.time()
        p.wait()
        error = p.stderr.read()
        output = p.stdout.read()
        end_time = time.time()
        print("running cmd:{}, time is {} secs".format(cmd,end_time-start_time))
        return output, error
    def __analysiz_output(self,source_xml):
        ets = ETSource(source_xml)
        test_result = Result(source=source_xml)
        test_result = ExecutionResultBuilder(ets).build(test_result)
        return test_result
    def report_analysize(self,path):
        cit_cmd = "rebot -l all_log.html -r all_report.thml -o all_output.xml -d {} \"{}/*output.xml\"".format(path,path)
        output, error = self.__runcmd__(cit_cmd)
        output_path = os.path.join(path, "all_output.xml")
        cit_run=0
        cit_passed_num=0
        cit_failed_num=0
        case_info = {}
        if os.path.exists(output_path):
            result = self.__analysiz_output(output_path)
            cit_failed_num = result.statistics.total.critical.failed
            cit_passed_num = result.statistics.total.critical.passed
            cit_run = result.statistics.total.critical.total
            for item in result.suite.suites._items:
                case_name=item.name
                case_info[case_name]=item.status
        enb_version = self.get_enb_version(output_path)
        return case_info,cit_run,cit_passed_num,cit_failed_num,enb_version
    def get_enb_version(self,file):
        enb_version=''
        if os.path.exists(file):
            with open(file,"rb") as f:
                data=f.read()
                search_result=re.search("(SBTS.*_ENB_\d+_\d+_\d+)", data)
                if search_result:
                    enb_version=search_result.group(1)
        return enb_version

    def run(self):
        self.case_type_check(os.path.join(self.log_dir,"log"))
        print("start analysis case and generate html content")
        cittrunk_data,cittrunk_resultdata=self.html_generate("CIT","trunk",2)
        #citbranch_data = self.html_generate("CIT", "branch",2)
        crttrunk_data,crttrunk_result_data=self.html_generate("CRT","trunk",33)
        crtbranch_data, crtbranch_result_data= self.html_generate("CRT", "branch", 33)
        cdrtbranch_data,cdrtbranch_result_data = self.html_generate("CDRT", "", 5)
        data_start = TEMPLATE_START
        data = CITTABLE_TITLE + cittrunk_data + crttrunk_data + crtbranch_data + cdrtbranch_data + CITTABLE_END
        result_data=TEST_RESULT_TITLE + cittrunk_resultdata  + crttrunk_result_data + crtbranch_result_data + cdrtbranch_result_data + TEST_RESULT_END
        data_end = TEMPLATE_END
        data=data_start+data + result_data +data_end
        #print("start to send email")
        #self.send_email(data)
        html_file=os.path.join(self.log_dir,"test.html")
        with open(html_file,"wb") as f:
            f.write(data)
        os.system("rm -rf {}/*".format(os.path.join(self.log_dir,"log")))
        #os.system("sshpass -p btstest scp {} root@10.159.218.103://var/lib/jenkins/email-templates/cloud_report.template".format(html_file))

    def html_generate(self,casetype,enbtype,case_num):
        casetype_path = os.path.join(self.log_dir, casetype)
        casetype_path = os.path.join(casetype_path, enbtype)
        casetype_len = len(os.listdir(casetype_path))
        data=""
        result_data = ""
        if casetype_len>0:
            case_info, run_num, pass_num, fail_num, enb_version = self.report_analysize(casetype_path)
            data=CITTABLE_TR.format("{}_{}".format(casetype,enbtype),case_num,run_num,case_num-run_num,pass_num,fail_num,enb_version)
            case_names=sorted(case_info.keys())
            for item in case_names:
                result_data =  result_data + TEST_RESULT_TD.format(item,case_info[item],case_info[item],"{}_{}".format(casetype,enbtype))
        return data, result_data

    def send_email(self,mail_msg):
        sender='xiaoyan.geng@nokia-sbell.com'
        receivers = ['xiaoyan.geng@nokia-sbell.com']
        message = MIMEText(mail_msg, 'html', 'utf-8')
        message['From'] = Header("xiaoyan.geng@nokia-sbell.com")
        message['To'] = Header("xiaoyan.geng@nokia-sbell.com")
        subject = 'trunk/branch report'
        message['Subject'] = Header(subject, 'utf-8')
        smtpObj = smtplib.SMTP()
        smtpObj.connect('10.130.128.21', 25)  # 25 �?SMTP 端口�?        smtpObj.login("xiageng", 'Nokiazxcvbnm1234567')
        smtpObj.sendmail(sender, receivers, message.as_string())
    def run_test(self):
        self.case_type_check(os.path.join(self.log_dir,"log"))
        print("start analysis case and generate html content")
if __name__=="__main__":
    #path="C:\\linux\\linux group\\project\\robot_test\\email_report"
    path=os.getcwd()
    log_a=Log_analysis(path)
    log_a.run_test()