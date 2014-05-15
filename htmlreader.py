# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import urllib2
import urllib
import cookielib
import sys

#url = "http://c.learncodethehardway.org/book/"
#url = "http://www.ttmeiju.com/"
url = "http://www.ttmeiju.com/meiju/Late.Night.with.Seth.Meyers.html"

req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})

resp = urllib2.urlopen(req)

respHTML = resp.read()

code = sys.getfilesystemencoding()

with open('ttmeiju.html','w') as f:
    f.write(respHTML.decode(encoding="gbk").encode(code))
print type(respHTML)
#print respHTML
