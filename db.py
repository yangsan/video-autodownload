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
        cursor.execute("select rowid, * from showlist")
    except sqlite3.OperationalError:
        createShowListTable(cursor)
        cursor.execute("select rowid, * from showlist")

    show_list = cursor.fetchall()
    _closeDatabase(conn, cursor)
    return show_list


def addNewRowInShowTable(show_name, url, show_table_name):
    """
    add a new show into the show table
    """
    conn, cursor = _connectDatabase()

    if not tableExist("showlist"):
        createShowListTable(cursor)

    row_exits = cursor.execute("""
                   select * from showlist
                   where showname = ?
                   """, (show_name,)).fetchone()

    if not row_exits:
        cursor.execute("""
                        insert into showlist
                        (showname, url, tablename)
                        values
                        (?, ?, ?)
                        """,
                        (show_name, url, show_table_name))
        _closeDatabase(conn, cursor)
        return 1
    else:
        _closeDatabase(conn, cursor)
        return 0


def createShowListTable(cursor):
    cursor.execute("""
                create table showlist
                (
                showname text,
                url text,
                tablename text
                )
                """)


def getFromShowList(something, show_name):
    conn, cursor = _connectDatabase()
    something = cursor.execute("""
                   select %s from showlist
                   where showname = ?
                   """ % (something), (show_name))

    _closeDatabase(conn, cursor)
    return something


def createEpListTable(show_table_name):
    conn, cursor = _connectDatabase()
    if not tableExist(show_table_name):
        cursor.execute("""
                    create table %s
                    (
                    epname text,
                    magnet text,
                    status int
                    )
                    """ % (show_table_name))
        _closeDatabase(conn, cursor)
        return 1
    else:
        _closeDatabase(conn, cursor)
        return 0


def addNewEp(show_table_name, ep_name, magnet, status):
    conn, cursor = _connectDatabase()
    if not ifIn(ep_name, show_table_name):
        cursor.execute("""
                    insert into %s
                    (epname, magnet, status)
                    values
                    (?, ?, ?)
                    """ % (show_table_name), (ep_name, magnet, status))
        _closeDatabase(conn, cursor)
        return 1
    else:
        _closeDatabase(conn, cursor)
        return 0


def deleteEpList(show_table_name):
    conn, cursor = _connectDatabase()
    print show_table_name

    if tableExist(show_table_name):
        cursor.execute("""
                    drop table %s
                    """ % (show_table_name))

    _closeDatabase(conn, cursor)


def deleteShowListRow(show_id):
    conn, cursor = _connectDatabase()

    cursor.execute("""
                   delete from showlist
                   where rowid = ?
                   """, (show_id,))

    _closeDatabase(conn, cursor)


def ifIn(name, table_name):
    conn, cursor = _connectDatabase()

    cursor.execute("""
                   select * from %s
                   where epname = ?
                   """ % (table_name), (name,))
    if cursor.fetchone():
        _closeDatabase(conn, cursor)
        return True
    else:
        _closeDatabase(conn, cursor)
        return False


def getUndoneEpList(table_name):
    conn, cursor = _connectDatabase()
    cursor.execute("""
                   select * from %s
                   where status = 0
                   """ % (table_name))
    undone_list = cursor.fetchall()

    _closeDatabase(conn, cursor)
    return undone_list


def changeStatus(table_name, ep_name):
    conn, cursor = _connectDatabase()
    cursor.execute("""
                   update %s
                   set status=1
                   where epname = ?
                   """ % (table_name), (ep_name,))

    _closeDatabase(conn, cursor)


def tableExist(table_name):
    conn, cursor = _connectDatabase()
    tb_exits = "select name from sqlite_master where type='table' and name = \'%s\'" % (table_name)

    if cursor.execute(tb_exits).fetchone():
        _closeDatabase(conn, cursor)
        return True
    else:
        _closeDatabase(conn, cursor)
        return False
