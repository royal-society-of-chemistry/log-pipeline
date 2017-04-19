import re
import sys
import pickle
import marisa_trie
import itertools

NumCol = 47

# unwanted user agent elements
ua = []
ua.append('AddThis')
ua.append('EPiServer\+LinkValidator')
ua.append('LOCKSS\+cache')
ua.append('PRTG\+Network\+Monitor')
ua.append('Sogou\+web\+spider')
ua.append('Sparrho')
ua.append('Springshare\+Link\+Checker')
ua.append('WatchMouse')
ua.append('[Bb][Oo][Tt]\\b')

x1 = re.compile('(' + "|".join(ua) + ')')

# Functions
def makeTriePatterns(string):   # process user agent string into trie patterns from log file


# This function takes a user agent string and generates an array of arrays of possible prefix elements, based on looking for 
# certain common "sub-regexes" which are in turn associated with certain prefixes. 
# 
# For example:
# 
# 	sub-regex	prefix	
# 
# 	^Mozilla/5*	MOZ5#
# 	^Mozilla/4*	MOZ4#
# 	^Mozilla/3*	MOZ3#
# 	^Mozilla*	MOZ##
# 	^*		#####
# 
# If the UA string being checked starts with "Mozilla/5..." then it only needs to be compared with 
# the dictionary regexes that have prefixes MOZ5#, MOZ##, and #####; dictionary entries assigned to the MOZ4# 
# and MOZ3# prefixes can be skipped without running a comparison. This division can be done quickly with TRIES 
# technology.
# 
# If the process is repeated for other sets of common sub-regexes, we will generate sets of possible prefix elements:
# 
# [[MOZ5#,MOZ##,#####][WNT91,WNT9#,WNT##,#####][AND101,AND10#,AND###,######]... ] <----||| THIS IS THE ARRAY OF ARRAYS THAT THE FUNCTION RETURNS
# 
# If we collapse this matrix to a list we would get 3x4x4x.... possible prefix strings:
# 
# MOZ5#WNT91AND101...
# MOZ##WNT91AND101...
# MOZ##WNT91AND101...
# #####WNT91AND101...
# 
# MOZ5#WNT9#AND101...
# MOZ##WNT9#AND101...
# MOZ##WNT9#AND101...
# #####WNT9#AND101...
# 
# MOZ5#WNT##AND101...
# MOZ##WNT##AND101...
# MOZ##WNT##AND101...
# #####WNT##AND101...
# 
# MOZ5######AND101...
# MOZ#######AND101...
# MOZ#######AND101...
# ##########AND101... etc.
# 
# While this looks like a lot of prefixes to check, it is still a very small subset of all the possible BrowsCap 
# regex entries, and the TRIES functionality makes the lookups very quick.
# 
# (The orignal dictionary regexes will already have been given a single prefix based on these groups of patterns; each 
# would be assigned the ones that most uniquely matches the regex.)
# 
# In reality, the first part that deals with the "Mozilla" prefix is a special case - not only is it at the beginning of
# the UA string, the code includes a section for isolating the first alphanumeric of the UA string and making a prefix 
# from that. It  turns out that UA strings that DO NOT start with "Mozilla" aren't "unique" enough, giving a possible set 
# of potential regexes from the dictionary that isn't focussed enough, slowing down the filter considerably. Dividing them 
# into alphabetically-defined sub-groups was sufficient to increase speed again.
# 
# Identification of sub-regex phrases continued until the speed of the filtration in practice plateaued, and the time it 
# took to load the TRIES pickle file became the rate limiting step in the filter.

	trie_str = []
	patterns = []

	# Mozilla
	moz_str = []
	p1 = re.compile('^Mozilla/(\d)\.')
	p2 = re.compile('^([A-Za-z0-9])')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		moz_str.append('MOZ' + m1.group(1) + 'X')
	if re.search('^Mozilla',string):
		moz_str.append('MOZ##')
	if m2:
		moz_str.append(m2.group(1) + m2.group(1) + m2.group(1) + '##')
	moz_str.append('#####')
	trie_str.append(moz_str)

	# Windows
	win_str = []
	p1 = re.compile('Windows NT (\d\d)\.(\d)')
	p2 = re.compile('Windows NT (\d\d)\.')
	p3 = re.compile('Windows NT (\d)\.(\d)')
	p4 = re.compile('Windows NT (\d)\.')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		win_str.append('WNT' + m1.group(1) + m1.group(2))
	if m2:
		win_str.append('WNT' + m2.group(1) + '#')
	if m3:
		win_str.append('WNT0' + m3.group(1) + m3.group(2))
	if m4:
		win_str.append('WNT0' + m4.group(1) + '#')
	if re.search('Windows NT',string):
		win_str.append('WNT###')
	if re.search('Windows XP',string):
		win_str.append('WIN0XP')
	if re.search('Windows ME',string):
		win_str.append('WIN0ME')
	if re.search('Windows 2000',string):
		win_str.append('WIN02K')
	if re.search('Windows 98',string):
		win_str.append('WIN098')
	if re.search('Windows 95',string):
		win_str.append('WIN095')
	if re.search('Windows',string):
		win_str.append('WIN###')
	win_str.append('######')
	trie_str.append(win_str)

	# Android
	and_str = []
	p1 = re.compile('Android.?(\d\d)\.(\d)')
	p2 = re.compile('Android.?(\d\d)')
	p3 = re.compile('Android.?(\d)\.(\d)')
	p4 = re.compile('Android.?(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		and_str.append('AND' + m1.group(1) + m1.group(2))
	if m2:
		and_str.append('AND' + m2.group(1) + '#')
	if m3:
		and_str.append('AND0' + m3.group(1) + m3.group(2))
	if m4:
		and_str.append('AND0' + m4.group(1) + '#')
	if re.search('Android',string):
		and_str.append('AND###')
	and_str.append('######')
	trie_str.append(and_str)

	# Mac OS X
	mac_str = []
	p1 = re.compile('Mac OS X (\d\d).?(\d)')
	p2 = re.compile('Mac OS X (\d\d)')
	p3 = re.compile('Mac OS X (\d).?(\d)')
	p4 = re.compile('Mac OS X (\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		mac_str.append('MCX' + m1.group(1) + m1.group(2))
	if m2:
		mac_str.append('MCX' + m2.group(1) + '#')
	if m3:
		mac_str.append('MCX0' + m3.group(1) + m3.group(2))
	if m4:
		mac_str.append('MCX0' + m4.group(1) + '#')
	if re.search('Mac OS X',string):
		mac_str.append('MCX###')
	mac_str.append('######')
	trie_str.append(mac_str)


	# iPhone OS
	iph_str = []
	p1 = re.compile('iPhone OS (\d\d).?')
	p2 = re.compile('iPhone OS (\d).?')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		iph_str.append('IOS' + m1.group(1) + '#')
	if m2:
		iph_str.append('IOS0' + m2.group(1) + '#')
	if re.search('iPhone OS',string):
		iph_str.append('IOS###')
	iph_str.append('######')
	trie_str.append(iph_str)

	# CriOS
	cos_str = []
	p1 = re.compile('CriOS/(\d\d)')
	m1 = p1.search(string)
	if m1:
		cos_str.append('COS' + m1.group(1) + '#')
	if re.search('CriOS',string):
		cos_str.append('COS###')
	cos_str.append('######')
	trie_str.append(cos_str)

	# OPiOS
	oos_str = []
	p1 = re.compile('OPiOS/(\d\d)\.(\d)')
	p2 = re.compile('OPiOS/(\d\d)')
	p3 = re.compile('OPiOS/(\d)\.(\d)')
	p4 = re.compile('OPiOS/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		oos_str.append('OOS' + m1.group(1) + m1.group(2))
	if m2:
		oos_str.append('OOS' + m2.group(1) + '#')
	if m3:
		oos_str.append('OOS0' + m3.group(1) + m3.group(2))
	if m4:
		oos_str.append('OOS0' + m4.group(1) + '#')
	if re.search('OPiOS',string):
		oos_str.append('OOS###')
	oos_str.append('######')
	trie_str.append(oos_str)

	# CPU OS
	cpu_str = []
	p1 = re.compile('CPU OS (\d)\?(\d)')
	p2 = re.compile('CPU OS (\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		cpu_str.append('CPU0' + m1.group(1) + m1.group(2))
	if m2:
		cpu_str.append('CPU0' + m2.group(1) + '#')
	if re.search('CPU OS',string):
		cpu_str.append('CPU###')
	cpu_str.append('######')
	trie_str.append(cpu_str)

	# MSIE
	mie_str = []
	p1 = re.compile('MSIE (\d\d)\.')
	p2 = re.compile('MSIE (\d)\.')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		mie_str.append('MIE' + m1.group(1) + '#')
	if m2:
		mie_str.append('MIE0' + m2.group(1) + '#')
	if re.search('MSIE',string):
		mie_str.append('MIE###')
	mie_str.append('######')
	trie_str.append(mie_str)

	# Trident
	trd_str = []
	p1 = re.compile('Trident/(\d)\.')
	m1 = p1.search(string)
	if m1:
		trd_str.append('TDT' + m1.group(1) + '#')
	if re.search('Trident',string):
		trd_str.append('TDT##')
	trd_str.append('#####')
	trie_str.append(trd_str)

	# Chrome
	chr_str = []
	p1 = re.compile('Chrome/(\d\d)')
	p2 = re.compile('Chrome/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		chr_str.append('CHR0' + m1.group(1))
	if m2:
		chr_str.append('CHR00' + m2.group(1))
	if re.search('Chrome',string):
		chr_str.append('CHR###')
	chr_str.append('######')
	trie_str.append(chr_str)

	# Chromium
	crm_str = []
	p1 = re.compile('Chromium/(\d\d)')
	p2 = re.compile('Chromium/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		crm_str.append('CRM0' + m1.group(1))
	if m2:
		crm_str.append('CRM00' + m2.group(1))
	if re.search('Chromium',string):
		crm_str.append('CRM###')
	crm_str.append('######')
	trie_str.append(crm_str)

	# Firefox
	ffx_str = []	
	p1 = re.compile('Firefox/(\d\d)\.(\d)')
	p2 = re.compile('Firefox/(\d\d)')
	p3 = re.compile('Firefox/(\d)\.(\d)')
	p4 = re.compile('Firefox/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		ffx_str.append('FFX' + m1.group(1) + m1.group(2))
	if m2:
		ffx_str.append('FFX' + m2.group(1) + '#')
	if m3:
		ffx_str.append('FFX0' + m3.group(1) + m3.group(2))
	if m4:
		ffx_str.append('FFX0' + m4.group(1) + '#')
	if re.search('Firefox',string):
		ffx_str.append('FFX###')
	ffx_str.append('######')
	trie_str.append(ffx_str)

	# Opera
	opr_str = []
	p1 = re.compile('Opera.(\d\d)\.(\d)')
	p2 = re.compile('Opera.(\d\d)')
	p3 = re.compile('Opera.(\d)\.(\d)')
	p4 = re.compile('Opera.(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		opr_str.append('OPR' + m1.group(1) + m1.group(2))
	if m2:
		opr_str.append('OPR' + m2.group(1) + '#')
	if m3:
		opr_str.append('OPR0' + m3.group(1) + m3.group(2))
	if m4:
		opr_str.append('OPR0' + m4.group(1) + '#')
	if re.search('Opera',string):
		opr_str.append('OPR###')
	opr_str.append('######')
	trie_str.append(opr_str)

	# OPR
	opx_str = []
	p1 = re.compile('OPR/(\d\d)')
	p2 = re.compile('OPR/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	if m1:
		opx_str.append('OPX0' + m1.group(1))
	if m2:
		opx_str.append('OPX00' + m2.group(1))
	if re.search('OPR',string):
		opx_str.append('OPX###')
	opx_str.append('######')
	trie_str.append(opx_str)

	# Thunderbird
	thb_str = []
	p1 = re.compile('Thunderbird/(\d\d)\.(\d)')
	p2 = re.compile('Thunderbird/(\d\d)')
	p3 = re.compile('Thunderbird/(\d)\.(\d)')
	p4 = re.compile('Thunderbird/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		thb_str.append('THB' + m1.group(1) + m1.group(2))
	if m2:
		thb_str.append('THB' + m2.group(1) + '#')
	if m3:
		thb_str.append('THB0' + m3.group(1) + m3.group(2))
	if m4:
		thb_str.append('THB0' + m4.group(1) + '#')
	if re.search('Thunderbird',string):
		thb_str.append('THB###')
	thb_str.append('######')
	trie_str.append(thb_str)

	# SeaMonkey
	smk_str = []
	p1 = re.compile('SeaMonkey/(\d)\.(\d\d)')
	p2 = re.compile('SeaMonkey/(\d)\.(\d)')
	p3 = re.compile('SeaMonkey/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	if m1:
		smk_str.append('SMK' + m1.group(1) + m1.group(2))
	if m2:
		smk_str.append('SMK' + m2.group(1) + m2.group(2) + '#')
	if m3:
		smk_str.append('SMK' + m3.group(1) + '##')
	if re.search('SeaMonkey',string):
		smk_str.append('SMK###')
	smk_str.append('######')
	trie_str.append(smk_str)

	# Lunascape
	lsc_str = []
	p1 = re.compile('Lunascape/(\d)\.(\d\d)')
	p2 = re.compile('Lunascape/(\d)\.(\d)')
	p3 = re.compile('Lunascape/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	if m1:
		lsc_str.append('LSC' + m1.group(1) + m1.group(2))
	if m2:
		lsc_str.append('LSC' + m2.group(1) + m2.group(2) + '#')
	if m3:
		lsc_str.append('LSC' + m3.group(1) + '##')
	if re.search('Lunascape',string):
		lsc_str.append('LSC###')
	lsc_str.append('######')
	trie_str.append(lsc_str)

	# PaleMoon
	pmn_str = []
	p1 = re.compile('PaleMoon/(\d\d)\.(\d)')
	p2 = re.compile('PaleMoon/(\d\d)')
	p3 = re.compile('PaleMoon/(\d)\.(\d)')
	p4 = re.compile('PaleMoon/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		pmn_str.append('PMN' + m1.group(1) + m1.group(2))
	if m2:
		pmn_str.append('PMN' + m2.group(1) + '#')
	if m3:
		pmn_str.append('PMN0' + m3.group(1) + m3.group(2))
	if m4:
		pmn_str.append('PMN0' + m4.group(1) + '#')
	if re.search('PaleMoon',string):
		pmn_str.append('PMN###')
	pmn_str.append('######')
	trie_str.append(pmn_str)

	# Silk
	slk_str = []
	p1 = re.compile('Silk/(\d)\.(\d\d)')
	p2 = re.compile('Silk/(\d)\.(\d)')
	p3 = re.compile('Silk/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	if m1:
		slk_str.append('SLK' + m1.group(1) + m1.group(2))
	if m2:
		slk_str.append('SLK' + m2.group(1) + m2.group(2) + '#')
	if m3:
		slk_str.append('SLK' + m3.group(1) + '##')
	if re.search('Silk',string):
		slk_str.append('SLK###')
	slk_str.append('######')
	trie_str.append(slk_str)

	# Iron
	irn_str = []
	p1 = re.compile('Iron/(\d\d)\.(\d)')
	p2 = re.compile('Iron/(\d\d)')
	p3 = re.compile('Iron/(\d)\.(\d)')
	p4 = re.compile('Iron/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		irn_str.append('IRN' + m1.group(1) + m1.group(2))
	if m2:
		irn_str.append('IRN' + m2.group(1) + '#')
	if m3:
		irn_str.append('IRN0' + m3.group(1) + m3.group(2))
	if m4:
		irn_str.append('IRN0' + m4.group(1) + '#')
	if re.search('Iron',string):
		irn_str.append('IRN###')
	irn_str.append('######')
	trie_str.append(irn_str)

	# UCBrowser
	ucb_str = []	
	p1 = re.compile('UCBrowser/(\d\d)\.(\d)')
	p2 = re.compile('UCBrowser/(\d\d)')
	p3 = re.compile('UCBrowser/(\d)\.(\d)')
	p4 = re.compile('UCBrowser/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		ucb_str.append('UCB' + m1.group(1) + m1.group(2))
	if m2:
		ucb_str.append('UCB' + m2.group(1) + '#')
	if m3:
		ucb_str.append('UCB0' + m3.group(1) + m3.group(2))
	if m4:
		ucb_str.append('UCB0' + m4.group(1) + '#')
	if re.search('UCBrowser',string):
		ucb_str.append('UCB###')
	ucb_str.append('######')
	trie_str.append(ucb_str)

	# UP.Browser
	upb_str = []	
	p1 = re.compile('UP\.Browser/(\d)\.(\d)')
	m1 = p1.search(string)
	if m1:
		upb_str.append('UPB0' + m1.group(1) + m1.group(2))
	if re.search('UP\.Browser',string):
		upb_str.append('UPB###')
	upb_str.append('######')
	trie_str.append(upb_str)

	# YaBrowser
	yab_str = []
	p1 = re.compile('YaBrowser/(\d\d)\.(\d)')
	p2 = re.compile('YaBrowser/(\d\d)')
	p3 = re.compile('YaBrowser/(\d)\.(\d)')
	p4 = re.compile('YaBrowser/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		yab_str.append('YAB' + m1.group(1) + m1.group(2))
	if m2:
		yab_str.append('YAB' + m2.group(1) + '#')
	if m3:
		yab_str.append('YAB0' + m3.group(1) + m3.group(2))
	if m4:
		yab_str.append('YAB0' + m4.group(1) + '#')
	if re.search('YaBrowser',string):
		yab_str.append('YAB###')
	yab_str.append('######')
	trie_str.append(yab_str)

	# CFNetwork
	cfn_str = []
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
		cfn_str.append('CFN' + m1.group(1) + m1.group(2))
	if m2:
		cfn_str.append('CFN' + m2.group(1) + '#')
	if m3:
		cfn_str.append('CFN0' + m3.group(1) + m3.group(2))
	if m4:
		cfn_str.append('CFN0' + m4.group(1) + '#')
	if m5:
		cfn_str.append('CFN00' + m5.group(1) + m5.group(2))
	if m6:
		cfn_str.append('CFN00' + m6.group(1) + '#')
	if re.search('CFNetwork',string):
		cfn_str.append('CFN####')
	cfn_str.append('#######')
	trie_str.append(cfn_str)

	# Version
	ver_str = []
	p1 = re.compile('Version/(\d\d)\.(\d)')
	p2 = re.compile('Version/(\d\d)')
	p3 = re.compile('Version/(\d)\.(\d)')
	p4 = re.compile('Version/(\d)')
	m1 = p1.search(string)
	m2 = p2.search(string)
	m3 = p3.search(string)
	m4 = p4.search(string)
	if m1:
		ver_str.append('VER' + m1.group(1) + m1.group(2))
	if m2:
		ver_str.append('VER' + m2.group(1) + '#')
	if m3:
		ver_str.append('VER0' + m3.group(1) + m3.group(2))
	if m4:
		ver_str.append('VER0' + m4.group(1) + '#')
	if re.search('Version',string):
		ver_str.append('VER###')
	ver_str.append('######')
	trie_str.append(ver_str)

	# HTC
	htc_str = []	
	if re.search('HTC',string):
		htc_str.append('Ht')
	htc_str.append('##')
	trie_str.append(htc_str)

	# Samsung	
	ssg_str = []	
	if re.search('SAMSUNG',string):
		ssg_str.append('Ss')
	elif re.search('[Ss]amsung',string):
		ssg_str.append('Ss')
	elif re.search('GT-[A-Z]\d{4}',string):
		ssg_str.append('Ss')
	elif re.search('SM-[A-Z]\d{3}',string):
		ssg_str.append('Ss')
	elif re.search('SGH-[A-Z]\d{3}',string):
		ssg_str.append('Ss')
	elif re.search('Tizen',string):
		ssg_str.append('Ss')
	ssg_str.append('##')
	trie_str.append(ssg_str)

	# Asus	
	ass_str = []
	if re.search('ASUS',string):
		ass_str.append('As')
	elif re.search('[Aa]sus',string):
		ass_str.append('As')
	elif re.search('TF\d{3}',string):
		ass_str.append('Mr')
	ass_str.append('##')
	trie_str.append(ass_str)

	# Motorola	
	mtr_str = []
	if re.search('XT\d{3,4}',string):
		mtr_str.append('Mr')
	elif re.search('MZ6\d{2}',string):
		mtr_str.append('Mr')
	elif re.search('XOOM',string):
		mtr_str.append('Mr')
	mtr_str.append('##')
	trie_str.append(mtr_str)

	# LG	
	lgx_str = []
	if re.search('LG-[A-Z]\d{3}',string):
		lgx_str.append('Lg')
	lgx_str.append('##')
	trie_str.append(lgx_str)

	# SonyEricsson	
	ses_str = []
	if re.search('SonyEricsson',string):
		ses_str.append('Se')
	elif re.search('ST\d{2}i',string):
		ses_str.append('Se')
	ses_str.append('##')
	trie_str.append(ses_str)

	# Lenovo	
	lnv_str = []
	if re.search('Lenovo',string):
		lnv_str.append('Lv')
	lnv_str.append('##')
	trie_str.append(lnv_str)

	# HUAWEI	
	haw_str = []
	if re.search('HUAWEI',string):
		haw_str.append('Hw')
	elif re.search('[Hh]uawei',string):
		haw_str.append('Hw')
	haw_str.append('##')
	trie_str.append(haw_str)

	# Nexus	
	nxs_str = []
	if re.search('NEXUS',string):
		nxs_str.append('Nx')
	elif re.search('[Nn]exus',string):
		nxs_str.append('Nx')
	nxs_str.append('##')
	trie_str.append(nxs_str)

	# BlackBerry	
	bby_str = []
	if re.search('BlackBerry',string):
		bby_str.append('Bb')
	bby_str.append('##')
	trie_str.append(bby_str)

	return trie_str

def formatLine1(line):   # process line from log file
	"""Process line against requirements"""
	lineSplit = line.rstrip("\n").split("\t")

	isbot = '-'
	os = '-'
	device = '-'
	browser = '-'
	writeline = True

	# Isolate user agent string from log entry	
	ua_string = lineSplit[12]

	# mark matches against list of common bots	
	if x1.search(ua_string):
		isbot = 'Bot/Crawler'

	# mark matches (previously made in this run) accordingly
	elif ua_string in ua_str:
		index = ua_str.index(ua_string)
		isbot = ua_data[index][0]
		os = ua_data[index][1]
		device = ua_data[index][2]
		browser = ua_data[index][3]

	# run new UA string against the trie/regex lists
	else:
		
		# convert "+" to space in string
		string = re.sub('\+',' ',ua_string)

		# Make "array of arrays" of possible custom prefixes
		trie_str = makeTriePatterns(string)

		# Collapse "array of arrays" into single list of [@]+[prefix]+[UAstring]" strings 
		patterns = ['@' + ''.join(x) + '_' + ua_string for x in list(itertools.product(*trie_str))]

		subcoll = []

		# For each prefix+UAstring combo, get matching keys from trie/regex dictionary (reversed so most specific is first) and append the associated integer index value to the temporary collection
		# This essentially collects the line numbers of the regex dictionary entries that are potential matches for the UA in question
		for pattern in patterns:
			for m in reversed(bc_trie.prefixes(u'' + pattern)):
				for n in bc_trie[m]:
					subcoll.append(int(n[0]))

		# Sort the indexes for the trie/regex dictionary previously found into ascending order, so that they are compared to the UAstring in the same order as the original BrowsCap list
		for index in sorted(subcoll):
			data_index = index

			# Compile only the patterns that are needed
			if bc_data[data_index][5] != True:
				bc_data[data_index][6]=re.compile(bc_data[data_index][0])
				bc_data[data_index][5]=True		

			# Using the bc_data, compare regex for each index; if matched, record results and stop looking
			if bc_data[data_index][6].search(ua_string):
				isbot = bc_data[data_index][2]
				os = bc_data[data_index][3]
				device = bc_data[data_index][4]
				browser = bc_data[data_index][1]
				
				# Add data associated with this User Agent string match to ua_str array (for this run only).This avoids looking up the details of the same UA string more than once per run of the code.
				ua_str.append(ua_string)
				entry = []
				entry.append(isbot)
				entry.append(os)
				entry.append(device)
				entry.append(browser)
				ua_data.append(entry)

				break

	if isbot == 'Bot/Crawler':
		writeline = False


	data = []
	data.append(writeline)
	data.append("\t".join(lineSplit[0:43]) + "\t" + device + "\t" + os + "\t" + browser + "\t" + lineSplit[46] + "\n")
	return data

# read file path and name from command line
inputpath = sys.argv[1]
inputfile = sys.argv[2]
outputpath = sys.argv[3]
outputfile1 = sys.argv[4]
outputfile2 = sys.argv[5]
uastring = sys.argv[6]
uadata = sys.argv[7]
browscap = sys.argv[8]
trie = sys.argv[9]

# open read and write files
f = open(inputpath + '/' + inputfile + '.log', 'r', encoding='latin-1')
n = open(outputpath + '/' + outputfile1 + '.log', 'w', encoding="latin-1")
m = open(outputpath + '/' + outputfile2 + '.log', 'w', encoding="latin-1")

# The "ua_str" pickled array contains the regexes for a small set of very common User Agents
with open(uastring, 'rb') as a:
	ua_str = pickle.load(a)

# The "ua_data" pickled array contains the basic classification data for a small set of very common User Agents
with open(uadata, 'rb') as b:
	ua_data = pickle.load(b)

# The "bc_data" pickled "array of arrays" contains the information from the BrowsCap Project. Each "row" deals with a specific regex; the first column is the regex, 
# the subsequent columns contain the classification data (e.g. bc_data[1][0] is the compiled regex, bc_data[1][6] is the browser etc.)
with open(browscap, 'rb') as c:
	bc_data = pickle.load(c)

# The "bc_trie" pickled data structure is the compiled trie data, which consists of many key/value pairs. The keys are generated from prefix+regex strings, and the value tuples 
# contain the integer index of the bc_data array (above) first dimension that corresponds to the regex.
with open(trie, 'rb') as d:
	bc_trie = pickle.load(d)

# cycle through lines, omitting those that don't match the relevant criteria
for line in f:
	result = formatLine1(line)
	if result[0]:
		n.write(result[1])
	else:
		m.write(result[1])	

