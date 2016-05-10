#!/usr/bin/python
import sys
import subprocess
import argparse

def smb_scan(ip, output_dir):
        NBTSCAN = "nbtscan %s" % (ip)
        f=open("nbt_results_%s" % (ip),"a+")
        nbtresults = subprocess.check_output(NBTSCAN, shell=True)
        if ("Connection refused" not in nbtresults) and ("Connect error" not in nbtresults) and ("Connection reset" not in nbtresults):
            print "[*] SAMRDUMP User accounts/domains found on " + ip
            lines = nbtresults.split("\n")
            for line in lines:
                if ("Found" in line) or (" . " in line):
                    print "   [+] " + line
                    
        f.write(nbtresults)
        f.close()
                        
if __name__=='__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", help="Designates target IP")
        parser.add_argument("-d", help="Designates output_directory")
        args = parser.parse_args()

        if args.i == None or args.d == None:
            print "Usage: smbrecon.py -i <ip address> -d <output_dir>"
            sys.exit(0)
        smb_scan(args.i.strip(),args.d.strip())
 
 

