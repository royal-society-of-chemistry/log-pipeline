import re
import sys

NumCol = 47

# read file path and name from command line
inputpath = sys.argv[1]
inputfile = sys.argv[2]
outputpath = sys.argv[3]
outputfile = sys.argv[4]

# IP addresses to exclude
ip = []
ip.append('192\.168\.[0-9]{1,3}\.[0-9]{1,3}')

# URL elements to exclude
url = []
url.append('-')	

# unwanted requests by file extensions
ext = []
ext.append('css')
ext.append('ico')
ext.append('js')
ext.append('png')
ext.append('jpg')
ext.append('gif')
ext.append('ttf')

# Regex patterns
p1 = re.compile('^(' + "|".join(url) + ')$')
p2 = re.compile('^.*\.(' + "|".join(ext) + ')$')
p3 = re.compile('^(' + "|".join(ip) + ')$')

# Functions
def checkLine1(line):   # determine if log file text string is right length, has correct characteristics
	"""Check line against requirements"""
	lineSplit=line.split("\t")
	if (len(lineSplit)!=NumCol):
		return False
	if p1.search(lineSplit[6].lower()):
		return False
	if p2.search(lineSplit[6].lower()):
		return False
	if p3.search(lineSplit[10]):
		return False
	return True

# open read and write files
f = open(inputpath + '/' + inputfile + '.log', 'r', encoding='latin-1')
n = open(outputpath + '/' + outputfile + '.log', 'w', encoding='latin-1')

# cycle through lines, omitting those that don't match the relevant criteria
for line in f:
	if checkLine1(line):
		n.write(line)
