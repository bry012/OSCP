@ECHO off
set command=%1
set file=%2

set tran_typ=%3

set ip=%4
 
echo open %ip% > ftp.txt

echo USER <username> <password> >> ftp.txt

echo %tran_typ%  >> ftp.txt

echo cd ftp >> ftp.txt
echo %command% %file% >> ftp.txt

echo bye >> ftp.txt

ftp -i -n -s:ftp.txt

del ftp.txt
