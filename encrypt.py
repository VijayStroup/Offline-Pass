#!/usr/bin/env python3

"""This module contains hashing and encrypting methods.

"""

from binascii import hexlify
from cryptography.fernet import Fernet
import dbconnection as db
import dbqueries as dbq
from hashlib import pbkdf2_hmac
from os import urandom

def hashIt(val):
    """Hash password with salt and 500 iterations."""

    salt = urandom(20)
    salt = hexlify(salt)
    hashPw = pbkdf2_hmac(
        'sha256', 
        bytes(val, encoding='utf-8'), 
        salt, 
        500_000
    )
    hashPw = hexlify(hashPw)
    return (hashPw, salt)

def hashCmp(val):
    """Hash passed in password, and compare with hash in database."""


    mInfo = dbq.selectLoginInfo()
    salt = mInfo[1]
    hashPw = pbkdf2_hmac(
        'sha256', 
        bytes(val, encoding='utf-8'), 
        salt, 
        500_000
    )
    hashPw = hexlify(hashPw)

    return mInfo[0] == hashPw

class Encrypt:
    """Methods for encrypting, decrypting, and comparing encrypted values."""

    def __init__(self):
        """Encryption key instance used for encryption and decryption."""

        self.key = dbq.selectKey()
        self.key = Fernet(self.key)

    def encrypt(self, val):
        """Encrypt value. - encoding: utf-8"""
        return self.key.encrypt(bytes(val, encoding='utf-8'))

    def decrypt(self, val):
        """Decrypt value. - encoding: utf-8"""
        plain = self.key.decrypt(val)

        return plain.decode('utf-8')

    def secQCmp(self, val):
        """Decrypt database security answer and compare with plain text entry
        in gui."""
        secA = dbq.selectSecA()
        secA = self.decrypt(secA)

        return val == secA
