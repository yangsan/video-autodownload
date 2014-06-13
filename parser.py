# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import urllib2
from subprocess import call


if __name__ == "__main__":

    #url = "http://eztv.it/shows/991/seth-meyers-late-night-with/"
    #url = "http://eztv.it/shows/983/the-tonight-show-starring-jimmy-fallon/"
    url = "http://eztv.it/shows/632/derek/"

    req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})

    resp = urllib2.urlopen(req)

    print "Done open request."

    respHTML = resp.read()

    print "Done reading contents."

    soup = BeautifulSoup(respHTML)

    eplist = dict()

    #soup = BeautifulSoup(open("seth.html"))

    for item in soup.find_all("tr", class_='forum_header_border'):
        epinfo = item.find_all("a", class_="epinfo")
        if len(epinfo) > 0:
            magnet = item.find_all("a", class_="magnet")[0]["href"]

            call(["transmission-gtk", magnet])

            eplist[epinfo[0]["title"]] = True
        ##for post in item.contents:
        #for post in item.children:
            ##print post
            #print type(post)
    for item in sorted(eplist.keys()):
        print item
    #print type(eplist.keys())
