import re
import sys

# Regex patterns
p1 = re.compile('ASP\.NET_SessionId=([A-Za-z0-9]*);')
p2 = re.compile('AuthSystemSessionId=([-A-Za-z0-9]*);')
p3 = re.compile('_ga=[A-Za-z0-9]+\.[A-Za-z0-9]+\.([A-Za-z0-9]+)\.[A-Za-z0-9]+;')
p4 = re.compile('_utma=[A-Za-z0-9]+\.([A-Za-z0-9]+)\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+;')

# Functions
def formatLine1(line):   # determine if log file text string is right length, has correct characteristics
	"""Check line against requirements"""

	# Session IDs
	lineSplit=line.rstrip("\n").split("\t")
	asp_sess_id = "-"
	auth_sess_id = "-"
	un_sess_id = "-"
	user_id = "-"
	m1 = p1.search(lineSplit[13])
	m2 = p2.search(lineSplit[13])
	m3 = p3.search(lineSplit[13])
	m4 = p4.search(lineSplit[13])
	if m2:
		auth_sess_id = str(m2.group(1))
		un_sess_id = str(m2.group(1))
	if m1:
		asp_sess_id = str(m1.group(1))
		un_sess_id = str(m1.group(1))
	if m4:
		user_id = str(m4.group(1))
	if m3:
		user_id = str(m3.group(1))

	n.write("\t".join(lineSplit[0:23]) + "\t" + un_sess_id + "\t" + asp_sess_id + "\t" + auth_sess_id + "\t" + user_id + "\t" + "\t".join(lineSplit[27:]) + "\n")

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







	
