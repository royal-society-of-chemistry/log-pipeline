import re
import sys

# read file path and name from command line
inputpath = sys.argv[1]
inputfile = sys.argv[2]
outputpath = sys.argv[3]
outputfile = sys.argv[4]

# Regex patterns - recognise products and their details pased on web address
p1 = re.compile('^/(?:en|is)/content/article(html|pdf)/(\d{4})/([a-z][a-z0-9])/([a-z]\d[a-z][a-z]\d{5}[a-z]|[a-z]\d{6}[a-z]|[a-z][a-z0-9]\d{10})$')
p2 = re.compile('^/(?:en|is)/content/chapter(html|pdf)/(\d{4})/((?:[a-z][a-z0-9])?\d{12}[x0-9]-[a-z0-9]{2}\d{3})(/[-0-9x]+)?$')
p3 = re.compile('^/marinlit/(?:compound|article)/(c[ms]\d{12}).*$')
p4 = re.compile('^/lus/(analytical-abstracts|chemical-hazards-industry|laboratory-hazards-bulletin)/article/([bj]\d+).*$')
p5 = re.compile('^/lus/(natural-product-updates|synthetic-reaction-updates|catalysts-and-catalysed-reactions|methods-in-organic-synthesis)/search/.*$')
p6 = re.compile('^/suppdata/([a-z][a-z0-9])/[a-z]\d/([a-z]\d[a-z][a-z]\d{5}[a-z]|[a-z]\d{6}[a-z]|[a-z][a-z0-9]\d{10})/.*\.([a-z0-9]+)$')
p7 = re.compile('^/merck-index/(?:monograph|reaction)/((?:m|r|mono)\d+).*$')
p8 = re.compile('^/learn-chemistry/(?:resource)/(res|rdc)(\d{8}).*$')
p9 = re.compile('^/[a-z]+/(hc\d{4})/hc\d{4}\.pdf$')

q1 = re.compile('q=unauthorize')
q2 = re.compile('branding(?:=|=instituteid=)([0-9]+)')

# Functions
def formatLine1(line):

	# Separate log entry into constituent parts 
	lineSplit = line.rstrip("\n").split("\t")

	# Harvest useful fields	
	target_domain=lineSplit[3].lower()
	target_url=lineSplit[6].lower()
	target_param=lineSplit[7].lower()
	user_cookie=lineSplit[13].lower()

	# Initial values of enriched terms
	terms = "??"             # col 33 | set TO "??"
	success = "Yes"          # col 34 | set to "Yes" 
	branding = "-"           # col 36 | ID from cookie
	year = "-"               # col 37 | publication year of download
	jnl = "-"                # col 38 | product id of download
	msid = "-"               # col 39 | unique id of download
	frmat = "-"              # col 40 | format of download (html|pdf)

#####################################################################################################
# COMMENTED SECTION BELOW IS PROVIDED AS AN ILLUSTRATION OF POSSIBLE WAYS OF EXTRACTING INFORMATION #
# CUSTOM ROUTINES APPROPRIATE TO YOUR CONTENT SHOULD BE CREATED AS NECESSARY                        #
#####################################################################################################
#	# Break up target url into components
#	# NOTE: url of just "/" will give array of size 1 where addr_elts[1]=""	
#	addr_elts = target_url.split("/")
#
#	# Check if target url is more than just "/"	
#	if (len(addr_elts) > 1):
#
#		# Use value of address "top folder" to direct search strategy, then use regex patterns to extract info
#		if ( addr_elts[1] == 'en' or addr_elts[1] == 'is' ):
#			m1 = p1.search(target_url)
#			m2 = p2.search(target_url)
#			if m1:
#				year = str(m1.group(2))
#				jnl = str(m1.group(3))
#				msid = str(m1.group(4))
#				frmat = str(m1.group(1))
#
#			elif m2:
#				year = str(m2.group(2))
#				jnl = "book"
#				msid = str(m2.group(3))
#				frmat = str(m2.group(1))
#
#		elif ( addr_elts[1] == 'marinlit' ):
#			m3 = p3.search(target_url)
#			if m3:
#				year = "-"
#				jnl = "marinlit"
#				msid = str(m3.group(1))
#				frmat = "html"
#		elif ( addr_elts[1] == 'merck-index' ):
#			m7 = p7.search(target_url)
#			n1 = q1.search(target_param)
#			if m7 and not n1:
#				year = "-"
#				jnl = "merck"
#				msid = str(m7.group(1))
#				frmat = "html"
#		elif ( addr_elts[1] == 'lus' ):
#			m4 = p4.search(target_url)
#			m5 = p5.search(target_url)
#			if m4:
#				year = "-"
#				if str(m4.group(1)) == "analytical-abstracts":
#					jnl = "aab"
#				elif str(m4.group(1)) == "chemical-hazards-industry":
#					jnl = "chi"
#				elif str(m4.group(1)) == "laboratory-hazards-bulletin":
#					jnl = "lhb"
#				msid = str(m4.group(2))
#				frmat = "html"
#			elif m5:
#				year = "-"
#				if str(m5.group(1)) == "natural-product-updates":
#					jnl = "npu"
#				elif str(m5.group(1)) == "synthetic-reaction-updates":
#					jnl = "sru"
#				elif str(m5.group(1)) == "catalysts-and-catalysed-reactions":
#					jnl = "ccr"
#				elif str(m5.group(1)) == "methods-in-organic-synthesis":
#					jnl = "mos"
#				msid = "-"
#				frmat = "html"
#		elif ( addr_elts[1] == 'suppdata' ):
#			m6 = p6.search(target_url)
#			if m6:
#				year = "-"
#				jnl = str(m6.group(1))
#				msid = str(m6.group(2))
#				frmat = str(m6.group(3))
#		elif ( addr_elts[1] == 'learn-chemistry' ):
#			m8 = p8.search(target_url)
#			if m8:
#				year = "-"
#				if str(m8.group(1)) == "res":
#					jnl = "lcm"
#				elif str(m8.group(1)) == "rdc":
#					jnl = "otdic"
#
#				msid = str(m8.group(1)) + str(m8.group(2))
#				frmat = "html"
#		elif ( target_domain == 'hc-content.rsc.org' ):
#			year = "-"
#			jnl = "hcoll"
#			msid = addr_elts[2]
#			frmat = "pdf"
#
#
#
#	n2 = q2.search(user_cookie)
#	if n2:
#		branding = str(n2.group(1))


	string1 = terms + "\t" + success
	string2 = branding + "\t" + year + "\t" + jnl + "\t" + msid + "\t" + frmat

	# Write line to new logfile with replacement values extracted from original
	n.write("\t".join(lineSplit[0:33]) + "\t" + string1 + "\t" + lineSplit[35] + "\t" + string2 + "\t" + "\t".join(lineSplit[41:]) + "\n")

# open read and write files
f = open(inputpath + '/' + inputfile + '.log', 'r', encoding='latin-1')
n = open(outputpath + '/' + outputfile + '.log', 'w', encoding="latin-1")

# cycle through lines, omitting those that don't match the relevant criteria
for line in f:
	formatLine1(line)

