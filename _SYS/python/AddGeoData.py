import re
import sys
import GeoIP

# Regex patterns
p1 = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

# Functions
def formatLine1(line):   # determine if log file text string is right length, has correct characteristics
	"""Check line against requirements"""

	# GeoIP lookups
	lineSplit=line.rstrip("\n").split("\t")
	country = "-"
	region = "-"

	rawip = lineSplit[10]
	m1 = p1.search(rawip)
	if m1:
		record = gi.record_by_addr(rawip)
		if record:
			if record['country_name']:
				country = str(record['country_name'])
			if record['region_name']:
				region = str(record['region_name'])

	n.write("\t".join(lineSplit[0:41]) + "\t" + country + "\t" + region + "\t" + "\t".join(lineSplit[43:]) + "\n")

# read file path and name from command line
inputpath = sys.argv[1]
inputfile = sys.argv[2]
outputpath = sys.argv[3]
outputfile = sys.argv[4]
geodata = sys.argv[5]

# open read and write files
f = open(inputpath + '/' + inputfile + '.log', 'r', encoding='latin-1')
n = open(outputpath + '/' + outputfile + '.log', 'w', encoding='latin-1')

# Read gi data and regions list from external files
gi = GeoIP.open(geodata,GeoIP.GEOIP_STANDARD)

# cycle through lines, omitting those that don't match the relevant criteria
for line in f:
	formatLine1(line)







	
