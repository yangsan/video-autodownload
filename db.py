# -*- coding: utf8 -*-
import sqlite3

#initilize or connect the database
conn = sqlite3.connect("showlist.db")
cursor = conn.cursor()


try:
    cursor.execute("select * from showlist")
except StandardError, e:
    print e, "\n try to create one."
    cursor.execute("""
                   create table showlist
                   (
                   showname text,
                   url text,
                   tablename text
                   )
                   """)
    cursor.execute("select * from showlist")

#cursor.execute("""
               #create table person
               #(
               #name varchar(20),
               #city varchar(20)
               #)
               #""")

#cursor.execute("""
               #insert into person
               #(name, city)
                #values ('kevin', 'Lanzhou')""")

#cursor.execute("""
               #insert into person
               #(name, city)
                #values ('mark', 'print')
               #""")


cursor.execute("select * from showlist")
print cursor.fetchone()
print type(cursor.fetchone())
#for row in cursor.execute("select * from user"):
    #print type(row)
    #print row

#for item in cursor.fetchone():
    #print type(item)
    #print item

#for row in cursor.execute("select rowid, * from person"):
    #print row
#print cursor.fetchall()

#cursor.execute("drop table person")


conn.commit()
cursor.close()
conn.close()
