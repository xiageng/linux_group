#-*-coding:utf-8 -*-
__author__ = 'j6feng'
import re
import os,sys,time
from abc import abstractmethod
from optparse import OptionParser
ULPHYSyscomp = ["pusch","pucch","prach","srs","chan","rm"]
#please notice the word upper and lower
commonRegDict = {
    "fatal": [".*FATAL EXCEPTION Nid.*",".*FATAL DSPHWAPI ERROR Nid.*",".*ErrorDriver flushing LogManager queue.*"],
    "err_wrn": [".*(ERR|WRN)/.*"],
}
puschRegDict = {
    "pusch":[".*DBG/ULPHY/PUSCH.*(Ue\sMeas).*CellId:(\d+),subframe:(\d+),crnti:(\d+),rssi:([-]?\d.*),interfpower:([-]?\d.*),pre-snr:([-]?\d.*),fO:([-]?\d.*),tA:([-]?\d.*),postSnr:([-]?\d.*)",
             ".*DBG/ULPHY/PUSCH.*(Cell\sMeas\sslot\s\d).*CellId:(\d+),subframe:(\d+),bandwidth:(\d+),INP:.*",],
    "decoder":[".*ULPHY/DECOD#,.*",]
}
pucchRegDict = {"pucch":[".*\s(ERR|WRN)/ULPHY/PUCCH.*",],
                "chan":[".*\s(ERR|WRN)/ULPHY/CHAN.*",],
                }
srsRegDict = {
    "srs":[".*\s(ERR|WRN)/ULPHY/SRS.*",
           ".*ULPHY/SRSPreCombiner#.*",],
}
prachRegDict = {
    "prach":[".*INF/ULPHY/PRACH.*[Pp]rach.*[Rr]eceiver.*subcell:(\d.*)frequecy(.*\d.*)frame(.*\d+.*)subframe(.*\d+)",
             ".*INF/ULPHY/PRACH.*detect(.*\d.*)preamble.*frame(.*\d.*)subframe(.*\d.*)prach[Ii]ndex(.*\d.*)[Tt]a(.*\d+.*)fre[Oo]ff(.*\d+.*)",
             ".*INF/ULPHY/PRACH.*cellId(.*\d.*)detect(.*\d.*)preamble.*frames",],
}

class ULPHYlog(object):
    def __init__(self,logfile,resultPath,UlSysComp):
        self.logFile = logfile
        self.UlSysComp = UlSysComp
        self.resultPath = os.path.join(resultPath, self.UlSysComp + time.strftime("%Y%m%d%H%M"))
        os.mkdir(self.resultPath)
        self.fatal_log = os.path.join(self.resultPath,"fatal.log")
        self.err_wrn_log = os.path.join(self.resultPath,"err_wrn.log")
        self.fatal_data = []
        self.err_wrn_data = []

    def analyze(self):
        with open(self.logFile) as loghandler:
            lines = loghandler.readlines()
            for line in lines:
                self.commonLogFilter(line)
                self.specailLogFilter(line)
            self.specialLogSave()
            self.commonlogSave()
            loghandler.close()

    def commonLogFilter(self,data):
        self.FilterFun("fatal",commonRegDict,data,self.fatal_data)
        self.FilterFun("err_wrn", commonRegDict,data, self.err_wrn_data)

    def commonlogSave(self):
        self.saveData(self.fatal_log,self.fatal_data)
        self.saveData(self.err_wrn_log,self.err_wrn_data)

    def FilterFun(self,sysComp,RegDict,data,outputList):
        for i in range(len(RegDict[sysComp])):
            matchgroup = None
            matchgroup = re.match(r"{}".format(RegDict[sysComp][i]), data, re.I)
            if matchgroup is not None:
                outputList.append(data)
                break

    def saveData(self,resultFile,resultData):
        if resultData:
            special = open(resultFile, "w+")
            special.writelines(resultData)
            special.close()
        else:
            print("there is no %s")%(resultFile)

    # @abstractmethod
    # def specailLogFilter(self,data):
    #     pass
    @abstractmethod
    def specialLogSave(self):
        pass

class PUSCHlog(ULPHYlog):
    def __init__(self,logfile, resultPath, UlSysComp):
        super(PUSCHlog,self).__init__(logfile, resultPath, UlSysComp)
        self.resultPusch = os.path.join(self.resultPath,"pusch.log")
        self.resultDecoder = os.path.join(self.resultPath, "decoder.log")
        self.puschData = []
        self.decoderData = []

    def specailLogFilter(self,data):
        self.FilterFun("pusch",puschRegDict,data,self.puschData)
        self.FilterFun("decoder",puschRegDict, data, self.decoderData)

    def specialLogSave(self):
        self.saveData(self.resultPusch,self.puschData)
        self.saveData(self.resultDecoder, self.decoderData)

class PUCCHlog(ULPHYlog):
    def __init__(self,logfile, resultPath, UlSysComp):
        super(PUCCHlog,self).__init__(logfile, resultPath, UlSysComp)
        self.resultPucch = os.path.join(self.resultPath,"pucch.log")
        self.resultChan = os.path.join(self.resultPath,"chan.log")
        self.pucchData = []
        self.chanData = []

    def specailLogFilter(self, data):
        self.FilterFun("pucch", pucchRegDict, data, self.pucchData)
        self.FilterFun("chan", pucchRegDict, data, self.chanData)

    def specialLogSave(self):
        self.saveData(self.resultPucch, self.pucchData)
        self.saveData(self.resultChan, self.chanData)

class PRACHlog(ULPHYlog):
    def __init__(self,logfile, resultPath, UlSysComp):
        super(PRACHlog,self).__init__(logfile, resultPath, UlSysComp)
        self.resultPrach = os.path.join(self.resultPath,"prach.log")
        self.prachData = []

    def specailLogFilter(self,data):
        self.FilterFun("prach",prachRegDict,data,self.prachData)

    def specialLogSave(self):
        self.saveData(self.resultPrach,self.prachData)

class SRSlog(ULPHYlog):
    def __init__(self,logfile, resultPath, UlSysComp):
        super(SRSlog,self).__init__(logfile, resultPath, UlSysComp)
        self.resultSrs= os.path.join(self.resultPath,"srs.log")
        self.SrsData = []

    def specailLogFilter(self,data):
        self.FilterFun("srs",srsRegDict,data,self.SrsData)

    def specialLogSave(self):
        self.saveData(self.resultSrs,self.SrsData)

def get_user_paras():
    opt = OptionParser()
    opt.add_option("--ULSC", type="string", action="store",dest="UlSystemComponent", help="UlphySystemComponent: err_wrn/PUSCH(+decoder)/PUCCH(+chan)/PRACH/SRS/RM/")
    opt.add_option("--path", type="string", action="store",dest="logPath",help="syslog")
    (options, args) = opt.parse_args()
    UlSysComp = options.UlSystemComponent.lower()
    logFile = options.logPath
    if logFile is None:
        print("there is missing syslog path, Please input syslog path, usage: --path   logPath")
        sys.exit(1)
    # there will has modify if there is add err/wrn
    if not (UlSysComp in ULPHYSyscomp):
        print("Please input the correct ulphy system component")
        sys.exit(1)
    if UlSysComp is None:
        UlSysComp = "ALL"
        print("Now will filter ulphy pusch/pucch/prach/srs/channelizer/rm/decoder log")
    resultPath = os.path.dirname(logFile)
    if resultPath == "":
        resultPath = os.getcwd()
    return [UlSysComp, logFile,resultPath]

ULPHY_clases = {
    "pusch": PUSCHlog,
    "pucch": PUCCHlog,
    "prach": PRACHlog,
    "srs"  : SRSlog,
    # "chan" : [CHANlog,],
    # "rm"   : [RMlog,],
    # "decoder": [DECODERlog,],
}
if __name__ == '__main__':
    UlSysComp, logFile, resultPath = get_user_paras()
    ulphy_instance = ULPHY_clases[UlSysComp](logFile, resultPath, UlSysComp)
    ulphy_instance.analyze()
    #ulphyLog = UlphyLog(logFile,resultPath)
