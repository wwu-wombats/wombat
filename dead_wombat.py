"""
holds methods to encrypt and decrypt files.
encryption: aes_crypt_pwd(<String>password, <String>file_name)
            returns: <String>salt(hard-coded as 'wombat'), <bytes>cryptographic key(from password), <bytes>encoded(encrypted file)

            aes_crypt_key(<bytes>key, <String>file_name)
            returns: <bytes>encoded(encrypted file)

decryption: aes_decrypt_key(<bytes>key, <bytes>file_input(encrypted bytestring)  )
            returns:<String>decrypted_string

            aes_decrypt_pwd(<String>password, <bytes>file_input(encrypted bytestring) )
            returns:<String>decrypted_string

password hashing: make_hash(<String>password)
                  returns:<bytes>pass_key(hashed password, with hardcoded salt 'wombat')

encryption key generation: make_crypt_key(<String>password)
                           returns:<bytes>crypt_key(cryptographic key, with hard-coded salt 'wombat')


"""
import pbkdf2
from Crypto.Cipher import AES
import base64
import os
from Crypto.Hash import SHA as SHA
import re
import pkcs7
import sys

def make_hash(password):
    salt = "wombat"
    pass_key = pbkdf2.PBKDF2(password, salt, 500, SHA).read(32)
    print("key is",sys.getsizeof(pass_key),"long")
    #print(key)
    return pass_key

def aes_crypt_pwd(password, file_name):
    salt = "wombat"
    padder = pkcs7.PKCS7Encoder()
    crypt_key = make_aes_key
    print("key is ",sys.getsizeof(crypt_key),"long")
    cipher = AES.new(crypt_key)
    file_input = open(file_name)
    file_input = file_input.read()
    file_input.close()
    print("input file is{\n",file_input,"}")
    #print("padding needed for file is: ", len(file_input) % 16)
    pad_str = padder.encode(file_input)
    encoded = cipher.encrypt(pad_str)
    #print(pad_str)

    return salt, crypt_key, encoded

def aes_crypt_key(key, file_name):
    padder = pkcs7.PKCS7Encoder()
    cipher = AES.new(key)
    file_obj = open(file_name)
    file_input = file_obj.read()
    file_obj.close()
    pad_str = padder.encode(file_input)
    encoded = cipher.encrypt(pad_str)
    return encoded

def aes_decrypt_key(key, file_input):
    cipher = AES.new(key)
    padder = pkcs7.PKCS7Encoder()
    decoded = cipher.decrypt(file_input).decode()
    decrypted_string = padder.decode(decoded)
    return decrypted_string

def aes_decrypt_pwd(password, file_input):
    salt = "wombat"
    padder = pkcs7.PKCS7Encoder()
    crypt_key = make_aes_key(password)
    cipher = AES.new(key)
    decoded = cipher.decrypt(file_input).decode()
    decrypted_string = padder.decode(decoded)
    return decrypted_string


def make_aes_key(password):
    salt = "wombat"
    crypt_key = pbkdf2.PBKDF2(password, salt, 1000, SHA).read(32)
    return crypt_key
