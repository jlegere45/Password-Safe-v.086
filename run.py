import safe

safe.usage()
def run():
    command = ''
    while command != 'q':
        command = raw_input("Enter in command: ")
        command.lower()
        if command == 'h':
            safe.usage()
        if command == 'a':
            safe.addAccount()
        if command == 'd':
            safe.deleteAccount()
        if command == 's':
            safe.showUsernames()
        if command == 'c':
            safe.copyToClip()
        if command == 'r':
            safe.showPassword()
run()
        
