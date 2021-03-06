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


def addNewRowInShowTable(show_name, url, show_table_name, status_code):
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
                        (showname, url, tablename, status)
                        values
                        (?, ?, ?, ?)
                        """,
                        (show_name, url, show_table_name, status_code))
        _closeDatabase(conn, cursor)
        return 1
    else:
        _closeDatabase(conn, cursor)
        return 0


def createShowListTable(cursor):
    """
    status code
    0: download whatever
    1: will see
    """
    cursor.execute("""
                create table showlist
                (
                showname text,
                url text,
                tablename text,
                status int
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
    """
    status code
    0: not downloaded yet
    1: downloaded
    2: pending
    """
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


def getEpList(table_name):
    conn, cursor = _connectDatabase()

    cursor.execute("""
                   select * from %s
                   """ % table_name)

    table_list = cursor.fetchall()
    _closeDatabase(conn, cursor)
    return table_list


def deleteEpList(show_table_name):
    conn, cursor = _connectDatabase()

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


def getSpecificEpList(table_name, status):
    conn, cursor = _connectDatabase()

    cursor.execute("""
                   select * from %s
                   where status = ?
                   """ % (table_name), (status,))

    specific_list = cursor.fetchall()
    _closeDatabase(conn, cursor)
    return specific_list


def changeStatus(table_name, ep_name, status):
    conn, cursor = _connectDatabase()
    cursor.execute("""
                   update %s
                   set status= ?
                   where epname = ?
                   """ % (table_name), (status, ep_name))

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
