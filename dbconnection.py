#!/usr/bin/env python3

"""This module contains the connection to the database.

"""

import sqlite3

conn = sqlite3.connect('database/password_manager.db')
c = conn.cursor()
