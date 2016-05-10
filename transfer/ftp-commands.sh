#!/bin/bash
echo ftp-commands.sh <GET or PUT> <file> <bin or ascii> <host>
HOST=$4
USER='<username>'
PASSWD='<password>'
ftp -n -v $HOST << EOT 
user $USER $PASSWD
prompt
$3
cd ftp 
$1 $2 
bye
EOT
