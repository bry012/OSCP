#!/bin/bash
HOST='<ip>'
USER='<username>'
PASSWD='<passowrd>'

ftp -n -v $HOST << EOT 
user $USER $PASSWD
prompt
cd ftp 
put $1 
bye
EOT
