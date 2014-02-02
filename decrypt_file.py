import dead_wombat
crypt_key = dead_wombat.make_aes_key("secretkey")

encrypted_file = open('server/files/admin/test.txt', 'r')
file_input = encrypted_file.read().encode()
print("encrypted_file is :\n",file_input)
print("size of file is:",len(file_input))

decoded_file = dead_wombat.aes_decrypt_key(crypt_key, file_input)
print("decoded file is {\n",decoded_file,"\n}")
file_save = open('test_output.txt', 'w')
file_save.write(decoded_file)
file_save.close()
