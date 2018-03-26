from Crypto.Cipher import AES
import hashlib
import os
import datetime
import base64
import pyperclip
import masterpass
from Files import KeyFile
from getpass import getpass
from loginClass import login

"""
A password safe manager. This is a each password is encrypted with a unique key that is also encrypted with the master key. 
"""
accounts = list();

mainPath = os.path.expanduser('~' + '/.password/')
if not os.path.exists(mainPath):
    os.mkdir(mainPath)
    masterPass.storePassword()
accountFile = mainPath + '.passwords'
keyFile = mainPath + '.keys'
keys = KeyFile(keyFile, hashlib.sha256(masterpass.checkPassword()).digest())

def usage():
    #Show commands
    print("Password Safe")
    print("Each password is stored with a username associated with it")
    print("\n-a --add account")
    print("-d --delete password")
    print("-c --copy password to clipboard")
    print("-r --password on console")
    print("-s --show every username")
    print("-h --show list of commands")
    print("-q --quit program")
    
def genKey():
    #Generates each key for each password
    return base64.b64encode(os.urandom(32))
def addAccount():
    global keys
    username = raw_input("Enter in username: ")
    password = getpass("Enter in your password: ")
    key = genKey()
    i = 0
    check = ""
    while check != password and i < 4:
        check = getpass("Type in password again: ")
	i += 1
        if check == password:
            break
        else:
            continue
    if i == 4:
	print("Too many incorrect attempts")
	return None
    #create temp account to be added into accounts
    temp = login(password, username, key, '')
    temp.encrypt()
    global accounts
    accounts.append(temp)
    writeToFiles()
    print('Account added!')
def writeToFiles():
    pwFile = open(accountFile, 'a')
    for i in range(len(accounts)):
        pwFile.write("%s,,%s,," % (accounts[i].get_password(),accounts[i].get_username()))
        keys.encryptKey(accounts[i].get_key())
        keys.encryptIV(accounts[i].get_iv())
    pwFile.close()
    accounts[:] = []
def showPassword():
    #Shows the password
    username = raw_input("Enter in username: ")
    with open(accountFile, 'r') as passwordFile:
        text = passwordFile.read()
        contents = text.split(',,')
        i = 0
        while contents[i] != username and i < (len(contents)-1):
            i += 1
        if contents[i] == username:
            iv = keys.decryptIV(i)
            key = keys.decryptKey(i-1)
            temp = login(contents[i-1], contents[i], key, iv)
            print('Username: %s Password: %s' %(temp.get_username(), temp.decrypt(key, iv)))
        else:
            print('Username not found')      
def copyToClip():
    #Copies password to clipboard
    username = raw_input("Enter in username: ")
    with open(accountFile, 'r') as passwordFile:
        text = passwordFile.read()
        contents = text.split(',,')
        i = 0
        while contents[i] != username and i < (len(contents)-1):
            i += 1
        if contents[i] == username:
            iv = keys.decryptIV(i)
            key = keys.decryptKey(i-1)
            temp = login(contents[i-1], contents[i], key, iv)
            pyperclip.copy(temp.decrypt(key, iv))
            print('Password copied!')
        else:
            print('Username not found')       
def showUsernames():
    #Shows all the usernames
    with open(accountFile, 'r') as passwordFile:
        text = passwordFile.read()
        contents = text.split(',,')
        print "Usernames: "
        i = 1
        while i < (len(contents)):
            print contents[i]
            i += 2
def deleteAccount():
    #removes account from the passsword safe
    username = raw_input("Enter in username: ")    
    i = 0
    contents = []
    keyContents = []
    with open(accountFile, 'r') as passwordFile:
        text = passwordFile.read()
        contents = text.split(',,')
    with open(keyFile, 'r') as keyIV:
        text = keyIV.read()
        keyContents = text.split(',,')
    while contents[i] != username and i < (len(contents)-1):
        i += 1
    if contents[i] == username:
        del contents[i]
        del contents[i-1]
        del contents[(len(contents)-1)]
        del keyContents[i+1]
        del keyContents[i]
        del keyContents[(len(keyContents)-1)]
        with open(accountFile, 'w') as passwordFile:
            for j in range (len(contents)):
                passwordFile.write('%s,,' % contents[j])
        with open(keyFile, 'w') as keyIV:
            for j in range (len(keyContents)):
                keyIV.write('%s,,' % keyContents[j])
        print('Account deleted!')
    else:
        print('Username not found')
