#!/usr/bin/env python
import subprocess
import sys
import argparse

def snmp_scan(ip_address, output_dir):
        snmpdetect = 0
        ONESIXONESCAN = "onesixtyone %s" % (ip_address)
        results = subprocess.check_output(ONESIXONESCAN, shell=True).strip()

        if results != "":
            if "Windows" in results:
                results = results.split("Software: ")[1]
                snmpdetect = 1
            elif "Linux" in results:
                results = results.split("[public] ")[1]
                snmpdetect = 1
            if snmpdetect == 1:
                print "[*] SNMP running on " + ip_address + "; OS Detect: " + results
                SNMPWALK = "snmpwalk -c public -v1 %s 1 > %s/recon_enum/results/%s_snmpwalk.txt" % (ip_address, output_dir, ip_address)
                results = subprocess.check_output(SNMPWALK, shell=True)

        NMAPSCAN = "nmap -vv -sV -sU -Pn -p 161,162 --script=snmp-netstat,snmp-processes %s" % (ip_address)
        results = subprocess.check_output(NMAPSCAN, shell=True)
        resultsfile = output_dir + "/recon_enum/results/" + ip_address + "_snmprecon.txt"
        f = open(resultsfile, "w")
        f.write(results)
        f.close

def usage():
        print "\n./snmprecon.py -i <ip_address> -d <output_dir>\n"

if __name__=='__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", help="Designates target ip")
        parser.add_argument("-d", help="Designates output_directory")
        args = parser.parse_args()
        if args.i == None or args.d == None:
                usage()
        else:
                snmp_scan(args.i.strip(),args.d.strip())
