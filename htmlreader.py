# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import urllib2
#import urllib
#import cookielib
import sys


def correct_encoding(html):
    """
    check the html's encoding and return in utf-8
    """
    #soup = BeautifulSoup(html)
    return html


if __name__ == "__main__":

    #url = "http://c.learncodethehardway.org/book/"
    #ur l = "http://www.ttmeiju.com/"
    #url = "http://www.ttmeiju.com/meiju/Late.Night.with.Seth.Meyers.html"
    #url = "http://eztv.it/shows/991/seth-meyers-late-night-with/"

    #req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})

    #resp = urllib2.urlopen(req)

    #code = sys.getfilesystemencoding()

    #respHTML = resp.read().decode(encoding="gbk").encode(code)

    #soup = BeautifulSoup(respHTML)

    #showList = set()
    #for item in soup.find_all("a", class_='magnet'):
        ##print item.attrs
        #showList.add(item.attrs['href'])


    test = set()
    for i in range(10):
        test.add(i)
    test.add(1)
    test.add(10)
    test.add(1)

    print test


    #with open('sethmeyers.html','w') as f:
        #f.write(respHTML.decode(encoding="gbk").encode(code))
        #f.write(respHTML)
    #print respHTML
