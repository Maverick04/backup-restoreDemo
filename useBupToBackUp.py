#!/usr/bin/python

#BACKUP BPM API
#NAME:	BackUpBPM
#ARGU:  UsageEnvName SnapshotName
#RETURN VALUE: 0:SUCCEED 1:FAIL
#DEVELOPER YANGTONG 2013-07-17

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
    return "Usage: BackUpEnvWithWinBup(bpmEnvName,bpmSnapshotName,backupDIR,storeDIR)\n \
                bpmEnvName: Environment Name\n \
                bpmSnapshotName: BackUp Snapshot Name\n \
                backupDIR: Dir contains the files to be backed \n \
                storeDIR: Dir that stores packfile\n"

def BackUpEnvWithBup(bpmEnvName,bpmSnapshotName,backupDIR,storeDIR):
#    pdb.set_trace()
    if CheckArgu(bpmEnvName) and CheckArgu(bpmSnapshotName) and CheckArgu(backupDIR) and CheckArgu(storeDIR):
        pass
    else:
        
        return 1, "Argument Error :" + PrintUsage()

    
    BACKUPFILENAME=bpmEnvName+'_'+bpmSnapshotName
    BACKENVDIR=backupDIR
    bupOutFile=getenv("baseDIR").replace("bin", BACKUPFILENAME+"_bup_out.log")

    #Check if BACKENVDIR&BackDir exists
    if os.path.exists(BACKENVDIR):
        pass
    else:
        msg = 'Backup Directories Do not exist!'
        return 1, msg
    
    if not os.path.exists(storeDIR):
        os.makedirs(storeDIR, 0755)
    #pdb.set_trace()
    #Make index
    
    cmdindex='%s/bin/bup -d %s index -u %s > %s 2>&1' % (getenv("bupDIR"), storeDIR, BACKENVDIR, bupOutFile)
    re=os.system(cmdindex)
    
    if re != 0:
        if re==3840:                    
            cmdinit='BUP_DIR=%s %s/bin/bup init >> %s 2>&1' % (storeDIR, bupOutFile)
            re=os.system(cmdinit)
            if re == 0:
                os.system(cmdindex)
            else:
                msg = 'Fail to init repo'
                return re, msg
        else:
            msg = 'Fail To Index'
            return re, msg
   
    #Backup To Local Repo
    
    cmd='%s/bin/bup -d %s save -n %s -9 --strip %s >> %s 2>&1' % (getenv("bupDIR"), storeDIR, BACKUPFILENAME, BACKENVDIR, bupOutFile)
    re=os.system(cmd)

    if re==0:
        msg = 'Save File Completed'
        return 0, msg
    else:
        msg = 'Fail To Save'
        return re, msg
    
if __name__ =='__main__':
    code, msg = BackUpEnvWithBup(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    if code != 0:
        print msg
