import requests
from bs4 import BeautifulSoup
import urllib2
import base64
import sys

try:
	if "http://" not in sys.argv[1]:
		print "not the expected url please check your input"
	else:
		url = sys.argv[1]

		file_name = url[url.index("@"):url.index("&")].replace('@','')
		print file_name
		r = requests.get(url)
		data = r.text

		data_cleaned = {}
		for x in data.split():
			if 'class="uid"' in x and "@" in x:
				data_cleaned[int(x.replace('&#x2F;','/').replace('class="uid">','').replace('</span>','').split('@')[0])] = x.replace('&#x2F;','/').replace('class="uid">','').replace('</span>','').split('@')[1]

		with open(file_name,"wb") as handle:
			for x in range(0,len(data_cleaned)):
				handle.write(base64.b64decode(data_cleaned[x]))
		print file_name + " has been downloaded."
except:
	print "Something went wrong please try again, check your input or try switching your computer on and off"
