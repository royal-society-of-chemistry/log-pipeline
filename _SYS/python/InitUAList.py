import re
import sys
import csv
import pickle

csvpath = sys.argv[1]
picklepath = sys.argv[2]
datapath = sys.argv[3]
inputfile = sys.argv[4]

ua_str = []
ua_data = []

with open(datapath + '/' + inputfile, newline='') as csvfile:
	rawua = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in rawua:
		ua_str.append(row[0])
		entry = []
		entry.append('Bot/Crawler')
		entry.append('X')
		entry.append('X')
		entry.append('X')
		ua_data.append(entry)

with open(picklepath + '/ua_str.pickle', 'wb') as f:
	pickle.dump(ua_str, f, pickle.HIGHEST_PROTOCOL)
with open(picklepath + '/ua_data.pickle', 'wb') as g:
	pickle.dump(ua_data, g, pickle.HIGHEST_PROTOCOL)


