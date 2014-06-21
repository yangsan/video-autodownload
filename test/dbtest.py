# -*- coding: utf8 -*-
import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

#cursor.execute("""
                #create table showlist
                #(
                #showname text,
                #url text,
                #tablename text
                #)
                #""")

show_name = "Jimmy Fallon"
url = "https:"
tablename = "jimmy_fallon"

#cursor.execute("""
               #insert into showlist
               #(showname, url, tablename)
                #values (?, ?, ?)""", (show_name, url, tablename))

#cursor.execute("""
               #insert into showlist
               #(showname, url, tablename)
                #values (?, ?, ?)""", ("aig", url, tablename))

#cursor.execute("""
               #delete from showlist
               #where rowid = 1
               #""")

cursor.execute("""
            select %s from showlist
            """ % ("showname"))

print cursor.fetchall()

conn.commit()
cursor.close()
conn.close()
