# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import urllib2
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
def showShowList(show_list = None):
    if show_list:
        printBeginofBlock()
        print "The show list:"
        for number, show in enumerate(show_list):
            print "%d) %s showid: %d" % (number, show[1], show[0])
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
    show_table_name = show_name.replace(" ", "_")
    db.addNewRowInShowTable(show_name, url, show_table_name)


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
                print "%s deleted." % show_map[show_id_input][1]
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



#swich func
#########################################################################
def switch(flag):
    return {
        "1": showShowList,
        "2": addNewShow,
        "3": deleteShow
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
        flag = raw_input("==>")
        switch(flag)()

    #url = "http://www.ttmeiju.com/meiju/The.Tonight.Show.Starring.Jimmy.Fallon.html"

    #soup = htmlReader(url)

    #for item in soup.find_all("a", title=u"磁力链"):
        ##print type(item)
        #print item.parent.previous_sibling.previous_sibling
        #break
