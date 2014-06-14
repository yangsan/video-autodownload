# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import urllib2
from subprocess import call
import json

show_list_path = "./data/show_list.json"

#################################################################
def addNewShow():
    show_list = openShowList()
    if not show_list:
        print "Build a new one."
        show_list = dict()

    show_name = raw_input("Enter show name:")
    url = raw_input("Enter show url:")
    show_file_name = show_name.replace(" ", "_")

    show_list[show_name] = {"url": url, "filename": show_file_name}

    saveShowList(show_list)

    print "Show \" %s \"added." % (show_name)


def openShowList():
    try:
        with open(show_list_path) as f:
            show_list = json.load(f)
        return show_list
    except:
        print "Show list dosen't exit or is empty."
        return None

def saveShowList(show_list):
    try:
        with open(show_list_path, "w+") as f:
            json.dump(show_list, f)
    except IOError:
        print "Can't open show list file."


def showShowList(show_list):
    if show_list:
        print "Show list:"
        for showname in show_list.keys():
            print showname
    else:
        print "Show list is empty."


def deleteShow():
    show_list = openShowList()
    if show_list:
        show_name_list = [name for name in show_list.keys()]
        print "Show List:"
        for i, name in enumerate(show_name_list):
            print "%d. %s" %(i, name)
        number = int(raw_input(
            "Enter the number before theone you want to delete , enter other keys to abort\n ==>:"))
        try:
            show_list.pop(show_name_list[number])
            saveShowList(show_list)
            print "\" %s \" deleted" % (show_name_list[number])
            print "--------------------------------------------"
        except:
            print "Invalid input, abort."


#################################################################


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


def epDownloader(soup, filename):

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


if __name__ == "__main__":

    ##url = "http://eztv.it/shows/991/seth-meyers-late-night-with/"
    ##url = "http://eztv.it/shows/983/the-tonight-show-starring-jimmy-fallon/"
    #url = "http://eztv.it/shows/632/derek/"

    #soup = htmlReader(url)

    #filename = "./json/derek.json"

    #epDownloader(soup, filename)
    deleteShow()

