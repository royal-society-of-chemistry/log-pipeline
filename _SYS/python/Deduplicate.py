import sys
from datetime import datetime
from datetime import timedelta

#Functions

#returns false if the session has been seen within the last "deltaToUse" minutes
#the timestamp is updated at every check, so that all repeats are removed (e.g. if someone hammers at (10,20,30,40,50 ,60) minutes then they are all removed except the first...
def isDuplicateItem(duplicateItem,newTime,duplicateItemTable,deltaToUse):

	if (duplicateItem not in duplicateItemTable):
		duplicateItemTable[duplicateItem] = newTime
		return False

	lastTime = duplicateItemTable[duplicateItem]

	diffTime = newTime-lastTime
	diffInMins = diffTime / timedelta(minutes=1)
	duplicateItemTable[duplicateItem] = lastTime
	if (diffInMins<deltaToUse):
		return True

	return False

# read file path and name from command line
inputpath = sys.argv[1]
inputfile = sys.argv[2]
outputpath = sys.argv[3]
outputfile = sys.argv[4]

# open read and write files
f = open(inputpath + '/' + inputfile + '.log', 'r', encoding='latin-1')
n = open(outputpath + '/' + outputfile + '.log', 'w', encoding="latin-1")

duplicateItemTable={}

for line in f:

	lineSplit = line.rstrip("\n").split("\t")
	duplicateItem = lineSplit[23] + "_" + lineSplit[10] + "_" + lineSplit[6]
	newTime = datetime.strptime(lineSplit[0]+" "+lineSplit[1],"%Y-%m-%d %H:%M:%S")

	if ( lineSplit[40] != "-" ):
		if ( isDuplicateItem( duplicateItem,newTime,duplicateItemTable,150 ) ):
			deDup = "1"
		else:
			deDup = "0"
	else:
		deDup = "-"

	lineNew = "\t".join(lineSplit[0:46]) + "\t" + deDup
	n.write(lineNew + "\n")

n.close()
