#!/usr/bin/env python3

"""____   __  __ _ _              _____              
  / __ \ / _|/ _| (_)            |  __ \             
 | |  | | |_| |_| |_ _ __   ___  | |__) |_ _ ___ ___ 
 | |  | |  _|  _| | | '_ \ / _ \ |  ___/ _` / __/ __|
 | |__| | | | | | | | | | |  __/ | |  | (_| \__ \__ \
  \____/|_| |_| |_|_|_| |_|\___| |_|   \__,_|___/___/

Author:     Vijay Stroup (https://vijaystroup.com)
Version:    1.0

"""

import dbconnection as db
from frames import Frames
from tkinter import Tk
import sqlite3
from os import getcwd

if __name__ == '__main__':
    cwd = getcwd()

    root = Tk()
    root.title('Offline Pass')
    root.geometry("+600+200")
    root.iconbitmap(cwd + '/imgs/favicon.ico')
    root.resizable(False, False)

    try:
        db.c.execute("SELECT password FROM master")
        result = db.c.fetchone()[0]
        if result == None:
            Frames(root, 'setup')
        else:
            Frames(root, 'login')
    except sqlite3.OperationalError:
        from cryptography.fernet import Fernet
        key = Fernet.generate_key()

        db.c.execute("""CREATE TABLE IF NOT EXISTS entries (
            website BLOB,
            username BLOB,
            password BLOB
        )""")
        db.c.execute("""CREATE TABLE IF NOT EXISTS master (
            password BLOB,
            salt BLOB,
            question BLOB,
            answer BLOB,
            key BLOB
        )""")
        sql_statement = (
        'INSERT INTO master (password, salt, question, answer, key) '
        'VALUES (?, ?, ?, ?, ?)'
        )
        bind_statement = (None, None, None, None, key)

        db.c.execute(sql_statement, bind_statement)
        db.conn.commit()

        Frames(root, 'setup')

    root.mainloop()

    db.conn.close()
