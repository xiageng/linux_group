# -*- coding: utf-8 -*-
"""
:copyright: Nokia Networks
:author: Chen Jin Emily
:contact: jin_emily.chen@nokia.com
:maintainer: None
:contact: None
"""


import os
import time
import shutil
from optparse import OptionParser
import subprocess
"""
1. case backup
2. failed_case folder
3. xml name as xxx_0_output.xml
4. case logs folder to timestampe
1. tag pass of fail in log name
2. robot_opt for robot avaiable option
for CRT case:
    case run pass no need to run again
for stability case:
    case repeat run without care about case pass or fail
    some special case need to stop once case failed

base on the requirements:
for CRT case:
    pickup.py -r xxx -p xxx -d xxx --robot_opt xxx
for stability case:
    if case need to stop once case failed,
        please add 's' at the end of run_times in suitemapping, such as '100s'
    pickup.py -r xxx -p xxx -d xxx --robot_opt xxx --case_type stab
"""

SET_TABLE = {
    'test_suite': 'Test Suite',
    'run': 'Run',
    'case_name': 'Case Name',
    'timeout': 'Timeout(min)',
    'tag': 'Case Tag',
    'pc_ip': 'PC IP'}


class TestSuite:
    '''
    '''

    def __init__(self, outputpath):
        '''
        '''
        from robot import version
        ROBOT_VERSION = version.get_version()
        if ROBOT_VERSION < '2.7':
            raise Exception("Please make sure your robot version > 2.7")
        from robot.api import ExecutionResult
        self._er = ExecutionResult(outputpath)
        self.status = self._er.suite.status
        self.passed_list = []
        for case in self._er.suite.tests:
            if case.status == 'PASS':
                self.passed_list.append(str(case))


def get_suite_status(outputfile):
    '''
    '''
    try:
        obj = TestSuite(outputfile)
    except Exception, err:
        print err
        return 1, []
        
    if obj.status == 'FAIL':
        return 1, obj.passed_list
    else:
        return 0, obj.passed_list


def _handle_abnormal_xml(ouput_path, fix_flag, timeout):

    timeout = 60 if not timeout else int(timeout)
    file_size = os.path.getsize(ouput_path)
    if file_size > 0 and fix_flag:
        print "start fix xml--------\n%s" % ouput_path
        from fix_xml import fix_xml
        # fix_xml(ouput_path, ouput_path, timeout)
        print "do nothing\nstop fix xml--------"
    if file_size == 0:
        print 'File size is zero, \nwill delete %s!' % ouput_path
        os.remove(ouput_path)


class CaseRun(object):
    '''
    '''

    def __init__(self):
        '''
        '''
        # args parameters
        self.root_path = None  # -r option
        self.suite_mapping_path = None  # -p suitmapping option
        self.log_path = None  # -d option
        self.robot_opt = None  # robot option
        self.case_type = None

        # kinds of folder
        self.case_backup_dir = None
        self.index_info = None
        self.useful_lines = None
        self.passed_case_list = []
        self.failed_suitemapping = ''
        self.BTS_IP = None
        self.count = 0

    def count_num(self):
        self.count += 1
        if self.count < 10:
            dis_count = "000%s" % self.count
        elif 10 <= self.count < 100:
            dis_count = "00%s" % self.count
        elif 100 <= self.count < 1000:
            dis_count = "0%s" % self.count
        elif 1000 <= self.count < 10000:
            dis_count = "%s" % self.count
        return dis_count

    def parse_parameters(self):
        '''
        '''
        parser = OptionParser()
        parser.add_option(
            "-r",
            "--rootpath",
            action="store",
            type="string",
            dest="rootpath")
        parser.add_option(
            "-p",
            "--pickup",
            action="store",
            type="string",
            dest="pickup")
        parser.add_option(
            "-d",
            "--dir",
            action="store",
            type="string",
            dest="dir")
        parser.add_option(
            "--robot_opt",
            action="store",
            type="string",
            dest="robot_opt")

        parser.add_option(
            "--case_type",
            action="store",
            type="string",
            dest="case_type")
        (options, _args) = parser.parse_args()

        if not options.rootpath:
            raise Exception("Please input the root path for these cases")

        if not options.pickup:
            raise Exception(
                "Please input pick up file name which ending with .py")

        if not options.dir:
            raise Exception(
                "Please input LOG DIR for log.html, report.html and output.xml")

        self.root_path = options.rootpath
        self.suite_mapping_path = options.pickup
        self.log_path = options.dir
        self.output_for_RS = options.dir

        self.robot_opt = options.robot_opt if options.robot_opt else ''
        self.case_type = options.case_type if options.case_type else ''

        option = self.robot_opt.split()
        for env_py in option:
            if env_py.endswith('.py'):
                self._parse_bts_ip(env_py)
                break

        if self.robot_opt:
            items = self.robot_opt.split()
            for i in range(len(items)):
                if items[i] == '-V' and not items[i + 1].startswith('"'):
                    items[i + 1] = '"%s"' % items[i + 1]
            self.robot_opt = ' '.join(items)

    def _parse_bts_ip(self, env_py):
        with open(env_py, 'r') as f_obj:
            content = f_obj.read()
            import re
            tmp = re.search('BTS_PC_INFO.*IP.*"(\d+.\d+.\d+.\d+)"', content)
            if tmp:
                self.BTS_IP = tmp.group(1)

    def create_folders(self):
        '''
        # create a new folder to store cases needed to be tested
        '''
        time_string = time.strftime("%Y%m%d%H%M%S")

        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        case_log_dir = os.path.join(
            self.log_path, 'Test_Log_%s' %
            time_string)
        self.log_path = case_log_dir
        if not os.path.exists(case_log_dir):
            os.mkdir(case_log_dir)
        self.case_backup_dir = os.path.join(
            case_log_dir, "Cases_Picked_Backup")
        if not os.path.exists(self.case_backup_dir):
            os.mkdir(self.case_backup_dir)
            os.mkdir(os.path.join(self.case_backup_dir, 'pass_log'))
            os.mkdir(os.path.join(self.case_backup_dir, 'fail_log'))
        self.failed_suitemapping = os.path.join(
            self.case_backup_dir, 'failedcase.csv')

    def parse_suite_mapping(self):
        """It will analyse suite_mapping_path, then write case information into a list which
        contains case path, case name, case tag """
        with open(self.suite_mapping_path, 'r') as f_obj:
            content = f_obj.read()
        print SET_TABLE['test_suite'], SET_TABLE['run'], 33000000
        
        if SET_TABLE['test_suite'] not in content or \
                SET_TABLE['run'] not in content:
            raise Exception(
                "some tag info miss in %s" %
                (self.suite_mapping_path))
        lines = content.splitlines()
        lines = [line.strip().split(',') for line in lines]

        line_num = len(lines)
        ip_flag = False
        # get position of tags
        for index in range(line_num):
            items = lines[index]
            if SET_TABLE['test_suite'] in items and SET_TABLE['run'] in items:
                index_items_length = len(items)
                run_pos = items.index(SET_TABLE['run'])
                start = index + 1
                self.index_info = items
                if SET_TABLE['pc_ip'] in items:
                    ip_pos = items.index(SET_TABLE['pc_ip'])
                    ip_flag = True
                break

        # get useful lines
        useful_lines = []
        for index in range(start, line_num):
            items = lines[index]
            if index_items_length == len(items) and items[
                    run_pos].strip() and items[run_pos] != "0":
                if ip_flag and items[ip_pos] and self.BTS_IP in items[ip_pos]:
                    useful_lines.append(items)
                elif ip_flag is False:
                    useful_lines.append(items)

        self.useful_lines = useful_lines
        return self._get_case_list()

    def _get_case_list(self):
        case_list = []
        index_info = self.index_info
        suite_pos = index_info.index(SET_TABLE['test_suite'])
        case_pos = index_info.index(SET_TABLE['case_name'])
        self.case_pos = case_pos
        run_pos = index_info.index(SET_TABLE['run'])
        timeout_pos = index_info.index(SET_TABLE['timeout'])
        tag_pos = index_info.index(SET_TABLE['tag'])

        for items in self.useful_lines:
            suite_path = items[suite_pos]
            suite_path = suite_path.replace(
                "/", "\\") if os.name == 'nt' else suite_path
            file_path = os.path.join(self.root_path, suite_path.strip('/'))

            detail_dict = {}
            detail_dict['run_times'] = items[run_pos]
            detail_dict['timeout'] = items[timeout_pos]
            detail_dict[
                'tag_info'] = '-t "%s" %s' % (items[case_pos], items[tag_pos])
            case_dir_dict = {}
            case_dir_dict[file_path] = detail_dict
            exist_flag = False

            for u in range(len(case_list)):
                if file_path in case_list[u] and (
                        items[case_pos] not in case_list[u][file_path]['tag_info']):
                    case_dir_dict[file_path]['tag_info'] = case_list[u][
                        file_path]['tag_info'] + ' -t "%s"' % items[case_pos]
                    case_list[u] = case_dir_dict
                    exist_flag = True
            if not exist_flag:
                case_list.append(case_dir_dict)

        if not case_list:
            raise Exception(
                "No case run, or suitemapping wrong please get the right one from report server")

        return case_list

    def run_all_suites(self, case_list):
        """It will make a new directory if not exist, then copy cases to pickup folder
        and run Robot command and generate output.xml file"""

        for case_dict in case_list:
            for case_dir in case_dict.keys():
                if not os.path.exists(case_dir):
                    print "\n####################Case Not Exist#######################"
                    print "Case: \"%s\" do not exist" % (case_dir)
                    print "\n\n"
                    continue
                print "\n####################Case INFO#######################"
                print "Run case INFO: ", case_dir, case_dict[case_dir]
                if 'stability' == self.case_type:
                    self._handle_stability_tags(case_dir, case_dict)
                else:
                    self._handle_tags(case_dir, case_dict)

    def _handle_tags(self, case_dir, case_dict):
        # copy case to new folder
        timeout = case_dict[case_dir]['timeout']
        run_times = case_dict[case_dir]['run_times']

        tag_info = case_dict[case_dir]['tag_info']

        case_fail_flag = 1
        for i in range(int(run_times)):
            if (0 != case_fail_flag):
                case_name = os.path.basename(case_dir)
                pre, ext = case_name.rsplit('.', 1)
                case = "%s_%s_No%s_output.%s" % (self.count_num(),
                                                 pre, str(i), ext)
                print """========================Run case:============================"""
                ouput_path = self._run_one_suite(
                    case, tag_info, case_dir, timeout)
                case_fail_flag, new_tag = self._check_suite_result(
                    ouput_path, tag_info)
                tag_info = new_tag

    def _handle_stability_tags(self, case_dir, case_dict):
        # copy case to new folder
        timeout = case_dict[case_dir]['timeout']
        run_times = case_dict[case_dir]['run_times']
        tag_info = case_dict[case_dir]['tag_info']

        case_fail_flag = 0
        case_fail_stop = True if run_times.endswith('s') else False
        for i in range(int(run_times.strip('s'))):
            print i
            if case_fail_stop and case_fail_flag:
                break
            case_name = os.path.basename(case_dir)
            pre, ext = case_name.rsplit('.', 1)
            case = "%s_%s_No%s_output.%s" % (self.count_num(),
                                             pre, str(i), ext)
            # run case one by one
            print """========================Run case:============================"""
            ouput_path = self._run_one_suite(
                case, tag_info, case_dir, timeout)
            case_fail_flag, _new_tag = self._check_suite_result(
                ouput_path, tag_info)

    def _run_one_suite(self, case_name, tag_info,
                       robot_case_path, timeout):
        """ run case one by obe by pybot command """
        suite_status = 1

        output_name = "%s.xml" % case_name.replace(" ", "_").rsplit('.', 1)[0]
        ouput_path = os.path.join(self.case_backup_dir, output_name)
        cmd_option = " "
        cmd_option += "-o \"%s\" -d \"%s\" " \
            % (ouput_path, self.log_path)

        cmd_option += "%s" % tag_info if tag_info else ''

        cmd_option += " %s" % self.robot_opt if self.robot_opt else ''

        pybot_cmd = "pybot %s \"%s\"" % (cmd_option, robot_case_path)

        start_time = time.time()
        print pybot_cmd
        p = subprocess.Popen(pybot_cmd, shell=True)
        fix_flag = False

        if not timeout:
            p.wait()
        else:
            while p.poll() is None and (time.time() - start_time) < float(timeout) * 60:
                time.sleep(3)
            if p.poll() is None:
                print """
     ======================Timeout=========================
        Timeout!!! teminate this case:
        Case: %s
        output: %s
    =====================================================""" % (case_name, ouput_path)
                os.system("TASKKILL /F /T /PID %s" % (p.pid))
                p.__del__()
                time.sleep(2)
                fix_flag = True

        if not os.path.exists(ouput_path):
            return ouput_path
        _handle_abnormal_xml(ouput_path, fix_flag, timeout)
        time.sleep(2)
        try:
            file_tail =  time.strftime("%m%d%H%M%S") + "_output.xml"
            output_file_for_RS = os.path.join(self.output_for_RS, file_tail)
            rebot_cmd = 'rebot -L TRACE -N TA  -o "%s"  "%s"' %(output_file_for_RS,ouput_path)
            os.system(rebot_cmd)
        except:
            # if use rebot failed, hard copy this file.
            try:
                shutil.copy(ouput_path, output_file_for_RS)
            except:
                pass            
        return ouput_path

    def _check_suite_result(self, ouput_path, tag_info):
        if not os.path.exists(ouput_path):
            return 1, tag_info
        suite_status, passed_list = get_suite_status(
            ouput_path.replace('\\', '\\\\'))

        self.passed_case_list += passed_list

        time.sleep(1)
        for f in passed_list:
            remove_tag = '-t "%s"' % f
            tag_info = tag_info.replace(remove_tag, "")

        # time_stamp = time.strftime("%m%d%H%M%S")
        status = 'fail' if suite_status else 'pass'
        path = os.path.dirname(ouput_path)
        name = os.path.basename(ouput_path)
        name = name.replace('.xml', '_%s.html' % status)
        if suite_status:
            new_log_file = os.path.join(path, 'fail_log', name)
        else:
            new_log_file = os.path.join(path, 'pass_log', name)
        rebot_cmd = "rebot -l \"%s\"  \"%s\"" % (new_log_file, ouput_path)
        print rebot_cmd
        os.system(rebot_cmd)
        return suite_status, tag_info

    def combine_output_file(self, output_name='output.xml'):
        """It will combine all result file with".xml" into log file and report file"""
        import glob
        dir_ = self.case_backup_dir
        xml_list = glob.glob(os.path.join(dir_, '*.xml'))
        if len(xml_list) == 0:
            return

        # generate log in -d option log path
        rebot_cmd = 'rebot -L TRACE -N TA -l "%s/%s_log.html" -r "%s/report.html" "%s/*.xml"' % (
            self.log_path, time.strftime("%m%d%H%M%S"), self.log_path,dir_)
        os.system(rebot_cmd)

        time.sleep(1)
        # generate log in case backup dir
        if not os.path.exists(os.path.join(dir_, output_name)):
            rebot_pick_cmd = "rebot -L TRACE -N TA -l \"%s/log.html\" -r \"%s/report.html\"  %s/*.xml" % (
                dir_, dir_, dir_)
            os.system(rebot_pick_cmd)

    def generate_new_suitemapping(self):
        import copy
        tmp = copy.copy(self.useful_lines)
        for line in self.useful_lines:
            for passed in list(set(self.passed_case_list)):
                if passed.lower().replace(
                        '_', ' ') == line[
                        self.case_pos].lower().replace(
                        '_', ' ') and line in tmp:
                    tmp.remove(line)

        if tmp:
            content = []
            content.append(','.join(self.index_info))
            for line in tmp:
                content.append(','.join(line))
            with open(self.failed_suitemapping, 'w') as f_obj:
                f_obj.writelines('\n'.join(content))


def run_pickup():
    try:
        obj = CaseRun()
        obj.parse_parameters()
        case_list = obj.parse_suite_mapping()
        print case_list
        obj.create_folders()

        obj.run_all_suites(case_list)
        obj.combine_output_file()

    except Exception as err:
        print err

    finally:
        obj.generate_new_suitemapping()


if __name__ == "__main__":
    run_pickup()
