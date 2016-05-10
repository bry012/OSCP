#!/usr/bin/env python
import subprocess
import sys
import os
import argparse


def nmap_scan(ip_address,port,output_dir):
        print "INFO: Performing nmap FTP script scan for " + ip_address + ":" + port
        FTPSCAN = "nmap -sV -Pn -vv -p %s --script=ftp-anon,ftp-bounce,ftp-libopie,ftp-proftpd-backdoor,ftp-vsftpd-backdoor,ftp-vuln-cve2010-4221 -oN '%s/ftp/%s_ftp.nmap' %s" % (port, output_dir, ip_address, ip_address)
        subprocess.check_output(FTPSCAN, shell=True)

def hydra_scan(ip_address,port,output_dir):
        print "INFO: Performing hydra ftp scan against " + ip_address 
        HYDRA = "hydra -L wordlists/userlist -P wordlists/offsecpass -f -o %s/ftp/%s_ftphydra.txt -u %s -s %s ftp" % (output_dir,ip_address, ip_address, port)
        results = subprocess.check_output(HYDRA, shell=True)
        resultarr = results.split("\n")
        outfile= "%s/ftp/%s-%s_hydra_brute.txt" % (output_dir,ip_address,port)
        f = open(outfile, "a+")
        for result in resultarr:
            if "login:" in result:
                print "[*] Valid ftp credentials found: " + result 
                f.write("[*] Valid ftp credentials found: " + result)
        f.close()


if __name__=='__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", help="Designates target IP")
        parser.add_argument("-d", help="Designates output_directory")
        parser.add_argument("-p", help="Designates port")
        args = parser.parse_args()

        if args.i == None or args.d == None or args.d == None:
            print "Usage: ftprecon.py -i <ip address> -p <port> -d <output_dir>"
            sys.exit(0)
        if not os.path.exists(args.d + "/ftp/"):
                    os.makedirs(args.d + "/ftp/")

        nmap_scan(args.i.strip(),args.p.strip(),args.d.strip())
        hydra_scan(args.i.strip(),args.p.strip(),args.d.strip())


