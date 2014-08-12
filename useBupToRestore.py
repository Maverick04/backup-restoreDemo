#!/usr/bin/python

#BACKUP BPM API
#NAME:	BackUpBPM
#ARGU:  UsageEnvName SnapshotName
#RETURN VALUE: True:SUCCEED False:FAIL
#DEVELOPER YANGTONG 2013-07-16

#import part
import os
import time
import sys
import commands
from backupUtil import *
#import pdb

#function defination
def CheckArgu(argu):
    if type(argu)==str and len(argu)>=1:   
    	return True
    else:
        return False 

def PrintUsage():
    return "Usage: RestoreEnvWithWinBup(bpmEnvName,bpmSnapshotName,restoreDIR,storeDIR)\n \
                bpmEnvName: Environment Name\n \
                bpmSnapshotName: BackUp Snapshot Name\n \
                restoreDIR: Dir will contain the files to be restored\n \
                storeDIR: Dir that stores packfile\n"

def RestoreEnvWithBup(bpmEnvName, bpmSnapshotName, restoreDIR, storeDIR):
    
    if CheckArgu(bpmEnvName) and CheckArgu(bpmSnapshotName) and CheckArgu(restoreDIR) and CheckArgu(storeDIR):
        pass
    else:
        msg = "[Argu Error]"
        msg += PrintUsage()
        return 1, msg

    
    RESTOREENVDIR=restoreDIR
    RESTOREFILENAME='/%s_%s/latest' % (bpmEnvName, bpmSnapshotName)  #restore env not just one VM

    #Check if RESTOREENVDIR exists
    if os.path.exists(storeDIR):
        pass
    else:
        msg = 'Directory %s Does not exist!' % storeDIR
        return 1, msg
    
    if not os.path.exists(RESTOREENVDIR):
        os.makedirs(RESTOREENVDIR, 0755)

    #Restore From Repo
    cmdread=getenv("bupDIR")+'/bin/bup -d '+storeDIR+' ls '+RESTOREFILENAME
    FileNames=os.popen(cmdread)
    #pdb.set_trace()
    for eachline in FileNames:
        eachline=eachline.rstrip('/\n')
        cmdrestore=getenv("bupDIR")+'/bin/bup -d'+storeDIR+' restore -C '+RESTOREENVDIR+' '+RESTOREFILENAME+'/'+eachline
        #print cmd
        re=os.system(cmdrestore)
        if re==0:
            print 'Restore '+eachline+' Compelted'
        else:
            msg = 'Fail To Restore '+eachline
            return re, msg
    return 0, ""
    
if __name__ =='__main__':
    code, msg = RestoreEnvWithBup(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    if code != 0:
          print msg
