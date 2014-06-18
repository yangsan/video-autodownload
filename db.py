# -*- coding: utf8 -*-
import sqlite3


def _connectDatabase():
    """
    Initialize or connect the database
    """
    conn = sqlite3.connect("showlist.db")
    cursor = conn.cursor()
    return conn, cursor


def _closeDatabase(conn, cursor):
    """
    Commit the change and close the cursor conn
    """
    conn.commit()
    cursor.close()
    conn.close()

def getShowList():
    """
    get show list from table showlist
    """
    conn, cursor = _connectDatabase()

    try:
        cursor.execute("select * from showlist")
    except sqlite3.Error, e:
        createShowListTable()
        cursor.execute("select * from showlist")

    show_list = cursor.fetchall()
    _closeDatabase(conn, cursor)
    return show_list

def addNewRowInShowTable(show_name, url, show_table_name):
    """
    add a new show into the show table
    """
    conn, cursor = _connectDatabase()

    #try:
    cursor.execute("""
                    insert into showlist
                    (showname, url, tablename)
                    values
                    (?, ?, ?)
                    """,
                    (show_name, url, show_table_name))

    #except sqlite3.OperationalError, e:
        #createShowListTable(cursor)
        #cursor.execute("""
                       #insert into showlist
                       #(showname, url, tablename)
                       #values
                       #(?, ?, ?)
                       #)
                       #""",
                       #(show_name, url, show_table_name))

    _closeDatabase(conn, cursor)



def createShowListTable(cursor):
    cursor.execute("""
                create table showlist
                (
                showname text,
                url text,
                tablename text
                )
                """)

def createEpListTable():
    pass

def deleteTable():
    pass

def deleteRow():
    pass

def getTableContent():
    pass


#try:
    #cursor.execute("select * from showlist")
#except StandardError, e:
    #print e, "\n try to create one."
    #cursor.execute("""
                   #create table showlist
                   #(
                   #showname text,
                   #url text,
                   #tablename text
                   #)
                   #""")
    #cursor.execute("select * from showlist")

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


#cursor.execute("select * from showlist")
#print cursor.fetchone()
#print type(cursor.fetchone())
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


