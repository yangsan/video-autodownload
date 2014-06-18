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
def showShowList():
    show_list = db.getShowList()
    if show_list:
        for number, show in enumerate(show_list):
            print "%d) %s" % (number, show[0])
    else:
        print "The show list is empty, please add some."

def addNewShow():
    show_name = raw_input("Enter the show name:")
    url = raw_input("Enter show url:")
    show_table_name = show_name.replace(" ", "_")
    db.addNewRowInShowTable(show_name, url, show_table_name)


def deleteShow():
    pass


#swich func
#########################################################################
def switch(flag):
    return {
        "1": showShowList,
        "2": addNewShow
    }[flag]


if __name__ == "__main__":

    while True:
        print "_" * 60
        print "*" * 60
        print "What do you want?"
        print "1.Show show list"
        print "2.Add new show"
        flag = raw_input("==>")
        switch(flag)()

    #url = "http://www.ttmeiju.com/meiju/The.Tonight.Show.Starring.Jimmy.Fallon.html"

    #soup = htmlReader(url)

    #for item in soup.find_all("a", title=u"磁力链"):
        ##print type(item)
        #print item.parent.previous_sibling.previous_sibling
        #break
