# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import urllib2
from subprocess import call
import json


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

    #url = "http://eztv.it/shows/991/seth-meyers-late-night-with/"
    #url = "http://eztv.it/shows/983/the-tonight-show-starring-jimmy-fallon/"
    url = "http://eztv.it/shows/632/derek/"

    soup = htmlReader(url)

    filename = "./json/derek.json"

    #try to open local json eplist
    try:
        with open(filename) as f:
            eplist = json.load(f)
    except:
        print "%s dosen't exit or is empty." % (filename)
        eplist = dict()

    for item in soup.find_all("tr", class_='forum_header_border'):
        epinfo = item.find_all("a", class_="epinfo")
        if len(epinfo) > 0:
            showname = epinfo[0]["title"]
            if (showname not in eplist) or (not eplist[showname]):
                print "Try to download ep: %s" % (showname)
                magnet = item.find_all("a", class_="magnet")[0]["href"]
                call(["transmission-gtk", magnet])
                eplist[showname] = True

    with open(filename, "w+") as f:
        json.dump(eplist, f)
