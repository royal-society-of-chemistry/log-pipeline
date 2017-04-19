import re
import sys

# Functions
def checkLine1(line):   # determine if log file text string is right length
	"""Check line against requirements"""
	lineSplit=line.rstrip("\n").split(" ")
	if (len(lineSplit)!=23):
		return False
	if (line.startswith("#")):
		return False
	return True		

# read file path and name from command line
inputpath = sys.argv[1]
inputfile = sys.argv[2]
outputpath = sys.argv[3]
outputfile = sys.argv[4]

# open read and write files
f = open(inputpath + '/' + inputfile + '.log', 'r', encoding='latin-1')
n = open(outputpath + '/' + outputfile + '.log', 'w', encoding='latin-1')

# cycle through lines
for line in f:
	if checkLine1(line):
		n.write( "\t".join( line.rstrip("\n").split(" ") ) + "\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\n" )
