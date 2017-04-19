import re
import sys
import csv
import pickle
import marisa_trie

def makeRangeRegex(string):
	"""Makes compiled python regex for browscap UA strings"""
	string = re.sub(r'\\',r'\\\\',string)
	string = re.sub('\.','\.',string)
	string = re.sub('\?','.',string)
	string = re.sub('\*','.*',string)
	string = re.sub('\$','\$',string)
	string = re.sub('\[','\[',string)
	string = re.sub('\]','\]',string)
	string = re.sub('\|','\|',string)
	string = re.sub('\(','\(',string)
	string = re.sub('\)','\)',string)
	string = re.sub('\+','\+',string)
	string = re.sub('\{','\{',string)
	string = re.sub('\}','\}',string)
	string = re.sub('\%','\%',string)
	string = re.sub(' ','\+',string)
	return re.compile('^' + string + '$')

def makeTriePrefix(string):

# This function returns a value for the prefix that will be used as the TRIE key for 
# each regex in the BrowsCap list.  

	prefix = []

	orig = string

	# Mozilla
	p1 = re.compile('^Mozilla/(\d)\.')
	p2 = re.compile('^([A-Za-z0-9])')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		prefix.append('MOZ' + m1.group(1) + 'X')
	elif re.search('^Mozilla',string):
		prefix.append('MOZ##')
	elif m2:
		prefix.append(m2.group(1) + m2.group(1) + m2.group(1) + '##')
	else:
		prefix.append('#####')

	# Windows

	p1 = re.compile('Windows NT (\d\d)\.(\d)')
	p2 = re.compile('Windows NT (\d\d)\.')
	p3 = re.compile('Windows NT (\d)\.(\d)')
	p4 = re.compile('Windows NT (\d)\.')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('WNT' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('WNT' + m2.group(1) + '#')
	elif m3:
		prefix.append('WNT0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('WNT0' + m4.group(1) + '#')
	elif re.search('Windows NT',string):
		prefix.append('WNT###')
	elif re.search('Windows XP',string):
		prefix.append('WIN0XP')
	elif re.search('Windows ME',string):
		prefix.append('WIN0ME')
	elif re.search('Windows 2000',string):
		prefix.append('WIN02K')
	elif re.search('Windows 98',string):
		prefix.append('WIN098')
	elif re.search('Windows 95',string):
		prefix.append('WIN095')
	elif re.search('Windows',string):
		prefix.append('WIN###')
	else:
		prefix.append('######')

	# Android

	p1 = re.compile('Android\?(\d\d)\.(\d)')
	p2 = re.compile('Android\?(\d\d)')
	p3 = re.compile('Android\?(\d)\.(\d)')
	p4 = re.compile('Android\?(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('AND' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('AND' + m2.group(1) + '#')
	elif m3:
		prefix.append('AND0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('AND0' + m4.group(1) + '#')
	elif re.search('Android',string):
		prefix.append('AND###')
	else:
		prefix.append('######')

	# Mac OS X
	
	p1 = re.compile('Mac OS X (\d\d)\?(\d)')
	p2 = re.compile('Mac OS X (\d\d)')
	p3 = re.compile('Mac OS X (\d)\?(\d)')
	p4 = re.compile('Mac OS X (\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('MCX' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('MCX' + m2.group(1) + '#')
	elif m3:
		prefix.append('MCX0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('MCX0' + m4.group(1) + '#')
	elif re.search('Mac OS X',string):
		prefix.append('MCX###')
	else:
		prefix.append('######')

	# iPhone OS
	
	p1 = re.compile('iPhone OS (\d\d)\?')
	p2 = re.compile('iPhone OS (\d)\?')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		prefix.append('IOS' + m1.group(1) + '#')
	elif m2:
		prefix.append('IOS0' + m2.group(1) + '#')
	elif re.search('iPhone OS',string):
		prefix.append('IOS###')
	else:
		prefix.append('######')

	# CriOS
	
	p1 = re.compile('CriOS/(\d\d)')
	m1 = p1.search(string)
	if m1:
		prefix.append('COS' + m1.group(1) + '#')
	elif re.search('CriOS',string):
		prefix.append('COS###')
	else:
		prefix.append('######')

	# OPiOS
	
	p1 = re.compile('OPiOS/(\d\d)\.(\d)')
	p2 = re.compile('OPiOS/(\d\d)')
	p3 = re.compile('OPiOS/(\d)\.(\d)')
	p4 = re.compile('OPiOS/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('OOS' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('OOS' + m2.group(1) + '#')
	elif m3:
		prefix.append('OOS0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('OOS0' + m4.group(1) + '#')
	elif re.search('OPiOS',string):
		prefix.append('OOS###')
	else:
		prefix.append('######')

	# CPU OS
	
	p1 = re.compile('CPU OS (\d)\?(\d)')
	p2 = re.compile('CPU OS (\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		prefix.append('CPU0' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('CPU0' + m2.group(1) + '#')
	elif re.search('CPU OS',string):
		prefix.append('CPU###')
	else:
		prefix.append('######')

	# MSIE
	
	p1 = re.compile('MSIE (\d\d)\.')
	p2 = re.compile('MSIE (\d)\.')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		prefix.append('MIE' + m1.group(1) + '#')
	elif m2:
		prefix.append('MIE0' + m2.group(1) + '#')
	elif re.search('MSIE',string):
		prefix.append('MIE###')
	else:
		prefix.append('######')

	# Trident

	p1 = re.compile('Trident/(\d)\.')
	m1 = p1.search(string)
	if m1:
		prefix.append('TDT' + m1.group(1) + '#')
	elif re.search('Trident',string):
		prefix.append('TDT##')
	else:
		prefix.append('#####')

	# Chrome

	p1 = re.compile('Chrome/(\d\d)')
	p2 = re.compile('Chrome/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		prefix.append('CHR0' + m1.group(1))
	elif m2:
		prefix.append('CHR00' + m2.group(1))
	elif re.search('Chrome',string):
		prefix.append('CHR###')
	else:
		prefix.append('######')

	# Chromium

	p1 = re.compile('Chromium/(\d\d)')
	p2 = re.compile('Chromium/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		prefix.append('CRM0' + m1.group(1))
	elif m2:
		prefix.append('CRM00' + m2.group(1))
	elif re.search('Chromium',string):
		prefix.append('CRM###')
	else:
		prefix.append('######')

	# Firefox

	p1 = re.compile('Firefox/(\d\d)\.(\d)')
	p2 = re.compile('Firefox/(\d\d)')
	p3 = re.compile('Firefox/(\d)\.(\d)')
	p4 = re.compile('Firefox/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('FFX' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('FFX' + m2.group(1) + '#')
	elif m3:
		prefix.append('FFX0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('FFX0' + m4.group(1) + '#')
	elif re.search('Firefox',string):
		prefix.append('FFX###')
	else:
		prefix.append('######')

	# Opera

	p1 = re.compile('Opera.(\d\d)\.(\d)')
	p2 = re.compile('Opera.(\d\d)')
	p3 = re.compile('Opera.(\d)\.(\d)')
	p4 = re.compile('Opera.(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('OPR' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('OPR' + m2.group(1) + '#')
	elif m3:
		prefix.append('OPR0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('OPR0' + m4.group(1) + '#')
	elif re.search('Opera',string):
		prefix.append('OPR###')
	else:
		prefix.append('######')

	# OPR

	p1 = re.compile('OPR/(\d\d)')
	p2 = re.compile('OPR/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		prefix.append('OPX0' + m1.group(1))
	elif m2:
		prefix.append('OPX00' + m2.group(1))
	elif re.search('OPR',string):
		prefix.append('OPX###')
	else:
		prefix.append('######')

	# Thunderbird

	p1 = re.compile('Thunderbird/(\d\d)\.(\d)')
	p2 = re.compile('Thunderbird/(\d\d)')
	p3 = re.compile('Thunderbird/(\d)\.(\d)')
	p4 = re.compile('Thunderbird/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('THB' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('THB' + m2.group(1) + '#')
	elif m3:
		prefix.append('THB0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('THB0' + m4.group(1) + '#')
	elif re.search('Thunderbird',string):
		prefix.append('THB###')
	else:
		prefix.append('######')

	# SeaMonkey

	p1 = re.compile('SeaMonkey/(\d)\.(\d\d)')
	p2 = re.compile('SeaMonkey/(\d)\.(\d)')
	p3 = re.compile('SeaMonkey/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	if m1:
		prefix.append('SMK' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('SMK' + m2.group(1) + m2.group(2) + '#')
	elif m3:
		prefix.append('SMK' + m3.group(1) + '##')
	elif re.search('SeaMonkey',string):
		prefix.append('SMK###')
	else:
		prefix.append('######')

	# Lunascape

	p1 = re.compile('Lunascape/(\d)\.(\d\d)')
	p2 = re.compile('Lunascape/(\d)\.(\d)')
	p3 = re.compile('Lunascape/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	if m1:
		prefix.append('LSC' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('LSC' + m2.group(1) + m2.group(2) + '#')
	elif m3:
		prefix.append('LSC' + m3.group(1) + '##')
	elif re.search('Lunascape',string):
		prefix.append('LSC###')
	else:
		prefix.append('######')

	# PaleMoon

	p1 = re.compile('PaleMoon/(\d\d)\.(\d)')
	p2 = re.compile('PaleMoon/(\d\d)')
	p3 = re.compile('PaleMoon/(\d)\.(\d)')
	p4 = re.compile('PaleMoon/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('PMN' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('PMN' + m2.group(1) + '#')
	elif m3:
		prefix.append('PMN0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('PMN0' + m4.group(1) + '#')
	elif re.search('PaleMoon',string):
		prefix.append('PMN###')
	else:
		prefix.append('######')

	# Silk

	p1 = re.compile('Silk/(\d)\.(\d\d)')
	p2 = re.compile('Silk/(\d)\.(\d)')
	p3 = re.compile('Silk/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	if m1:
		prefix.append('SLK' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('SLK' + m2.group(1) + m2.group(2) + '#')
	elif m3:
		prefix.append('SLK' + m3.group(1) + '##')
	elif re.search('Silk',string):
		prefix.append('SLK###')
	else:
		prefix.append('######')

	# Iron

	p1 = re.compile('Iron/(\d\d)\.(\d)')
	p2 = re.compile('Iron/(\d\d)')
	p3 = re.compile('Iron/(\d)\.(\d)')
	p4 = re.compile('Iron/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('IRN' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('IRN' + m2.group(1) + '#')
	elif m3:
		prefix.append('IRN0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('IRN0' + m4.group(1) + '#')
	elif re.search('Iron',string):
		prefix.append('IRN###')
	else:
		prefix.append('######')

	# UCBrowser
	
	p1 = re.compile('UCBrowser/(\d\d)\.(\d)')
	p2 = re.compile('UCBrowser/(\d\d)')
	p3 = re.compile('UCBrowser/(\d)\.(\d)')
	p4 = re.compile('UCBrowser/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('UCB' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('UCB' + m2.group(1) + '#')
	elif m3:
		prefix.append('UCB0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('UCB0' + m4.group(1) + '#')
	elif re.search('UCBrowser',string):
		prefix.append('UCB###')
	else:
		prefix.append('######')

	# UP.Browser
	
	p1 = re.compile('UP\.Browser/(\d)\.(\d)')
	m1 = p1.search(string)
	if m1:
		prefix.append('UPB0' + m1.group(1) + m1.group(2))
	elif re.search('UP\.Browser',string):
		prefix.append('UPB###')
	else:
		prefix.append('######')

	# YaBrowser
	
	p1 = re.compile('YaBrowser/(\d\d)\.(\d)')
	p2 = re.compile('YaBrowser/(\d\d)')
	p3 = re.compile('YaBrowser/(\d)\.(\d)')
	p4 = re.compile('YaBrowser/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('YAB' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('YAB' + m2.group(1) + '#')
	elif m3:
		prefix.append('YAB0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('YAB0' + m4.group(1) + '#')
	elif re.search('YaBrowser',string):
		prefix.append('YAB###')
	else:
		prefix.append('######')

	# CFNetwork

	p1 = re.compile('CFNetwork/(\d\d\d)\.(\d)\.')
	p2 = re.compile('CFNetwork/(\d\d\d)\.')
	p3 = re.compile('CFNetwork/(\d\d)\.(\d)\.')
	p4 = re.compile('CFNetwork/(\d\d)\.')
	p5 = re.compile('CFNetwork/(\d)\.(\d)\.')
	p6 = re.compile('CFNetwork/(\d)\.')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	m5 = p5.search(string)
	m6 = p6.search(string)
	if m1:
		prefix.append('CFN' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('CFN' + m2.group(1) + '#')
	elif m3:
		prefix.append('CFN0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('CFN0' + m4.group(1) + '#')
	elif m5:
		prefix.append('CFN00' + m5.group(1) + m5.group(2))
	elif m6:
		prefix.append('CFN00' + m6.group(1) + '#')
	elif re.search('CFNetwork',string):
		prefix.append('CFN####')
	else:
		prefix.append('#######')

	# Version

	p1 = re.compile('Version/(\d\d)\.(\d)')
	p2 = re.compile('Version/(\d\d)')
	p3 = re.compile('Version/(\d)\.(\d)')
	p4 = re.compile('Version/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		prefix.append('VER' + m1.group(1) + m1.group(2))
	elif m2:
		prefix.append('VER' + m2.group(1) + '#')
	elif m3:
		prefix.append('VER0' + m3.group(1) + m3.group(2))
	elif m4:
		prefix.append('VER0' + m4.group(1) + '#')
	elif re.search('Version',string):
		prefix.append('VER###')
	else:
		prefix.append('######')

	# HTC	

	if re.search('HTC',string):
		prefix.append('Ht')
	else:
		prefix.append('##')

	# Samsung	

	if re.search('SAMSUNG',string):
		prefix.append('Ss')
	elif re.search('[Ss]amsung',string):
		prefix.append('Ss')
	elif re.search('GT-[A-Z]\d{4}',string):
		prefix.append('Ss')
	elif re.search('SM-[A-Z]\d{3}',string):
		prefix.append('Ss')
	elif re.search('SGH-[A-Z]\d{3}',string):
		prefix.append('Ss')
	elif re.search('Tizen',string):
		prefix.append('Ss')
	else:
		prefix.append('##')

	# Asus	

	if re.search('ASUS',string):
		prefix.append('As')
	elif re.search('[Aa]sus',string):
		prefix.append('As')
	elif re.search('TF\d{3}',string):
		prefix.append('Mr')
	else:
		prefix.append('##')

	# Motorola	

	if re.search('XT\d{3,4}',string):
		prefix.append('Mr')
	elif re.search('MZ6\d{2}',string):
		prefix.append('Mr')
	elif re.search('XOOM',string):
		prefix.append('Mr')
	else:
		prefix.append('##')

	# LG	

	if re.search('LG-[A-Z]\d{3}',string):
		prefix.append('Lg')
	else:
		prefix.append('##')

	# SonyEricsson	

	if re.search('SonyEricsson',string):
		prefix.append('Se')
	elif re.search('ST\d{2}i',string):
		prefix.append('Se')
	else:
		prefix.append('##')

	# Lenovo	

	if re.search('Lenovo',string):
		prefix.append('Lv')
	else:
		prefix.append('##')

	# HUAWEI	

	if re.search('HUAWEI',string):
		prefix.append('Hw')
	elif re.search('[Hh]uawei',string):
		prefix.append('Hw')
	else:
		prefix.append('##')

	# Nexus	

	if re.search('NEXUS',string):
		prefix.append('Nx')
	elif re.search('[Nn]exus',string):
		prefix.append('Nx')
	else:
		prefix.append('##')

	# BlackBerry	

	if re.search('BlackBerry',string):
		prefix.append('Bb')
	else:
		prefix.append('##')

	string = '@' + ''.join(prefix) + '_' + re.sub(' ','+',re.split(r'(\*|\?)',orig)[0])
	return string

def makeTrieValue(a):
	return (a,)


# read file path and name from command line
datapath = sys.argv[1]
csvpath = sys.argv[2]
picklepath = sys.argv[3]

ver = 'XXXX'
browscap_data = []
trie_keys = []
trie_values = []
	
with open(csvpath + '/' + 'browscap.csv', newline='') as csvfile:
	rawbrowscap = csv.reader(csvfile, delimiter=',', quotechar='"')
	flag = 'header'
	for row in rawbrowscap:

		# First element in row is 'GJK_Browscap_Version', therefore next row holds the version number
		if row[0] == 'GJK_Browscap_Version':
			flag = 'version'

		# If flag is version, take version number. Next row is a header row
		elif flag == 'version':
			ver = str(row[0])
			flag = 'header'

		# If first element is 'PropertyName', next row is a header row
		elif row[0] == 'PropertyName':
			flag = 'header'

		# If first element is 'DefaultProperties', next row is a first body row
		elif row[0] == 'DefaultProperties':
			flag = 'body'

		# if flag is 'body', start collecting data
		elif flag == 'body':
			entry = []

			# first member of data file: the regex
			entry.append(makeRangeRegex(row[0]))

			# subsequent members of data file: browscap row members detailing relevant data for a given regex
			for field in row:
				entry.append(field)

			# add colection to data array
			browscap_data.append(entry)

			# make trie prefix (key) for trie file
			trie_keys.append(makeTriePrefix(row[0]))

			# add trie index triple for trie file
			trie_values.append(makeTrieValue(len(trie_keys) - 1))


browscap_trie = marisa_trie.RecordTrie("<Q", zip(trie_keys,trie_values))

with open(picklepath + '/' + 'browscap_data_' + ver + '.pickle', 'wb') as f:
	pickle.dump(browscap_data, f, pickle.HIGHEST_PROTOCOL)
with open(picklepath + '/' + 'browscap_trie_' + ver + '.pickle', 'wb') as g:
	pickle.dump(browscap_trie, g, pickle.HIGHEST_PROTOCOL)

