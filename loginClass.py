from Crypto.Cipher import AES
import hashlib
import os
import base64
import random 

class login:
    
    def __init__(self, password, username, key, iv):
        self.password = password
        self.username = username
        self.key = key
        self.iv = iv
    
    #Setters
    def set_password(self, password):
        self.password = password
    def set_username(self, username):
        self.username = username
 #   def set_url(self, url):
 #       self.url = url
    def set_key(self, key):
        self.key = key
        
    #Getters
    def get_password(self):
        return self.password
    def get_username(self):
        return self.username
 #   def get_url(self):
 #       return self.url
    def get_key(self):
        return self.key
    def get_iv(self):
        return self.iv
    
    #generate iv
    def genIV(self):
        self.iv = base64.b64encode(os.urandom(10))
        return self.iv
    #encrypt password
    def encrypt(self):
        self.iv = self.genIV()
        encryptor = AES.new(hashlib.sha256(self.key).digest(), AES.MODE_CFB, self.iv)
        self.password = encryptor.encrypt(self.password)
    #decrypt password
    def decrypt(self, key, iv):
        if (self.key == key and self.iv == iv):
            decryptor = AES.new(hashlib.sha256(self.key).digest(), AES.MODE_CFB, self.iv)
            return decryptor.decrypt(self.password)
        else:
            return ("Unsuccessful decryption")