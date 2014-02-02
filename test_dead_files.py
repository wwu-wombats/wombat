import dead_wombat
import base64

password = "secretkey"
salt, crypt_key, file_output = dead_wombat.aes_crypt(password, 'test.txt')
print("password is",password)
print("hashed password(server password) is:",dead_wombat.make_hash(password))
print("salt is", salt)
print("key is",crypt_key)
#print("encrypted file is ",file_output)
encrypted_file = open('encrypted_output', 'wb')
encrypted_file.write(file_output)
encrypted_file.close()


encrypt_file = open('encrypted_output', 'rb')
file_input = encrypt_file.read()
print("encrypted file is :\n",file_input)

decoded_file = dead_wombat.aes_decrypt(crypt_key, file_input)
print("decoded file is {\n",decoded_file,"\n}")
file_save = open('test_output.txt', 'w')
file_save.write(decoded_file)
file_save.close()
