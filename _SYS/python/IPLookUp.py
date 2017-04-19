import re
import sys
import GeoIP

# Regex patterns
p1 = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

def formatLine1(line):   # determine if log file text string is right length, has correct characteristics
	"""Check line against requirements"""

	# Session IDs
	lineSplit = line.rstrip("\n").split("\t")

	source = 'unknown'

	rawip = lineSplit[10]
	m1 = p1.search(rawip)

	if m1:
		org = gi.org_by_addr(rawip)
		if org:
			source = org 
	n.write("\t".join(lineSplit[0:35]) + '\t' + source + '\t' + "\t".join(lineSplit[36:]) + "\n")

# read file path and name from command line
inputpath = sys.argv[1]
inputfile = sys.argv[2]
outputpath = sys.argv[3]
outputfile = sys.argv[4]
ipdata = sys.argv[5]

# open read and write files
f = open(inputpath + '/' + inputfile + '.log', 'r', encoding='latin-1')
n = open(outputpath + '/' + outputfile + '.log', 'w', encoding="latin-1")

# Read gi data and regions list from external files
gi = GeoIP.open(ipdata,GeoIP.GEOIP_STANDARD)

# cycle through lines, omitting those that don't match the relevant criteria
for line in f:
	formatLine1(line)
