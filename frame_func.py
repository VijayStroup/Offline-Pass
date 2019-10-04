#!/usr/bin/env python3

"""This module contains the functionality of the frames from frames.py

"""

import dbqueries as dbq
from encrypt import Encrypt, hashIt, hashCmp
import sqlite3

# Universal functions
def passwordRules(password):
    """Some master password required rules."""

    rules = [
            lambda password: any(x.isupper() for x in password),
            lambda password: any(x.islower() for x in password),
            lambda password: any(x.isdigit() for x in password),
            lambda password: len(password) >= 6 and len(password) <= 20,
            lambda password: not any(x.isspace() for x in password)
        ]

    return all(rule(password) for rule in rules)

# Setup functions
def pushSignup(password, question, answer):
    """Hash and encrypt all data and send to database."""

    encryptObj = Encrypt()
    if passwordRules(password) and answer != '':
        password = hashIt(password)
        question = encryptObj.encrypt(question)
        answer = encryptObj.encrypt(answer)
        key = dbq.selectKey()[0]

        dbq.updateMasterInfo(password[0], password[1], question, answer)

        return True
    else:
        return False

# Login functions
def loginCmp(password):
    """Hash password input and compare to database password."""

    return True if hashCmp(password) else False

# Reset password functions
def getSecQ():
    """Get security question to display in gui."""

    return Encrypt().decrypt(dbq.selectSecQ())

def secCmp(answer):
    """Compare security question answer against database answer."""

    if Encrypt().secQCmp(answer):
        return True
    else:
        return False

def pushReset(password):
    """If password requirements met, hash password and update database."""

    if passwordRules(password):
        password = hashIt(password)
        dbq.updateMasterPass(password[0], password[1])

        return True
    else:
        return False

# Home functions
def pushEntry(web, user, passwd):
    """Encrypt data and send to database."""

    encryptObj = Encrypt()
    if web != '':
        web = encryptObj.encrypt(web)
        user = encryptObj.encrypt(user)
        passwd = encryptObj.encrypt(passwd)

        dbq.addEntry(web, user, passwd)

        return True
    else:
        return False

# Treeview functions
def getEntries():
    """Get rows of encrypted data and decrypted data for gui. The encrypted
    data is used in other functions for the gui buttons."""

    encryptObj = Encrypt()
    rows = dbq.selectEntries()

    decryptedRows = [[] for i in range(len(rows))]
    i = 0
    for row in rows:
        web = encryptObj.decrypt(row[0])
        user = encryptObj.decrypt(row[1])
        passwd = encryptObj.decrypt(row[2])
        decryptedRows[i].extend((web, user, passwd))
        i += 1

    return (decryptedRows, rows)

def editEntry(ow, ou, op, nw, nu, np):
    """Update database with new data for specific entry."""

    encryptObj = Encrypt()
    nw = encryptObj.encrypt(nw)
    nu = encryptObj.encrypt(nu)
    np = encryptObj.encrypt(np)

    dbq.updateEntry(ow, ou, op, nw, nu, np)

def removeEntry(website, username, password):
    """Delete entry from database."""

    dbq.deleteEntry(website, username, password)

def removeMultiEntry(items, oldInfo):
    """Delete multiple entries from database."""

    i = 0
    for item in items:
        info = oldInfo[i]
        website = info[0]
        username = info[1]
        password = info[2]

        dbq.deleteEntry(website, username, password)
        i += 1
