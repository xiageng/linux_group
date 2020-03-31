#! /user/bin/enn python
#-*- coding: utf-8 -*-

import wx
import os,csv,re
import subprocess
from ute_admin import ute_admin
ute_admin = ute_admin()
import paramiko


class Main_Window(wx.Frame):
    def __init__(self,parent,title_test="BTS Detection"):
        wx.Frame.__init__(self,parent, title=title_test)
        #self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        #boxSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.nb = wx.Notebook(self)

        self.nb.AddPage(BTS_DATA_Panel(self.nb), "BTS Data Info")
        self.nb.AddPage(Fetch_Info_Panel(self.nb), "Fetch BTS Info")

        self.Centre(wx.BOTH)
        self.Show()


    def __del__(self):
        pass

class BTS_DATA_Panel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        fgSizer = wx.FlexGridSizer(0, 1, 0, 0)
        fgSizer.SetFlexibleDirection(wx.BOTH)
        fgSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        fgSizer2 = wx.FlexGridSizer(1, 3, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticTextbtsid = wx.StaticText(self, wx.ID_ANY, u"bts id:")
        self.m_staticTextbtsid.Wrap(-1)
        fgSizer1.Add(self.m_staticTextbtsid, 0, wx.ALL, 5)

        self.m_textCtrlbtsid = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString)
        fgSizer1.Add(self.m_textCtrlbtsid, 0, wx.ALL, 5)

        self.m_staticText_vmip = wx.StaticText(self, wx.ID_ANY, u"vm ip:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_vmip.Wrap(-1)
        fgSizer1.Add(self.m_staticText_vmip, 0, wx.ALL, 5)

        self.m_textCtrl_vmip = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.m_textCtrl_vmip, 0, wx.ALL, 5)

        self.m_staticText_user = wx.StaticText(self, wx.ID_ANY, u"user:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_user.Wrap(-1)
        fgSizer1.Add(self.m_staticText_user, 0, wx.ALL, 5)

        self.m_textCtrl_user = wx.TextCtrl(self, wx.ID_ANY, u"ute", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.m_textCtrl_user, 0, wx.ALL, 5)

        self.m_staticText_pw = wx.StaticText(self, wx.ID_ANY, u"password:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_pw.Wrap(-1)
        fgSizer1.Add(self.m_staticText_pw, 0, wx.ALL, 5)

        self.m_textCtrl_pw = wx.TextCtrl(self, wx.ID_ANY, u"ute", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.m_textCtrl_pw, 0, wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_button1, 0, wx.ALL, 5)
        self.m_button_update = wx.Button(self, wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_button_update, 0, wx.ALL, 5)
        self.m_button_show = wx.Button(self, wx.ID_ANY, u"Show Info", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer2.Add(self.m_button_show, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.OnClickAdd, self.m_button1)
        self.Bind(wx.EVT_BUTTON, self.OnClickUpdate, self.m_button_update)
        self.Bind(wx.EVT_BUTTON, self.OnClickShow, self.m_button_show)
        self.m_textCtrlbtsid.Bind(wx.EVT_LEFT_DCLICK, self.cleanbtsidtext)
        self.m_textCtrl_vmip.Bind(wx.EVT_LEFT_DCLICK, self.cleanvmiptext)
        self.m_textCtrl_user.Bind(wx.EVT_LEFT_DCLICK, self.cleanusertext)
        self.m_textCtrl_pw.Bind(wx.EVT_LEFT_DCLICK, self.cleanpasswordtext)
        fgSizer.Add(fgSizer1, 1, wx.EXPAND, 5)
        fgSizer.Add(fgSizer2, 1, wx.EXPAND, 5)

        self.SetSizer(fgSizer)
        self.Centre(wx.BOTH)
        self.Layout()

    def cleanbtsidtext(self, event):
        self.m_textCtrlbtsid.Clear()
    def cleanvmiptext(self, event):
        self.m_textCtrl_vmip.Clear()
    def cleanusertext(self, event):
        self.m_textCtrl_user.Clear()
    def cleanpasswordtext(self, event):
        self.m_textCtrl_pw.Clear()
    def OnClickAdd(self,event):
        csv_file=os.path.join(os.getcwd(),'bts_data.csv')
        self.fieldname = ["btsid", "vm_ip", "user", "password"]
        showtext=''
        self.btsid=self.m_textCtrlbtsid.GetValue()
        self.vm_ip=self.m_textCtrl_vmip.GetValue()
        self.user=self.m_textCtrl_user.GetValue()
        self.pw=self.m_textCtrl_pw.GetValue()

        if os.path.exists(csv_file):
            check_result=self.check_btsid(csv_file)
            if check_result:
                showtext="btsid:{} is existing, if you want to update btsid info, please use button Update".format(self.btsid)
            else:
                showtext="btsid:{},vm_ip:{} will be added".format(self.btsid,self.vm_ip)
                self.write_data(csv_file)
        else:
            showtext = "btsid:{},vm_ip:{} will be added".format(self.btsid, self.vm_ip)
            self.write_data(csv_file,fieldname=self.fieldname)
        dlg = wx.MessageDialog(self, showtext)
        dlg.ShowModal()
        dlg.Destroy()

    def OnClickUpdate(self,event):
        csv_file=os.path.join(os.getcwd(),'bts_data.csv')
        self.fieldname = ["btsid", "vm_ip", "user", "password"]
        showtext=''
        self.btsid=self.m_textCtrlbtsid.GetValue()
        self.vm_ip=self.m_textCtrl_vmip.GetValue()
        self.user=self.m_textCtrl_user.GetValue()
        self.pw=self.m_textCtrl_pw.GetValue()

        if os.path.exists(csv_file):
            check_result=self.check_btsid(csv_file)
            if check_result:
                showtext="btsid:{},vm_ip:{} is updating".format(self.btsid,self.vm_ip)
                self.update_data(csv_file)
            else:
                showtext="btsid:{} is not existing".format(self.btsid)
        else:
            showtext="btsid:{} is not existing".format(self.btsid)
        dlg = wx.MessageDialog(self, showtext)
        dlg.ShowModal()
        dlg.Destroy()

    def OnClickShow(self,event):
        csv_file = os.path.join(os.getcwd(), 'bts_data.csv')
        data=''
        showtext=''
        if os.path.exists(csv_file):
            with open(csv_file,"rb") as f:
                data=f.readlines()
                for line in data:
                    showtext=showtext+line
        dlg = wx.MessageDialog(self, showtext)
        dlg.ShowModal()
        dlg.Destroy()

    def update_data(self,csv_file):
        self.read_DataCenter(csv_file)

        for i in range(len(self.csv_data)):
            if self.csv_data[i]["btsid"]==self.btsid.lower():
                data = {"btsid": self.btsid.lower(), "vm_ip": self.vm_ip, "user": self.user, "password": self.pw}
                self.csv_data[i]=data
                break
        with open(csv_file,"wb") as f:
            writer = csv.DictWriter(f, self.fieldname)
            writer.writeheader()
            for line in self.csv_data:
                writer.writerow(line)

    def write_data(self,csv_file,fieldname=''):
        with open(csv_file, "ab") as f:
            writer = csv.DictWriter(f, fieldname)
            if len(fieldname)!=0:
                writer.writeheader()
            data = {"btsid":self.btsid.lower(),"vm_ip":self.vm_ip,"user":self.user,"password":self.pw}
            writer.writerow(data)
    def check_btsid(self,csv_file):
        self.read_DataCenter(csv_file)
        btsid = [line["btsid"] for line in self.csv_data]
        if self.btsid.lower() in btsid:
            return True
        return False

    def read_DataCenter(self,csv_file):
        if os.path.exists(csv_file):
            print csv_file
            with open(csv_file,"rb") as f:
                reader = csv.DictReader(f)
                self.csv_data = [row for row in reader]
                print self.csv_data

class Fetch_Info_Panel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        fgSizernew = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizernew.SetFlexibleDirection(wx.BOTH)
        fgSizernew.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticTextbtsid = wx.StaticText(self, wx.ID_ANY, u"bts id:")
        fgSizernew.Add(self.m_staticTextbtsid, 0, wx.ALL, 5)
        self.m_textCtrlbtsid = wx.TextCtrl(self, wx.ID_ANY, "bts823")
        fgSizernew.Add(self.m_textCtrlbtsid, 0, wx.ALL, 5)

        self.m_textCtrls1 = wx.TextCtrl(self, wx.ID_ANY, "s1")
        fgSizernew.Add(self.m_textCtrls1, 0, wx.ALL, 5)

        self.m_textCtrls1_value = wx.TextCtrl(self, wx.ID_ANY, "")
        fgSizernew.Add(self.m_textCtrls1_value, 0, wx.ALL, 5)

        self.button_fetch = wx.Button(self, wx.ID_ANY, u"Fetch", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizernew.Add(self.button_fetch, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.OnClickFetch, self.button_fetch)

        self.SetSizer(fgSizernew)
        self.Centre(wx.BOTH)
        self.Layout()

    def OnClickFetch(self,event):
        csv_file = os.path.join(os.getcwd(), 'bts_data.csv')
        self.scfc_path = os.path.join(os.getcwd(), "scfc")
        self.btsid=self.m_textCtrlbtsid.GetValue()
        info_data=self._search_file(csv_file,self.btsid)
        info_data=info_data.split(",")
        vm_ip=info_data[1]
        user=info_data[2]
        pw=info_data[3]
        if len(vm_ip):
            print vm_ip
        earfcn,s1_ip,s1_gateway=self.get_earfcn_s1()
        showtext = "btsid:{},earfcn:{},s1_ip:{},s1_gateway:{}".format(self.btsid,earfcn,s1_ip,s1_gateway)
        dlg = wx.MessageDialog(self, showtext)
        dlg.ShowModal()
        dlg.Destroy()

            #self.get_scfc(self.btsid,vm_ip)
    def _search_file(self,file,search_data):
        find_line=''
        with open(file,"rb")as f:
            data=f.readlines()
            for line in data:
                if search_data in line:
                    find_line=line
                    break
        return find_line

    def get_earfcn_s1(self):
        scfc_file = os.path.join(self.scfc_path, "{}_scfc.xml".format(self.btsid))
        earfcn_line=self._search_file(scfc_file,"name=\"earfcn\"")
        earfcn=re.search(".*>(\d+)<",earfcn_line).group(1)
        print earfcn_line,earfcn
        s1_line=self._search_file(scfc_file,"name=\"localIpAddr\"")
        s1_ip=re.search("(\d+\.\d*\.\d*\.\d*).*", s1_line).group(1)
        print s1_line,s1_ip
        s1_gateway_line=self._search_file(scfc_file,"name=\"gateway\"")
        s1_gateway = re.search("(\d+\.\d*\.\d*\.\d*).*", s1_gateway_line).group(1)
        print s1_gateway_line,s1_gateway
        return earfcn,s1_ip,s1_gateway


class MainApp(wx.App):
    def OnInit(self):
        self.title="BTS_App"
        Main_Window(None)
        #self.frame.Show()
        return True

def main():
    app = MainApp()
    app.MainLoop()


def get_scfc_file(btsid,vm_ip,user,pw):
    ute_admin.setup_admin(bts_host="192.168.255.1", bts_port=443, use_ssl=True, remote_host=vm_ip,
                          remote_host_username=user, remote_host_password=pw, alias="gxy")
    cmd='ssh ute@10.108.228.10 -o StrictHostKeyChecking=no python /home/ute/xiageng/bts_detection/scfc_get.py {} {} {} {}'.format(
        btsid, vm_ip, user, pw)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    error = p.stderr.read()
    output = p.stdout.read()
    print("error: {}".format(error))
    print("output: {}".format(output))

if __name__=="__main__":
    #main()
    get_scfc_file("bts4722","10.108.228.13","ute","ute")
