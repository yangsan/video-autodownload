# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import urllib2


def htmlReader(url):
    """
    Taking in a url return a BeautifulSoup soup object.
    """
    req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})

    resp = urllib2.urlopen(req)

    print "Done open request."

    respHTML = resp.read()

    print "Done reading contents."

    return BeautifulSoup(respHTML)


if __name__ == "__main__":

    url = "http://www.ttmeiju.com/meiju/The.Tonight.Show.Starring.Jimmy.Fallon.html"

    soup = htmlReader(url)

    for item in soup.find_all("a", title=u"磁力链"):
        #print type(item)
        print item.parent.previous_sibling.previous_sibling
        break
