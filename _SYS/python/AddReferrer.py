import re
import sys

# Regex patterns
p1 = re.compile('https?://([^/]+)/')
p2 = re.compile('pubs.rsc.org')
p3 = re.compile('pubs.rsc.org.')
p4 = re.compile('google.')
p5 = re.compile('scholar.google')

# Functions
def formatLine1(line):   # determine if log file text string is right length, has correct characteristics
	"""Check line against requirements"""

	# Referrer details
	lineSplit=line.rstrip("\n").split("\t")
	ref_dom = "-"
	pubs_src = "false"
	pubs_proxy = "false"
	google_src = "false"
	google_scholar = "false"
	source = "-"
	m1 = p1.search(lineSplit[14])
	if m1:
		ref_dom = str(m1.group(1))
		source = str(m1.group(1))
	m2 = p2.search(ref_dom)
	m3 = p3.search(ref_dom)
	m4 = p4.search(ref_dom)
	m5 = p5.search(ref_dom)
	if m2:
		pubs_src = "true"
		source = "pubs.rsc.org"
	if m3:
		pubs_src = "true"
		pubs_proxy = "true"
	if m5:
		google_scholar = "true"
		source = "Google Scholar"
	elif m4:
		google_src = "true"
		source = "Google"

	n.write("\t".join(lineSplit[0:27]) + "\t" + ref_dom + "\t" + pubs_src + "\t" + pubs_proxy + "\t" + google_src + "\t" + google_scholar + "\t" + source + "\t" + "\t".join(lineSplit[33:]) + "\n")

# read file path and name from command line
inputpath = sys.argv[1]
inputfile = sys.argv[2]
outputpath = sys.argv[3]
outputfile = sys.argv[4]

# open read and write files
f = open(inputpath + '/' + inputfile + '.log', 'r', encoding='latin-1')
n = open(outputpath + '/' + outputfile + '.log', 'w', encoding='latin-1')

# cycle through lines, omitting those that don't match the relevant criteria
for line in f:
	formatLine1(line)







	
