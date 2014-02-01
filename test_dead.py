import dead_wombat
import base64


salt, crypt_vector, file_output = dead_wombat.aes_crypt("dickbutt", 'test.txt')
print("key is ",crypt_vector)
#print("encrypted file is ",file_output)
print("salt is ", salt)

decoded_file = dead_wombat.aes_decrypt(crypt_vector, file_output)
print("decoded file is {\n",decoded_file,"\n}")
file_save = open('test_output.txt', 'w')
file_save.write(decoded_file)
file_save.close()
