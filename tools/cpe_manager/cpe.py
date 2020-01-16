# -*- coding: utf-8 -*-
import requests
import json
import time


class CPE(object):
    def __init__(self, ip, timeout=4):
        self.ip = ip
        self.username = 'superadmin'
        self.password = 'admin'
        self.session = requests.Session()
        self.timeout = timeout

    def login(self):
        login_url = 'http://{}/action/login'.format(self.ip)
        payload = {
            'username': self.username,
            'password': self.password
        }
        try:
            r = self.session.post(login_url, data=payload, timeout=self.timeout)
        except requests.Timeout as err:
            print err.message

    def is_login(self):
        '''
        用于判断session是否过期，还没想好要不要判断，怎么判断
        '''
        pass

    def get_node_info(self, *args):
        '''
        以节点node的方式查询状态信息
        :param *args:
            lteDlEarfcnGet  lteUlEarfcnGet
            lteMccGet   lteMncGet
            lteCellidGet
            lteBandGet  lteBandwidthGet
            lteDlBandwidthGet   lteUlBandwidthGet
            lteCinr0Get lteCinr1Get
            ltePciGet   lteLockpcilistGet
            lteRsrq0Get lteRsrq1Get
            lteRsrp0Get lteRsrp1Get
            lteRssi0Get lteRssi1Get
            lteDlFrequencyGet   lteUlFrequencyGet
            lteDlmcsGet lteUlmcsGet
            lteTxpowerGet   lteSinrGet
            lteMainStatusGet: 查询连接状态，为connected代表已连接
            systemDataRateDlCurrent systemDataRateUlCurrent: 空口总速率
            systemProductModel
        :return: 查询的node对应的状态信息
        '''
        url = "http://{}/info?{}".format(self.ip, '&'.join(args))
        try:
            r = self.session.get(url, timeout=self.timeout)
            return json.loads(r.content)
        except requests.Timeout as err:
            print err.message

    def set_node_info(self, node_paras):
        '''
        以节点node的方式设置状态信息
        :param node_paras:
        :return: 是否设置成功
        '''
        url = "http://{}/info".format(self.ip)
        try:
            r = self.session.post(url, data=json.dumps(node_paras), timeout=self.timeout)
            return json.loads(r.content)
        except requests.Timeout as err:
            print err.message

    def get_form_info(self, form):
        '''
        以表单的方式查询状态信息
        :param form:
            devicelist
            apnlist
            wanStatus: 获取WAN口状态，IP地址
            sccList: 获取scc列表
            macFilterList: 获取当前mac过滤的列表
        :return: 查询的表单对应的状态信息
        '''
        url = "http://{}/{}".format(self.ip, form)
        try:
            r = self.session.get(url, timeout=self.timeout)
            return json.loads(r.content)
        except requests.Timeout as err:
            print err.message

    def set_form_info(self, form, action, form_paras):
        '''
        以表单的方式设置状态信息
        :param form:
        :param action: add, delete, set
        :param form_paras:
        :return:
        '''
        url = "http://{}/{}?action={}".format(self.ip, form, action)
        try:
            r = self.session.post(url, data=json.dumps(form_paras), timeout=self.timeout)
            return json.loads(r.content)
        except requests.Timeout as err:
            print err.message


if __name__ == "__main__":
    # 举个栗子
    # 创建一个cpe实例，输入cpe参数：ip
    cpe_0 = CPE('192.168.200.1', 1)

    # 登录
    cpe_0.login()

    # 以节点node的方式查询状态信息，一次可以输入多个节点查询
    print u'查询webSessionTimeout和lteMainStatusGet的状态：'
    info_eg0 = cpe_0.get_node_info('webSessionTimeout', 'lteMainStatusGet')

    # 以节点node的方式设置状态信息，一次可以设置多个节点的状态信息
    print u'把webSessionTimeout设置为15，返回的message为null表示设置成功：'
    info_eg1 = cpe_0.set_node_info({"webSessionTimeout": "15"})

    # 以表单的方式查询状态信息，一次只能输入一个表单名称
    print u'查询WAN口状态，IP地址：'
    info_eg2 = cpe_0.get_form_info('wanStatus')

    # 以表单的方式设置状态信息，一次只能设置一个表单
    print u'增加一个macFilterList，返回的message为null表示设置成功：'
    info_eg2 = cpe_0.set_form_info('macFilterList', 'add', {"mac":"66:55:44:33:22:11"})
    print u'修改刚才增加的macFilterList，返回的message为null表示设置成功：'
    info_eg2 = cpe_0.set_form_info('macFilterList', 'set', {"id": 0, "mac":"11:66:22:55:33:44"})
    print u'删除刚才增加的macFilterList，返回的message为null表示设置成功：'
    info_eg2 = cpe_0.set_form_info('macFilterList', 'delete', {"id": 0})





