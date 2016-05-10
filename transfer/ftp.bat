echo open <ip> > ftp.txt
echo USER <username> >> ftp.txt
echo PASS <password> >> ftp.txt
echo ftp >> ftp.txt
echo bin >> ftp.txt
echo put <file> >> ftp.txt
echo bye >> ftp.txt
ftp -v -n -s:ftp.txt
