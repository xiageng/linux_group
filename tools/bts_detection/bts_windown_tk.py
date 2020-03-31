#! /user/bin/enn python
#-*- coding: utf-8 -*-
#import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import os,re,csv,subprocess
from ute_admin import ute_admin
ute_admin = ute_admin()
class Application(Frame):
    def __init__(self,master=None):
        Frame.__init__(self, master)
        nb=Notebook(master)
        nb.add(BTS_DATA_Panel(nb), text='BTS Data Info')
        nb.add(Fetch_Info_Panel(nb), text='Fetch BTS Info')
        nb.pack(expand=1, fill="both")

class BTS_DATA_Panel(Frame):
    def __init__(self, master=None):
        self.fieldnames = ["btsid", "vm_ip", "user", "password"]
        curpath = os.path.abspath(os.path.dirname(__file__))
        print("{}".format(curpath))
        self.csv_file = os.path.join(curpath, 'bts_data.csv')
        Frame.__init__(self, master)
        self.grid()
        Label(self, text="bts id:").grid(row=0)
        self.m_textCtrlbtsid=Entry(self)
        self.m_textCtrlbtsid.grid(row=0, column=1)
        Label(self, text="vm ip:").grid(row=1)
        self.m_textCtrl_vmip=Entry(self)
        self.m_textCtrl_vmip.grid(row=1, column=1)
        Label(self, text="user:").grid(row=2)
        self.m_textCtrl_user=Entry(self)
        self.m_textCtrl_user.grid(row=2, column=1)
        Label(self, text="password:").grid(row=3)
        self.m_textCtrl_pw=Entry(self)
        self.m_textCtrl_pw.grid(row=3, column=1)
        Button(self, text='Add', command=self.OnClickAdd).grid(row=4, column=0)
        Button(self, text='Update', command=self.OnClickUpdate).grid(row=4, column=1)
        Button(self, text='Show', command=self.OnClickShow).grid(row=4, column=2)


    def OnClickAdd(self):
        csv_file=self.csv_file
        showtext=''
        self.btsid=self.m_textCtrlbtsid.get()
        self.vm_ip=self.m_textCtrl_vmip.get()
        self.user=self.m_textCtrl_user.get()
        self.pw=self.m_textCtrl_pw.get()

        if os.path.exists(csv_file):
            check_result=self.check_btsid(csv_file)
            if check_result:
                showtext="btsid:{} is existing, if you want to update btsid info, please use button Update".format(self.btsid)
            else:
                showtext="btsid:{},vm_ip:{} will be added".format(self.btsid,self.vm_ip)
                self.write_data(csv_file,self.fieldnames,flag=False)
        else:
            showtext = "btsid:{},vm_ip:{} will be added".format(self.btsid, self.vm_ip,flag=True)
            self.write_data(csv_file,fieldname=self.fieldnames)
        showinfo(title="Add bts id",message=showtext)

    def OnClickUpdate(self):
        csv_file=self.csv_file
        self.fieldname = ["btsid", "vm_ip", "user", "password"]
        showtext=''
        self.btsid=self.m_textCtrlbtsid.get()
        self.vm_ip=self.m_textCtrl_vmip.get()
        self.user=self.m_textCtrl_user.get()
        self.pw=self.m_textCtrl_pw.get()

        if os.path.exists(csv_file):
            check_result=self.check_btsid(csv_file)
            if check_result:
                showtext="btsid:{},vm_ip:{} is updating".format(self.btsid,self.vm_ip)
                self.update_data(csv_file)
            else:
                showtext="btsid:{} is not existing".format(self.btsid)
        else:
            showtext="btsid:{} is not existing".format(self.btsid)
        showinfo(title="Update bts id",message=showtext)

    def OnClickShow(self):
        csv_file = self.csv_file
        data=''
        showtext=''
        if os.path.exists(csv_file):
            with open(csv_file,"r") as f:
                data=f.readlines()
                for line in data:
                    showtext=showtext+line
        showinfo(title="Show all",message=showtext)

    def update_data(self,csv_file):
        self.read_DataCenter(csv_file)

        for i in range(len(self.csv_data)):
            if self.csv_data[i]["btsid"]==self.btsid.lower():
                data = {"btsid": self.btsid.lower(), "vm_ip": self.vm_ip, "user": self.user, "password": self.pw}
                self.csv_data[i]=data
                break
        with open(csv_file,"w") as f:
            writer = csv.DictWriter(f, self.fieldname)
            #writer.writeheader()
            for line in self.csv_data:
                writer.writerow(line)

    def write_data(self,csv_file,fieldname,flag=False):
        with open(csv_file, "a") as f:
            writer = csv.DictWriter(f, fieldname)
            if flag:
                writer.writeheader()
            data = {"btsid":self.btsid.lower(),"vm_ip":self.vm_ip,"user":self.user,"password":self.pw}
            print(data)
            writer.writerow(data)
    def check_btsid(self,csv_file):
        self.read_DataCenter(csv_file)
        btsid = [line["btsid"] for line in self.csv_data]
        if self.btsid.lower() in btsid:
            return True
        return False

    def read_DataCenter(self,csv_file):
        if os.path.exists(csv_file):
            print(csv_file)
            with open(csv_file,"r") as f:
                reader = csv.DictReader(f,fieldnames=self.fieldnames)
                self.csv_data = [row for row in reader]
                print(self.csv_data)

class Fetch_Info_Panel(Frame):
    def __init__(self,master=None):
        self.fieldnames = ["btsid", "vm_ip", "user", "password"]
        curpath = os.path.abspath(os.path.dirname(__file__))
        print("{}".format(curpath))
        self.csv_file = os.path.join(curpath, 'bts_data.csv')
        self.scfc_path = os.path.join(curpath, "scfc")
        Frame.__init__(self, master)
        self.grid()
        Label(self, text="bts id:").grid(row=0)
        self.m_textCtrlbtsid = Entry(self)
        self.m_textCtrlbtsid.grid(row=0, column=1)
        Label(self, text="s1 ip:").grid(row=1)
        self.e1 = StringVar()
        self.m_textCtrls1_ip = Entry(self,textvariable=self.e1)
        self.m_textCtrls1_ip.grid(row=1, column=1)
        Label(self, text="s1 gateway:").grid(row=2)
        self.e2 = StringVar()
        self.m_textCtrls1_gate = Entry(self,textvariable=self.e2)
        self.m_textCtrls1_gate.grid(row=2, column=1)
        Label(self, text="earfcn:").grid(row=3)
        self.e3 = StringVar()
        self.m_textCtrlsarfcn = Entry(self,textvariable=self.e3)
        self.m_textCtrlsarfcn.grid(row=3, column=1)
        self.showtext=""
        Button(self, text='Fetch', command=self.OnClickFetch).grid(row=4, column=0)
        Button(self, text='Check', command=self.OnClickCheck).grid(row=4, column=1)


    def OnClickFetch(self):
        csv_file = self.csv_file
        self.btsid=self.m_textCtrlbtsid.get()
        print(csv_file)
        info_data=self._search_file(csv_file,self.btsid)
        print(info_data)
        info_data=info_data.split(",")
        vm_ip=info_data[1]
        user=info_data[2]
        pw=info_data[3]
        if len(vm_ip):
            print(vm_ip)
            self.get_scfc(self.btsid,vm_ip,user,pw)
        earfcn,s1_ip,s1_gateway=self.get_earfcn_s1(self.btsid)
        self.e1.set(s1_ip)
        self.e2.set(s1_gateway)
        self.e3.set(earfcn)


    def OnClickCheck(self):
        self.showtext=''
        showtext=''
        dict_earfcn={}
        dict_s1ip={}
        dict_s1_gateway={}
        self.read_DataCenter(self.csv_file)
        for line in self.csv_data:
            self.get_scfc(line["btsid"],line["vm_ip"],line["user"],line["password"])
            earfcn,s1_ip,s1_gateway = self.get_earfcn_s1(line["btsid"])
            dict_earfcn[line["btsid"]]=earfcn
            dict_s1ip[line["btsid"]] = s1_ip
            dict_s1_gateway[line["btsid"]] = s1_gateway
            showtext =showtext + "btsid:{},earfcn:{},s1_ip:{},s1_gateway:{}\n".format(line["btsid"],earfcn,s1_ip,s1_gateway)
        print(dict_earfcn,dict_s1ip,dict_s1_gateway)
        earfcn_showinfo=self.check_duplicate(dict_earfcn)
        s1ip_showinfo=self.check_duplicate(dict_s1ip)
        s1_gateway_showinfo=self.check_duplicate(dict_s1_gateway)
        if len(earfcn_showinfo):
            earfcn_txt="{}\n".format(earfcn_showinfo)
        if len(s1ip_showinfo):
            s1ip_txt="{}\n".format(s1ip_showinfo)
        showtext= showtext + "SCFC info:\n"+ "{}".format(self.showtext) +"Duplicated info:\n" \
                  + earfcn_txt + s1ip_txt
        showinfo(title="Show all",message=showtext)

    def check_duplicate(self,info_dict):
        duplicate={}
        bts_id=[]
        item_value=info_dict.values()
        result=(len(item_value)==len(set(item_value)))
        if not result:
            item_set=set(item_value)
            for item in item_set:
                if item_value.count(item)>1:
                    bts_id = []
                    for info_key,info_value in info_dict.items():
                        if item == info_value:
                            bts_id.append(info_key)
                    duplicate[item]=bts_id
        return duplicate

    def read_DataCenter(self, csv_file):
        if os.path.exists(csv_file):
            print(csv_file)
            with open(csv_file, "r") as f:
                reader = csv.DictReader(f, fieldnames=self.fieldnames)
                self.csv_data = [row for row in reader]
                print(self.csv_data)
    def _search_file(self,file,search_data):
        find_line=''
        with open(file,"r")as f:
            data=f.readlines()
            for line in data:
                if search_data in line:
                    find_line=line
                    break
        return find_line

    def get_scfc(self,btsid, vm_ip, user, pw):
        scfc_path=self.scfc_path
        if not os.path.exists(scfc_path):
            os.mkdir(scfc_path)
        scfc_file = os.path.join(scfc_path, "{}_scfc.xml".format(btsid))
        if os.path.exists(scfc_file):
            os.system("rm -r {}".format(scfc_file))
        try:
            ute_admin.setup_admin(bts_host="192.168.255.1", bts_port=443, use_ssl=True, remote_host=vm_ip,
                                  remote_host_username=user, remote_host_password=pw, alias="gxy")
            ute_admin.collect_scf(scfc_file, alias="gxy")
            ute_admin.teardown_admin(alias="gxy")
        except Exception as e:
            print("cann't get bts id:{} scfc file".format(btsid))
            self.showtext = self.showtext + "cann't get bts id:{} scfc file\n".format(btsid)

    def get_earfcn_s1(self,btsid):
        scfc_file = os.path.join(self.scfc_path, "{}_scfc.xml".format(btsid))
        earfcn_line=self._search_file(scfc_file,"name=\"earfcn\"")
        earfcn=re.search(".*>(\d+)<",earfcn_line).group(1)
        print(earfcn_line,earfcn)
        s1_line=self._search_file(scfc_file,"name=\"localIpAddr\"")
        s1_ip=re.search("(\d+\.\d*\.\d*\.\d*).*", s1_line).group(1)
        print(s1_line,s1_ip)
        s1_gateway_line=self._search_file(scfc_file,"name=\"gateway\"")
        s1_gateway = re.search("(\d+\.\d*\.\d*\.\d*).*", s1_gateway_line).group(1)
        print(s1_gateway_line,s1_gateway)
        return earfcn,s1_ip,s1_gateway


def main():
    root = Tk()
    root.title(string='bts_detection')
    app=Application(root)
    root.mainloop()


if __name__=="__main__":
    main()
    pass