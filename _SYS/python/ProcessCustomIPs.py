import re
import sys
import csv
import ipaddress
import socket
import binascii

p1 = re.compile('^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2})$')
p2 = re.compile('^0*(\d{1,3})\.0*(\d{1,3})\.0*(\d{1,3})\.0*(\d{1,3})$')
p3 = re.compile('^0*(\d{1,3})\.0*(\d{1,3})\.0*(\d{1,3})\.0*(\d{1,3})-0*(\d{1,3})\.0*(\d{1,3})\.0*(\d{1,3})\.0*(\d{1,3})$')

# read file path and name from command line
datapath = sys.argv[1]
inputfile = sys.argv[2]
outputfile = sys.argv[3]

ranges = []

with open(datapath + '/' + inputfile, newline='') as csvfile:
	rawip = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in rawip:
		name = '\"' + str(re.sub(',','',row[1])) + '\"'

		m1 = p1.search(row[0])
		m2 = p2.search(row[0])
		m3 = p3.search(row[0])

		if m1:
			_entry = []
			doms = ipaddress.IPv4Network(row[0])
			domA = str(doms[0])
			domB = str(doms[-1])
			_entry.append(int(binascii.hexlify(socket.inet_aton(domA)),16))
			_entry.append(int(binascii.hexlify(socket.inet_aton(domB)),16))
			_entry.append(name)
			ranges.append(_entry)
		if m2:
			_entry = []
			domA = str(m2.group(1) + '.' + m2.group(2) + '.' + m2.group(3) + '.' + m2.group(4))
			domB = str(m2.group(1) + '.' + m2.group(2) + '.' + m2.group(3) + '.' + m2.group(4))
			_entry.append(int(binascii.hexlify(socket.inet_aton(domA)),16))
			_entry.append(int(binascii.hexlify(socket.inet_aton(domB)),16))
			_entry.append(name)
			ranges.append(_entry)
		elif m3:
			_entry = []
			domA = str(m3.group(1) + '.' + m3.group(2) + '.' + m3.group(3) + '.' + m3.group(4))
			domB = str(m3.group(5) + '.' + m3.group(6) + '.' + m3.group(7) + '.' + m3.group(8))
			_entry.append(int(binascii.hexlify(socket.inet_aton(domA)),16))
			_entry.append(int(binascii.hexlify(socket.inet_aton(domB)),16))
			_entry.append(name)
			ranges.append(_entry)

with open(datapath + '/' + outputfile, 'w', newline='') as csvfile:
	newcsv = csv.writer(csvfile, delimiter=',', quotechar='|')
	for range in ranges:
		newcsv.writerow(range)
