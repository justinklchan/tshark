#!/usr/local/bin/python3
import threading
import sys
import os
import platform
import subprocess
import json
import time
import socket
import subprocess
import urllib.request
from datetime import datetime
from pytz import timezone    

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
myip=s.getsockname()[0]
s.close()

seen=[]

def ip2loc(ip):
	content = urllib.request.urlopen("http://ip-api.com/line/"+ip).read().decode('UTF-8')
	elts = content.split("\n")
	if elts[0] == "success":
		print(elts[1])
		print(elts[4])
		print(elts[5])
		print(elts[10])
		print(elts[11])
		print(elts[12])
		south_africa = timezone(elts[9])
		sa_time = datetime.now(south_africa)
		print(sa_time.strftime('%H:%M:%p'))
		print("====================================")

def exec():
	global lastip
	command = ['tshark', '-a', 'duration:2', '-w', 'out.txt']
	run_tshark = subprocess.Popen(
	    command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	run_tshark.communicate()

	command = ['tshark', '-r', 'out.txt']
	run_tshark = subprocess.Popen(
	    command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	output = run_tshark.communicate()[0]

	try:
		for line in output.decode('utf-8').split('\n'):
			if "UDP" in line and myip in line:
				elts=line.split()
				if elts[2] == myip:
					if elts[4] not in seen:
						ip2loc(elts[4])
						seen.append(elts[4])
	except:
		pass

while True:
	exec()
