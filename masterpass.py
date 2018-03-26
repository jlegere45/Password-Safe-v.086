import bcrypt
import getpass
import hashlib

pwPath = os.path.expanduser('~' + '/.mpassword/')

def storePassword():
    password = getpass.getpass('Enter in the Master Key: ')
    check = getpass.getpass('Enter in Master Key again: ') 
    while check != password:
        check = getpass.getpass('Incorrect entry. Please type in the Master Key: ')
    print('It is recommend that the user stores a written copy of their Master Key somewhere safe.')
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(check, salt)
    with open(pwPATH, 'w') as masterPath:
        masterPath.write('%s,,' % salt)
        masterPath.write('%s,,' % password)
def checkPassword():
    with open(pwPATH, 'r') as masterPath:
        text = masterPath.read()
        contents = text.split(',,')
        salt = contents[0]
        password = contents[1]
        check = getpass.getpass('Enter in Master Key: ')
	attempt = check
        check = bcrypt.hashpw(check, salt)
        counter = 0
        while check != password:
            check = getpass.getpass('Incorrect entry. Please type in the Master Key: ')
            check.join(salt)
            check = bcrypt.hashpw(check, salt)
            counter += 1
            if counter == 4:
                print('Too many attempts, exiting program.')
                quit()
        print('Correct password, use of Password Safe granted.')
        return check
