backup-restoreDemo
==================

Demo project about backup and restore testing invironment.

This demo describes a C/S model about how to backup and restore the test environment.

Developers need different testing invironments during software lifeclicle. While, not always enough machines(vms) are provided so they have to destory some environments to make space for new testing goals. This demo is used to backup the whole environment(softwares,datebases,configurations etc.) to the server and redeploy it when needed.

This demo uses bup(an opensource tool which uses git to track files and provides data compression) and rsync to sychronize data between server and client. It also provide SSH login and remote command.

This demo is finished during internship at IBM China Development Lib.

-Tong Yang July 2013
