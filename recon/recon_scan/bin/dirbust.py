#!/usr/bin/python

import sys
import os
import subprocess
import argparse

def dirbust_scan(url,scan_name, output_dir):
        folders = ["/usr/share/dirb/wordlists", "/usr/share/dirb/wordlists/vulns"]

        found = []
        print "INFO: Starting dirb scan for " + url
        for folder in folders:
            for filename in os.listdir(folder):

                outfile = " -o " + output_dir + "/" + scan_name + "_dirb_" + filename
                DIRBSCAN = "dirb %s %s/%s %s -S -r" % (url, folder, filename, outfile)
                print DIRBSCAN
                try:
                        results = subprocess.check_output(DIRBSCAN, shell=True)
                        resultarr = results.split("\n")
                        for line in resultarr:
                            if "+" in line:
                                    if line not in found:
                                        found.append(line)
                except Exception, e:
                    print e
                    pass

        try:
            print found
            if found[0] != "":
                print "[*] Dirb found the following items..."
                for item in found:
                    print "   " + item
        except Exception, e:
            print "INFO: No items found during dirb scan of " + url		

def usage():
        print "\n./dirbust.py -u <url> -n <scan_name> -d <output_dir>\n"

if __name__=='__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", help="Designates target url")
        parser.add_argument("-d", help="Designates output_directory")
        parser.add_argument("-n", help="Designates scan_name")
        args = parser.parse_args()
        
        if args.u == None or args.d == None or args.n == None:
                usage()
                
        else:
                dirbust_scan(args.u,args.n,args.d)

