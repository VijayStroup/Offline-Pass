#!/usr/bin/env python3

"""This module contains sql transactions.

"""

import dbconnection as db

# Select Statements
def selectSecQ():
    db.c.execute("SELECT question FROM master")
    return db.c.fetchone()[0]

def selectSecA():
    db.c.execute("SELECT answer FROM master")
    return db.c.fetchone()[0]

def selectLoginInfo():
    db.c.execute("SELECT password, salt FROM master")
    return db.c.fetchone()

def selectKey():
    db.c.execute("SELECT key FROM master")
    return db.c.fetchone()[0]

def selectEntries():
    db.c.execute("SELECT * FROM entries")
    return db.c.fetchall()

# Insert Statements
def addEntry(website, username, password):
    sql_statement = (
        'INSERT INTO entries (website, username, password) '
        'VALUES (?, ?, ?)'
    )
    bind_statement = (website, username, password)

    db.c.execute(sql_statement, bind_statement)
    db.conn.commit()

# Update Statements
def updateMasterPass(password, salt):
    db.c.execute("UPDATE master SET password = ?, salt = ?", (password, salt))
    db.conn.commit()

def updateMasterInfo(password, salt, question, answer):
    sql_statement = (
        'UPDATE master '
        'SET password = ?, salt = ?, question = ?, answer = ?'
    )
    bind_statement = (password, salt, question, answer)

    db.c.execute(sql_statement, bind_statement)
    db.conn.commit()

def updateEntry(ow, ou, op, nw, nu, np):
    sql_statement = (
        'UPDATE entries SET '
        'website = ?, username = ?, password = ? '
        'WHERE website = ? and username = ? and password = ?'
    )
    bind_statement = (nw, nu, np, ow, ou, op)

    db.c.execute(sql_statement, bind_statement)
    db.conn.commit()

# Delete Statements
def deleteEntry(website, username, password):
    sql_statement = (
        'DELETE FROM entries WHERE '
        'website = ? AND username = ? AND password = ?'
    )
    bind_statement = (website, username, password)

    db.c.execute(sql_statement, bind_statement)
    db.conn.commit()
