import dead_wombat
#this encrypts with the key "secretkey" not the crypto key generated from that
password = "secretkey"
crypt_key = dead_wombat.make_aes_key(password)
file_output = dead_wombat.aes_crypt_key(crypt_key, 'test.txt')
print("password is",password)
print("hashed password(server password) is:",dead_wombat.make_hash(password))
print("salt is wombat")
print("key is", dead_wombat.make_aes_key(password))
#print("encrypted file is ",file_output)
print("size of file is",len(file_output))
print("file is :",file_output)
encrypted_file = open('encrypted_output', 'wb')
encrypted_file.write(file_output)
encrypted_file.close()
