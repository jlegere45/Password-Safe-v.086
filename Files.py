from Crypto.Cipher import AES
import os
import base64
"""
This is the class contains the methods from encrypting and decrypting
the file containing the keys. I seperated each value with two ',' because occassionaly the encryption would contain one , I will update the code to export to json files in the future
"""
class KeyFile:
    def __init__(self, path, masterKey):
        self.path = path
        self.masterKey = masterKey 
   
    def encryptFile(self):
	#This function is never used but may be in later versions
        f = open(self.path, 'r')
        text = f.read()
        contents = text.split(',,')
        print contents
        f.close()
        f = open(self.path, 'w')
        f.write('%s,,' % self.iv)
        for i in range (len(contents)):
            encryptor = AES.new(self.masterKey, AES.MODE_CFB, self.iv)            
            f.write('%s,,' % encryptor.encrypt(contents[i]))
        f.close()

    def encryptKey(self, key):
	#Encrypts the key for a login object
        f = open(self.path, 'a')
        try:
            encryptor = AES.new(self.masterKey, AES.MODE_CFB, self.getIV())
            f.write('%s,,' % encryptor.encrypt(key))
        except:
            #Generate iv for first time
            iv = base64.b64encode(os.urandom(10))
            encryptor = AES.new(self.masterKey, AES.MODE_CFB, iv)
            f.write('%s,,' % iv)
            f.write('%s,,' % encryptor.encrypt(key)) 
        f.close()

    def encryptIV(self, iv):
	#Encrypts the iv for a login object
        f = open(self.path, 'a')
        encryptor = AES.new(self.masterKey, AES.MODE_CFB, self.getIV())
        f.write('%s,,' % encryptor.encrypt(iv))
        f.close()

    def decryptFile(self):
	#This function is also never used but may be in later verisons 
        iv = self.getIV()
        f = open(self.path, 'r')
        text = f.read()
        contents = text.split(',,')
        del contents[0]
        f.close()
        f = open(self.path, 'w')
        print contents
        for i in range (len(contents)):
            decryptor = AES.new(self.masterKey, AES.MODE_CFB, iv)            
            f.write('%s,,' % decryptor.decrypt(contents[i]))
        f.close()

    def decryptKey(self, index):
	#decryptes key and returns it based on the program specified index
        f = open(self.path, 'r')
        text = f.read()
        contents = text.split(',,')
        del contents[0]
        contents[index]
        decryptor = AES.new(self.masterKey, AES.MODE_CFB, self.getIV())
        key = decryptor.decrypt(contents[index])
        f.close()
        return key

    def decryptIV(self, index):
	#returns the decrypted iv
        f = open(self.path, 'r')
        text = f.read()
        contents = text.split(',,')
        del contents[0]
        decryptor = AES.new(self.masterKey, AES.MODE_CFB, self.getIV())
        iv = decryptor.decrypt(contents[index])
        f.close()
        return iv

    def getIV(self):
	#Returns the iv for this encryption
        f = open(self.path, 'r')
        iv = f.read(16)
        return iv
        
