"""
holds methods to encrypt and decrypt files.
encryption: aes_crypt(<String>password, <String>file_name)
            returns: <String>salt(hard-coded as 'wombat'), <bytes>cryptographic key(from password), <bytes>encoded(encoded file)

decryption: aes_decrypt(<bytes>key, <bytes>file_input(encrypted bytestring)  )
            returns:<String>decrypted_string

password hashing: make_hash(<String>password)
                  returns:<bytes>pass_key(hashed password, with hardcoded salt 'wombat')


"""
import pbkdf2
from Crypto.Cipher import AES
import base64
import os
from Crypto.Hash import SHA256 as SHA
import re
import pkcs7
import sys

def make_hash(password):
    salt = "wombat"
    pass_key = pbkdf2.PBKDF2(password, salt, 500, SHA).read(32)
    print("key is",sys.getsizeof(pass_key),"long")
    #print(key)
    return pass_key

def aes_crypt(password, file_name):
    salt = "wombat"

    padder = pkcs7.PKCS7Encoder()
    crypt_key = pbkdf2.PBKDF2(password, salt, 1000, SHA).read(32)
    print("key is ",sys.getsizeof(crypt_key),"long")
    cipher = AES.new(crypt_key)
    file_input = open(file_name)
    file_input = file_input.read()
    print("input file is{\n",file_input,"}")
    #print("padding needed for file is: ", len(file_input) % 16)
    pad_str = padder.encode(file_input)
    encoded = cipher.encrypt(pad_str)
    #print(pad_str)

    return salt, crypt_key, encoded

def aes_decrypt(key, file_input):
    cipher = AES.new(key)
    decoded = cipher.decrypt(file_input).decode()
    padder = pkcs7.PKCS7Encoder()
    decrypted_string = padder.decode(decoded)
    return decrypted_string
