#!/usr/bin/env python

#API Name: DB2 Full Restore
#Arguments: TimeStamp: String
#Return Value: True/False
#Developer YANGTONG 2013-07-15

#import part
import os
import sys
import commands
import pdb
import pexpect

#function defination
def OfflineBackup(TIMESTAMP):

    DBNAME=os.getenv("DBNAME")     #Get DBNAME what to do if more than one db?
    if DBNAME==None:
        print "Fail To Get DBNAME"
        return False

    DB2_DIR=os.getenv("DB2_DIR")     #Get DB2 BACKUP Directory
    if DB2_DIR==None:
        print "Fail To Get DB2_DIR"
        return False
    else:
        if os.path.isdir(DB2_DIR):
            pass
        else:
            print "Backup Directiory Does Not Exist"
            return False

    Filenames=os.listdir(DB2_DIR)  # shi fou he li? 
    for filename in Filenames:
        if filename.find(DBNAME) and filename.find(TIMESTAMP):
            break
    else:
        print "No Backup for Specific TimeStamp"
        return False


    Result=commands.getstatusoutput('db2 force applications all') #Stop Applications
    if Result[0]==1024:
        print "No start database manager command was issued"
        return False
    elif Result[0]==0:
        Result=commands.getstatusoutput('db2 list applications')
        if Result[0]==0:
            commands.getstatus('db2 force applications all')
        else:
            print 'Applications Stopped'

    cmd='db2 restore database '+DBNAME+' from '+DB2_DIR+' taken at '+TIMESTAMP

    try: 
        child=pexpect.spawn(cmd)              #restore backup
        child.logfile=sys.stdout
        child.expect('continue')
        child.sendline('y')
        child.expect(pexpect.EOF)

        cmd='db2 rollforward database '+DBNAME+' to end of logs and stop'
        Result=commands.getstatusoutput(cmd)  #rollback log
        if Result[0]==0:
            return True
        else:
            print 'Restore Fail'    
    except Exception as e:
        print e
        sys.exit()

#main part
if __name__=='__main__':
    OfflineBackup('20130715002709')
