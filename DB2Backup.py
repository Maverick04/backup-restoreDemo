#!/usr/bin/env python

#API Name: DB2 Offline Backup
#Arguments: None
#Return Value: Boolean
#Developer YANGTONG 2013-07-15

#import part
import os
import sys
import commands
import pdb

#function defination
def OfflineBackup():

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

    DBNAME=os.getenv("DBNAME")     #Get DBNAME what to do if more than one db?
    if DBNAME==None:
        print "Fail To Get DBNAME"
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
    cmd='db2 backup database '+DBNAME+' to '+DB2_DIR
    try:
        Result=commands.getstatusoutput(cmd)
        if Result[0]==0:
            return True
        else:
            print 'Backup Fail'    
    except Exception as e:
        print e
        sys.exit()

#main part
if __name__=='__main__':
    OfflineBackup()

			
        

    
  
	



	



