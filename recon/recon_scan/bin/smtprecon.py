#!/usr/bin/python
import socket
import sys
import subprocess
import argparse

#SMTPSCAN = "nmap -vv -sV -Pn -p 25,465,587 --script=smtp-vuln* %s" % (ip_address)
#results = subprocess.check_output(SMTPSCAN, shell=True)

#f = open("/root/scripts/recon_enum/results/smtpnmapresults.txt", "a")
#f.write(results)
#f.close


def smtp_scan(ip_address,port,output_dir):
        print "INFO: Trying SMTP Enum on " + ip_address
        names = open('/usr/share/wfuzz/wordlist/fuzzdb/wordlists-user-passwd/names/namelist.txt', 'r')
        f=open("%s/%s-%s_smtp_vrfy.txt" % (output_dir, ip_address,port), "a+")
        for name in names:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect=s.connect((ip_address,25))
            banner=s.recv(1024)
            s.send('HELO 1337@haxor.org \r\n')
            result= s.recv(1024)
            s.send('VRFY ' + name.strip() + '\r\n')
            result=s.recv(1024)
            if ("not implemented" in result) or ("disallowed" in result):
                    sys.exit("INFO: VRFY Command not implemented on " + ip_address) 
            if (("250" in result) or ("252" in result) and ("Cannot VRFY" not in result)):
                    print "[*] SMTP VRFY Account found on " + ip_address + ": " + name.strip()	
                    f.write("[*] SMTP VRFY Account found on " + ip_address + ": " + name.strip())	
                    f.close()
                    s.close()


def usage():
        print "\n./smtprecon.py -i <ip> -d <output_dir>\n"

if __name__=='__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", help="Designates target ip")
        parser.add_argument("-d", help="Designates output_directory")
        args = parser.parse_args()
        
        if args.i == None or args.d == None:
                usage()
                
        else:
                smtp_scan(args.i,25,args.d)

