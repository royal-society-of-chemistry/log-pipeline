import sys
import os

from datetime import datetime
from datetime import timedelta
import re
import gzip


monthToNumber = {
		'jan': '01',
		'feb': '02',
		'mar': '03',
		'apr':'04',
		 'may':'05',
		 'jun':'06',
		 'jul':'07',
		 'aug':'08',
		 'sep':'09',
		 'oct':'10',
		 'nov':'11',
		 'dec':'12'
		}
	
def convertDate(inDate):
	dSplit=inDate.split("/")
	if(len(dSplit)!=3):
		raise ValueError("Date format incorrect for Apache/NCSA: " + inDate)
	year=dSplit[2]
	monthAsWord=dSplit[1]
	day=dSplit[0]
	
	if(len(day)==1):
		day="0"+day
	
	month=monthToNumber[monthAsWord.lower()]
	if(month==None):
		raise ValueError("Date format incorrect for Apache/NCSA: " + inDate)
	return year+"-"+month+"-"+day
	
if(len(sys.argv)!=5):
	print("Usage: ncsaToW3c.py <indir> <outdir> <inputfilename> <outputfilename>")
	
	
# read file name from command line
inputDir=sys.argv[1]
outputDir=sys.argv[3]

filename = sys.argv[2]
newfilename = sys.argv[4]

f = open(inputDir+os.sep+filename+'.log', mode='r', encoding="latin-1")
n = open(outputDir+os.sep+newfilename+'.log', mode='w', encoding="latin-1")

n.write("#Fields: DateTime s-ip s-sitename s-computername cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs-version cs(User-Agent) cs(Cookie) cs(Referer) cs-host sc-status sc-substatus sc-win32-status sc-bytes cs-bytes time-taken ImportID\n")
regexNcsa = re.compile('([(\d\.)]+) (.*?|-) (.*?|-) \[(.*?)\] "(.*?)" (\d+|-) (\d+|-) "(.*?)" "(.*?)" "(.*?)"')
for line in f:
	try:
		parseLine=regexNcsa.search(line)
		splitLine=line.split(" ")
		ip=parseLine.group(1)
		user_identifier=parseLine.group(2)
		username=parseLine.group(3)
		if(username==""):
			username="-"
		datestamp=parseLine.group(4)
		request=parseLine.group(5).strip().replace("\"","") #GET /RSCpubs.ePlatform.Service.FreeContent.ImageService.svc/ImageService/image/GA?id=C4EE03690E HTTP/1.1
		statusCode=parseLine.group(6)
		returnSize=parseLine.group(7)
		referer=parseLine.group(8)
		userAgent=parseLine.group(9)
		cookie=parseLine.group(10)
		
		userAgent=userAgent.replace("\"","").replace(" ","+")
		cookie=cookie.replace("\"","").replace(" ","+")
		referer=referer.replace("\"","").replace(" ","+")
		#data stamp are in the format [02/Jan/2015:00:05:03 +0000] - convert to 2015-01-02 00:05:03
		dateSplit=datestamp.split(":")
		dateOnly=dateSplit[0]
		dateOnly=convertDate(dateOnly)
		timeOnly=dateSplit[1]+":"+dateSplit[2]+":"+dateSplit[3].split(" ")[0]
		#have to tify up to remove space and also parse out method call type etc
		methodType="-"
		csUriQuery="-"
		csUriStem="-"
		protocolVersion="-"
		
		if(request != "" and request!="-"):
			requestSplit=request.split(" ")
			methodType=requestSplit[0].strip()
			if(len(methodType)==0):
				methodType="-"
			if(len(requestSplit)>1):
				requestUrl=requestSplit[1].strip()
				if(len(requestUrl)!=0):
					requestUrlSplit=requestUrl.split("?")
					csUriStem=requestUrlSplit[0].strip()
					if(len(csUriStem)==0):
						csUriStem="-"
					if(len(requestUrlSplit)>1):
						csUriQuery=requestUrlSplit[1]
						csUriQuery=csUriQuery.replace(" ","+")
						if(len(csUriQuery)==0):
							csUriQuery="-"
				if(len(requestSplit)>2):
					protcolVersion=requestSplit[2].strip()
					if(len(protocolVersion)==0):
						protocolVersion="-"
	
		n.write(dateOnly+" "+timeOnly+" "+"192.168.0.1 pubs.rsc.org - "+methodType+ " "+csUriStem+" "+csUriQuery+" - "+username+" "+ip+" "+protocolVersion+ " " +userAgent+" " +cookie + " " +referer + " - "+statusCode+ " - - - "+returnSize+ " - -\n")
			
	except Exception as e:
		print ("Error: {0}".format(e))
		print("Error on: " + line)
		
		
	


