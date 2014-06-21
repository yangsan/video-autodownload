# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import urllib2
from subprocess import Popen
import db


#url reader
#########################################################################
def htmlReader(url):
    """
    Taking in a url return a BeautifulSoup soup object.
    """
    req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
    resp = urllib2.urlopen(req)
    respHTML = resp.read()

    return BeautifulSoup(respHTML)


#show list maintainer
#######################################################################e#
def showShowList(show_list=None):
    if show_list:
        printBeginofBlock()
        print "The show list:"
        for number, show in enumerate(show_list):
            print "%d) %s" % (number, show[1])
        printEndofBlock()
        return 1
    else:
        show_list = db.getShowList()
        if not show_list:
            print "The show list is empty, please add some."
            return 0
        else:
            showShowList(show_list)


def addNewShow():
    show_name = raw_input("Enter the show name:")
    url = raw_input("Enter show url:")

    print "Do you want to auto-download this show?[y/n]"
    while True:
        status = raw_input("==>")
        if status == "n":
            status_code = 1
            break
        elif status == "y":
            status_code = 0
            break
        else:
            print "Invalid input, please try again."

    show_table_name = show_name.replace(" ", "_")
    if not db.addNewRowInShowTable(show_name, url, show_table_name, status_code):
        print "Show info already exists."
    else:
        if not db.createEpListTable(show_table_name):
            print "Episodes list already exists."
        else:
            initializeEpList(show_table_name, url)


def deleteShow():
    """
    delete a show
    """
    show_list = db.getShowList()
    show_map = {}
    if show_list:
        print "Which one do you want to delete? Enter n to abort."
        for number, show in enumerate(show_list):
            print "%d) %s" % (number, show[1])
            show_map[number] = show

        while True:
            show_id_input = raw_input("==>")
            if show_id_input == "n":
                print "Abort delete."
                return 1
            try:
                show_id_input = int(show_id_input)
                show_id = show_map[show_id_input][0]
                db.deleteShowListRow(show_id)
                db.deleteEpList(show_map[show_id_input][3])
                print "Show: %s deleted." % show_map[show_id_input][1]
                return 0
            except ValueError, e:
                print "Error: ", e
                print "Please try again."
            except KeyError, e:
                print "Error: input number out of range."
                print "Please try again."

    else:
        print "The show list is empyt, can't delete any."

    return 0


#episodes list maintainer
#########################################################################
def initializeEpList(show_table_name, url):
    soup = htmlReader(url)

    while True:
        download_all = raw_input("Do you want to download all?[y/n/per]")
        if download_all == "y" or download_all == "n" or download_all == "per":
            break
        else:
            print "Invalid input, please try again."

    for item in soup.find_all("a", title=u"磁力链"):
        ep_name = item.parent.previous_sibling.previous_sibling.string
        magnet = item["href"]
        if "y" == download_all:
            db.addNewEp(show_table_name, ep_name, magnet, 0)
        elif "n" == download_all:
            db.addNewEp(show_table_name, ep_name, magnet, 1)
        else:
            while True:
                #print ep_name
                flag = raw_input("Do you want to download \" %s \"?[y/n]"
                                 % (ep_name.encode("utf8")))
                if "y" == flag:
                    db.addNewEp(show_table_name, ep_name, magnet, 0)
                    break
                elif "n" == flag:
                    db.addNewEp(show_table_name, ep_name, magnet, 1)
                    break
                else:
                    print "Invalid input, please try again."


def showEpList():
    show_list = db.getShowList()
    show_map = {}
    if show_list:
        print "Which one do you want to see? Enter n to abort."
        for number, show in enumerate(show_list):
            print "%d) %s" % (number, show[1])
            show_map[number] = show

        while True:
            show_id_input = raw_input("==>")
            if show_id_input == "n":
                print "Abort delete."
                return 1
            try:
                show_id_input = int(show_id_input)
                show_table_name = show_map[show_id_input][3]
                showEpListTable(show_table_name)
                return 0
            except ValueError, e:
                print "Error: ", e
                print "Please try again."
            except KeyError, e:
                print "Error: input number out of range."
                print "Please try again."

    else:
        print "The show list is empyt, nothing to show."

    return 0


def showEpListTable(table_name):
    status = {0: "not downloaded yet",
              1: "done",
              2: "pending"}
    ep_list = db.getEpList(table_name)
    print "The episodes list:"
    for number, ep in enumerate(ep_list):
        print "%d) status:%s  %s" % (number, status[ep[2]], ep[0].encode("utf8"))


#fresh episodes list
#########################################################################
def freshEpList():
    print "Freshing episodes list:"
    show_list = db.getShowList()
    for show in show_list:
        show_name = show[1]
        url = show[2]
        show_table_name = show[3]
        if show[4]:
            status = 2
        else:
            status = 0
        print "Try: %s" % (show_name)
        soup = htmlReader(url)
        for item in soup.find_all("a", title=u"磁力链"):
            ep_name = item.parent.previous_sibling.previous_sibling.string
            magnet = item["href"]
            if db.addNewEp(show_table_name, ep_name, magnet, status):
                print "Episode: %s added" % ep_name


#comfirm pending shows
#########################################################################
def confirmPendingEps():
    show_list = db.getShowList()
    flag = 0
    for show in show_list:
        show_table_name = show[3]
        pending_list = db.getSpecificEpList(show_table_name, 2)
        if pending_list:
            for ep in pending_list:
                flag = 1
                ep_name = ep[0]
                print "Do you want to download: %s?[y/n]" % (ep_name)

                while True:
                    user_input = raw_input("==>")
                    if user_input == "n":
                        db.changeStatus(show_table_name, ep_name, 1)
                        break
                    elif user_input == "y":
                        db.changeStatus(show_table_name, ep_name, 0)
                        break
                    else:
                        print "Invalid input, please try again."
    if not flag:
        print "Clear nothing pending."


#download ep list
#########################################################################
def downloadEp():
    print "Downloading..."
    show_list = db.getShowList()
    flag = 0
    for show in show_list:
        show_table_name = show[3]
        undone_list = db.getSpecificEpList(show_table_name, 0)
        if undone_list:
            for ep in undone_list:
                print "Try: %s" % (ep[0])
                with open("log.out", "a+") as f:
                    Popen(["transmission-gtk", ep[1]], stderr=f)
                    flag = 1
                db.changeStatus(show_table_name, ep[0], 1)
    if not flag:
        print "Clear, nothing downloaded."


#swich func
#########################################################################
def switch(flag):
    return {
        "1": showShowList,
        "2": addNewShow,
        "3": deleteShow,
        "4": freshEpList,
        "5": downloadEp,
        "6": showEpList,
        "7": confirmPendingEps
    }[flag]


def printBeginofBlock():
    print "_" * 60
    print "*" * 60


def printEndofBlock():
    print "*" * 60
    print "-" * 60

if __name__ == "__main__":

    while True:
        printBeginofBlock()
        print "What do you want?"
        print "1.Show show list"
        print "2.Add new show"
        print "3.Delete show"
        print "4.Fresh episodes list"
        print "5.Download"
        print "6.Show episodes list"
        print "7.Confirm pending episodes"
        flag = raw_input("==>")
        switch(flag)()
