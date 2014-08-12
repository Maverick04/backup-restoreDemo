cd %RsyncDIR%
call "%RsyncDIR%"\bin\rsync -ravz --itemize-changes --delete --progress --password-file="%rsyncPWDCYGFile%" %rsyncUser%@%machineIP%::%Module% %backupDIR% < "%rsyncPWDFile%" > "%RsyncDIR%"\%machineIP%_out.log 2>&1

