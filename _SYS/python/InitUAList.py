import re
import sys
import pickle

picklepath = sys.argv[1]

ua_str = []
ua_str.append('-')
ua_str.append('LOCKSS+cache')
ua_str.append('Sparrho+scraper+(+http://www.sparrho.com)')
ua_str.append('Sogou+web+spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)')
ua_str.append('EPiServer+LinkValidator')
ua_str.append('MoodleBot/1.0')

ua_data = []

for string in ua_str:
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


