#!/usr/bin/python

from subprocess import *
from backupUtil import *
from stat import *
import os, sys
from useBupToBackUp import *
from useBupToRestore import *

parameters = {}

def _db2_BackUp(bpmEnvName,dbMachine):
    info = dbMachine.split("#")
    if len(info) < 4:
        return 1, "dbMachine Information is incorrect, should be db2AdminUser#db2Password#db2MachineIP#db2ExeFilePath#dbBackUpDIR"
    username = info[0]
    password = info[1]
    machineIP = info[2]
    db2Exe = info[3]
    dbBackUpDIR = info[4]
    db2MachineBKDIR = getenv("baseBackUpDIRCYG")+"/"+bpmEnvName+"/DB2_"+machineIP
    if not os.path.exists(db2MachineBKDIR):
        os.makedirs(db2MachineBKDIR, 0777)
    backupDBs = ["BPMDB", "CMNDB", "PDWDB"]
    cmds = ["%s force application all" % db2Exe]
    cmds.append(cmds[0])
    for backupDB in backupDBs:
        dbName = getenv(backupDB)
        cmds.append("%s BACKUP DATABASE %s TO %s" % (db2Exe, dbName, dbBackUpDIR))
    errorcode, msg = exeRemoteCmds(username, password, machineIP, cmds)
	
    platform = _getos()
    if platform == "windows":
        errorCode, msg = _callWinRsync(machineIP, db2MachineBKDIR, "db2")
        if errorCode != 0:
            return errorCode, msg
    elif platform == "linux":
        errorCode, msg = _callRsync(machineIP, db2MachineBKDIR, "db2")
        if errorCode != 0:
            return errorCode, msg
    else:
        (errorCode, msg) = (1, "Unknow Platform")
    return errorcode, msg
    
def _oracle_BackUp(dbMachine):
    print dbMachine
    
def _sqlServer_BackUp(dbMachine):
    print dbMachine

def _backupBPM(bpmEnvName, machineIP):
    bpmEnvPath = os.path.join(getenv("baseBackUpDIR")+os.sep, bpmEnvName)
    bpmMachinePath = os.path.join(bpmEnvPath, "BPM_"+machineIP)
    bpmMachineBKDIR = getenv("baseBackUpDIRCYG")+"/"+bpmEnvName+"/BPM_"+machineIP
    if not os.path.exists(bpmEnvPath):
        os.makedirs(bpmEnvPath, 0777)
    if not os.path.exists(bpmMachinePath):
        os.makedirs(bpmMachinePath, 0777)
    platform = _getos()
    if platform == "windows":
        errorCode, msg = _callWinRsync(machineIP, bpmMachineBKDIR, "bpm")
        if errorCode != 0:
            return errorCode, msg
    elif platform == "linux":
        errorCode, msg = _callRsync(machineIP, bpmMachinePath, "bpm")
        if errorCode != 0:
            return errorCode, msg
    else:
        (errorCode, msg) = (1, "Unknow Platform")
    return errorCode, msg
    

def _getos():
    if os.name == "nt":
        return "windows"
    elif os.name == "posix":
        return "linux"
    else:
        return "unKnown"
    
def _callWinRsync(machineIP, bpmMachinePath, module):
#    stdoutFile = file(os.path.join(getenv("RsyncDIR", RsyncDIR),machineIP+"_stdout.log"), 'w')
#    stderrFile = file(os.path.join(getenv("RsyncDIR", RsyncDIR),machineIP+"_stderr.log"), 'w')
    passwordFile = file(getenv("rsyncPWDFile"))
    password = passwordFile.read()
    passwordFile.close()
#    print password
    cmd = "\""+os.path.join(getenv("baseDIR"), "")+"\"callRsync.bat"
#    print cmd, bpmMachinePath
    os.putenv('RsyncDIR', getenv("RsyncDIR"))
    os.putenv('machineIP', machineIP)
    os.putenv('backupDIR', bpmMachinePath)
    os.putenv('RSYNC_PASSWORD', password)
    os.putenv('rsyncPWDCYGFile', rsyncPWDCYGFile)
    os.putenv("Module", module)
    os.putenv("rsyncUser", getenv("rsyncUser"))
    os.putenv("rsyncPWDFile", getenv("rsyncPWDFile"))
    p = os.popen(cmd).readlines()
    outputFile = file(os.path.join(getenv("RsyncDIR"), machineIP+"_out.log"))
    errorCode = 1
    msg = "Error happens when using rsync to get remote BPM files, check log file %s for the details : \n" % os.path.join(getenv("RsyncDIR"), machineIP+"_out.log") 
    for line in outputFile.readlines():
        if line.find("receiving incremental file") != -1:
            errorCode = 0
            msg = ""
#            os.remove(os.path.join(getenv("RsyncDIR", RsyncDIR), machineIP+"_out.log"))
            break
        else:
            msg+=line
    return errorCode, msg

def _callRsync(machineIP, bpmMachinePath, module):
    passwordFile = file(getenv("rsyncPWDFile"))
    password = passwordFile.read()
    passwordFile.close()
#    print password
    cmd = "%s/bin/rsync -ravz --itemize-changes --delete --progress --password-file=%s %s@%s::%s %s < %s > %s/%s_out.log 2>&1" \
    % (getenv("RsyncDIR"), getenv("rsyncPWDFile"), getenv("rsyncUser"), machineIP, module, bpmMachinePath, getenv("rsyncPWDFile"), getenv("baseDIR"), machineIP)
#    print cmd, bpmMachinePath
    os.putenv('RSYNC_PASSWORD', password)
    p = os.popen(cmd).readlines()
    outputFile = file(os.path.join(getenv("baseDIR"), machineIP+"_out.log"))
    errorCode = 1
    msg = "Error happens when using rsync to get remote BPM files, check log file %s for the details : \n" % os.path.join(getenv("baseDIR"), machineIP+"_out.log") 
    for line in outputFile.readlines():
        if line.find("receiving incremental file") != -1:
            errorCode = 0
            msg = ""
#            os.remove(os.path.join(getenv("RsyncDIR", RsyncDIR), machineIP+"_out.log"))
            break
        else:
            msg+=line
    return errorCode, msg

def __printUsage(scriptName):
    print "Usage: %s -envName backup_BPM_Env_Name -snapshot backup_SnapshotName \
    -dbType DB2 -dbMachine db2AdminUser#db2Password#db2MachineIP#db2ExeFilePath#dbBackUpDIR\
     -bpmMachines backup_BPM_MachineIP01 ...." % scriptName
    sys.exit()
    
def _loadParameter(parameter):
    global parameters
    i = 1
    while i<len(parameter):
        key = parameter[i]
        if key.find("-") != 0:
            __printUsage(parameter[0])
            
        if key == "-bpmMachines":
            parameters[key[1:]] = parameter[i+1:]
            break
        else:
            parameters[key[1:]] = parameter[i+1]
            i+=2
#    print parameters
    
def backupBPMEnv():
    global parameters
    
    dbFunc = {"DB2": _db2_BackUp,
          "Oracle": _oracle_BackUp,
          "SQLServer": _sqlServer_BackUp}
    
    bpmEnvName = parameters["envName"]
    bpmSnapshotName = parameters["snapshot"]
    bpmDBType = parameters["dbType"]
    dbMachine = parameters["dbMachine"]
    bpmMachines = parameters["bpmMachines"]
    
    errorCode, msg = 0, ""
    for bpmMachine in bpmMachines:
        errorCode, msg = _backupBPM(bpmEnvName, bpmMachine)
        if errorCode != 0:
            msg = "[Error] Error happens when backup BPM Machine "+bpmMachine+" : "+msg
            return errorCode, msg
    
    dbFunc[bpmDBType](bpmEnvName,dbMachine)
    
    platform = _getos()
    
    backupDIR = getenv("baseBackUpDIRCYG")+"/"+bpmEnvName
    dataStoreDIR = getenv("storeDIR")
    
    if platform == "windows":
        errorCode, msg = BackUpEnvWithWinBup(bpmEnvName, bpmSnapshotName, backupDIR, dataStoreDIR)
        if errorCode != 0:
            return errorCode, msg
    elif platform == "linux":
        errorCode, msg = BackUpEnvWithBup(bpmEnvName, bpmSnapshotName, backupDIR, dataStoreDIR)
        if errorCode != 0:
            return errorCode, msg
    else:
        (errorCode, msg) = (1, "Unknow Platform")
    return errorCode, msg

if __name__ == "__main__":
    if len(sys.argv) < 11:
        __printUsage(sys.argv[0])
        
    _loadParameter(sys.argv[:])
    errorCode, msg = backupBPMEnv()
    if errorCode != 0:
        print msg
