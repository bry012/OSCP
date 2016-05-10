#!/usr/bin/env python
import subprocess
import argparse

def dns_scan(ip_address, output_dir):
        HOSTNAME = "nmblookup -A %s | grep '<00>' | grep -v '<GROUP>' | cut -d' ' -f1" % (ip_address)# grab the hostname         
        host = subprocess.check_output(HOSTNAME, shell=True).strip()
        print "INFO: Attempting Domain Transfer on " + host
        #ZT = "dig @%s.thinc.local thinc.local axfr" % (host)
        ZT = "dig @%s thinc.local axfr" % (ip_address)
        ztresults = subprocess.check_output(ZT, shell=True)
        if "failed" in ztresults:
            print "INFO: Zone Transfer failed for " + host
        else:
            print "[*] Zone Transfer successful for " + host + "(" + ip_address + ")!!! [see output file]"
            outfile = "%s/recon_enum/results/%s_zonetransfer.txt" % (output_dir, ip_address)
            dnsf = open(outfile, "w")
            dnsf.write(ztresults)
            dnsf.close
def usage():
        print "\n./dnsrecon.py -i <ip_address> -d <output_dir>\n"

if __name__=='__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", help="Designates target ip")
        parser.add_argument("-d", help="Designates output_directory")
        args = parser.parse_args()
        if args.i == None or args.d == None:
                usage()
        else:
                dns_scan(args.i.strip(),args.d.strip())
