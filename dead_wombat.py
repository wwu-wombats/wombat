"""



"""
import pbkdf2
from Crypto.Cipher import AES
import base64
import os
from Crypto.Hash import SHA256 as SHA
import re
import pkcs7

def make_hash(password):
    salt = "wombat"
    key = pbkdf2.PBKDF2(password, salt, 500, SHA).read(32)
    #print(key)
    return salt

def aes_crypt(password, file_name):
    salt = "wombat"
    padder = pkcs7.PKCS7Encoder()
    key = pbkdf2.PBKDF2(password, salt, 1000, SHA).read(32)
    cipher = AES.new(key)
    file_input = open(file_name)
    file_input = file_input.read()
    print("input file is{\n ",file_input,"\n}")
    print("padding needed for file is: ", len(file_input) % 16)
    pad_str = padder.encode(file_input)
    encoded = cipher.encrypt(pad_str)
    print(pad_str)

    return salt, key, encoded

def aes_decrypt(key, file_input):
    cipher = AES.new(key)
    decoded = cipher.decrypt(file_input).decode()
    padder = pkcs7.PKCS7Encoder()
    return padder.decode(decoded)
