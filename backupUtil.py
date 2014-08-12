#!/usr/bin/python

from backupProperties import *
import os
import paramiko

properties = {
"baseDIR": baseDIR,
"baseBackUpDIR": baseBackUpDIR,
"baseBackUpDIRCYG": baseBackUpDIRCYG,
"RsyncDIR": RsyncDIR,
"rsyncPWDFile": rsyncPWDFile,
"storeDIR": storeDIR,
"bupDIR": bupDIR,
"rsyncUser": rsyncUser,
"BPMDB": BPMDB,
"CMNDB": CMNDB,
"PDWDB": PDWDB,
"rsyncPWDCYGFile": rsyncPWDCYGFile
}

def getenv(envName):
    global properties
    default = properties[envName]
    return os.getenv(envName, default)

def exeRemoteCmds(username, password, machineIP, cmds):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(machineIP,22,username,password,timeout=20)
#        outputf = open(outputFile, 'w')
        msg = ""
        errorCode = 0
        for m in cmds:
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.readlines()
            err = stderr.readlines()
            msg=msg+"[Command]:"+m+"\n[OUT]:"+str(out)+"\n[ERR]:"+str(err)+"\n"
            
    except Exception,e:
        errorCode = 1
	msg = ""
        msg = msg+ "Got exception :" + str(e)
    finally:
        ssh.close()
    return errorCode, msg
