# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import urllib2
from subprocess import call
import json
import os

show_list_path = "./data/show_list.json"

#methods for show list
#################################################################


def addNewShow():
    if not os.path.exists("./data"):
        call(["mkdir", "data"])

    show_list = openShowList()
    if not show_list:
        print "Build a new one."
        show_list = dict()

    show_name = raw_input("Enter show name:")
    url = raw_input("Enter show url:")
    show_file_name = show_name.replace(" ", "_")

    show_list[show_name] = {"url": url,
                            "filename": "./data/" + show_file_name + ".json"}

    print "Now try to initialize episodes list..."
    initEpList(show_list[show_name])

    saveShowList(show_list)

    print "Show \"%s\"added." % (show_name)


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


def showShowList(show_list=None):
    if show_list:
        print "-------------------------------------------------------------------------"
        print "*************************************************************************"
        print "Show list:"
        for i, showname in enumerate(show_list.keys()):
            print "%d. %s" % (i, showname)
        print "*************************************************************************"
        print "-------------------------------------------------------------------------"
    else:
        show_list = openShowList()
        if show_list:
            showShowList(show_list)


def deleteShow():
    show_list = openShowList()
    if show_list:
        show_name_list = show_list.keys()

        print "-------------------------------------------------------------------------"
        print "*************************************************************************"
        print "Show list:"
        for i, showname in enumerate(show_name_list):
            print "%d. %s" % (i, showname)
        print "*************************************************************************"
        print "-------------------------------------------------------------------------"
        number = int(raw_input(
            "Enter the number before the one you want to delete , enter other keys to abort\n==>:"))
        try:
            showname = show_name_list[number]
            call(["rm", show_list[showname]["filename"]])
            show_list.pop(showname)
            saveShowList(show_list)
            print "\"%s\" deleted" % (showname)
            print "---------------------------------------------------------------------"
        except:
            print "Invalid input, abort."


#################################################################

#methods for ep list
#################################################################


def initEpList(show_info):
    """
    Taking in a dict:
        {
        "url"       :   "http:...",
        "filename"  :   "file_name"
        }
    """
    soup = htmlReader(show_info["url"])
    ep_list = dict()

    while True:
        download_all = raw_input("Do you want to download all?[y/n/per]")
        if download_all == "y" or download_all == "n" or download_all == "per":
            break
        else:
            print "Invalid input, please try again."

    for item in soup.find_all("tr", class_='forum_header_border'):
        ep_info = item.find_all("a", class_="epinfo")
        if len(ep_info) > 0:
            ep_name = ep_info[0]["title"]
            if ep_name not in ep_list:

                if "y" == download_all:
                        ep_list[ep_name] = False

                elif "n" == download_all:
                        ep_list[ep_name] = True

                elif "per" == download_all:
                        while True:
                            flag = raw_input("Do you want to download \" %s \"?[y/n]" % (ep_name))
                            if "y" == flag:
                                ep_list[ep_name] = False
                                break
                            elif "n" == flag:
                                ep_list[ep_name] = True
                                break
                            else:
                                print "Invalid input, please try again."

    saveEpList(show_info["filename"], ep_list)


def saveEpList(filename, ep_list):
    with open(filename, "w+") as f:
        json.dump(ep_list, f)


def openEpList(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except:
        print "Episodes list dosen't exit or is empty."
        return None


def showEpList():
    show_list = openShowList()
    if show_list:
        show_name_list = show_list.keys()
        print "-------------------------------------------------------------------------"
        print "*************************************************************************"
        print "Show list:"
        for i, showname in enumerate(show_name_list):
            print "%d. %s" % (i, showname)
        print "*************************************************************************"
        print "-------------------------------------------------------------------------"
        number = int(raw_input(
            "Enter the number before the show you want for episodes list, enter other keys to abort\n==>:"))
        try:
            showname = show_name_list[number]
            show_info = show_list[showname]
            filename = show_info["filename"]
            ep_list = openEpList(filename)
            if ep_list:
                print "-------------------------------------------------------------------------"
                print "*************************************************************************"
                print "Episodes list:"
                for i, showname in enumerate(sorted(ep_list.keys(), reverse=True)):
                    if i>10:
                        break
                    if ep_list[showname]:
                        print "%d. Status: done     Show name: %s" % (i, showname)
                    else:
                        print "%d. Status: not yet  Show name: %s" % (i, showname)
                print "*************************************************************************"
                print "-------------------------------------------------------------------------"

        except StandardError, e:
            print "Error:" , e
            print "Invalid input, abort."

#################################################################



#parser and downloader
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

def freshAndDownload():
    show_list = openShowList()
    if show_list:
        for show_info in show_list.values():
            soup = htmlReader(show_info["url"])
            filename = show_info["filename"]

            try:
                with open(filename) as f:
                    ep_list = json.load(f)

                for item in soup.find_all("tr", class_='forum_header_border'):
                    ep_info = item.find_all("a", class_="epinfo")
                    if len(ep_info) > 0:
                        showname = ep_info[0]["title"]
                        if (showname not in ep_list) or (not ep_list[showname]):
                            print "Try to download ep: %s" % (showname)
                            magnet = item.find_all("a", class_="magnet")[0]["href"]
                            call(["transmission-gtk", magnet])
                            ep_list[showname] = True

                with open(filename, "w+") as f:
                    json.dump(ep_list, f)

            except:
                print "%s dosen't exit or is empty." % (filename)

#################################################################


#args handler
#################################################################


def switch(flag):
    return {"1": addNewShow,
            "2": showShowList,
            "3": deleteShow,
            "4": freshAndDownload,
            "5": showEpList}[flag]

#################################################################


if __name__ == "__main__":

    while True:
        print "What do you want?"
        print "1.add new show"
        print "2.show show list"
        print "3.delete show"
        print "4.fresh and download"
        print "5.show episodes list"
        print "Others to abort"
        flag = raw_input("==>")
        try:
            switch(flag)()
        except StandardError, e:
            print "Abort."
            break
