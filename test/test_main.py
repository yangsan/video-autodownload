# -*- coding: utf8 -*-
import videodownloader
import db

#videodownloader.intializeEpList("good", "http://www.ttmeiju.com/meiju/The.Tonight.Show.Starring.Jimmy.Fallon.html")
conn, cursor = db._connectDatabase()

#fetch = cursor.execute("""
               #select * from jimmy
               #""")

#for item in fetch:
    #print item
#fetch = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jimmy'")
#fetch = cursor.execute("select * from showlist")
#fetch = cursor.execute("select * from jimmy where status = 0")
#fetch = cursor.execute("select * from craig where status = 0")
#cursor.execute("delete from jimmy where rowid = 3")
#cursor.execute("delete from jimmy where rowid = 4")
#cursor.execute("delete from jimmy where rowid = 5")
#cursor.execute("delete from craig where rowid = 4")
#cursor.execute("delete from craig where rowid = 3")

#print fetch.fetchone()
#for item in fetch.fetchall():
    #print item
    #ep_name = item[0]
    #print ep_name
    #db.changeStatus("jimmy", ep_name)

#print fetch.fetchone()
#for item in fetch:
    #print item

#videodownloader.showEpListTable("Late_Night_with_Seth_Meyers")
videodownloader.showEpList()

db._closeDatabase(conn, cursor)
