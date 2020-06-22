# -*- coding: utf-8 -*-


import src.caesar
import pyperclip
from colorama import Fore, init
from os import name, system
from src.manage import SQLManage


if name == 'nt':
    init()

if name == 'nt':
    path = 'src//db.db'
else:
    path = 'src/db.db'

db = SQLManage(path)


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')
    print(Fore.GREEN + '\t\tPASSWORD +\n\n')


def login():
    while True:
        password = input(Fore.YELLOW + 'Enter Password: ')
        if password == db.check_password():
            clear()
            break
        else:
            print(Fore.RED + "Wrong Password!")
    return

def reg():
    while True:
        password = input(Fore.YELLOW + "Enter a New Password: ")
        retype = input(Fore.YELLOW + "Confirm New Password: ")
        if retype == password:
            print(Fore.GREEN + "Success!")
            db.add_password(password)
            break
        else:
            print(Fore.RED + "Password mismatch!")
    return


def main():
    global login
    clear()
    if db.check_password():
        login()
    else:
        reg()
        clear()
        login()
    
    help_message = Fore.YELLOW + '''
    help - help message
    add - add new password
    get *name* - get password by name
    get_all - get all names
    delete *name* - delete password by name
    delete_all - delete all passwords
    update - update login password
    clear - clear terminal
    exit - exit from program
    '''
    print(Fore.CYAN + '\tPassword Manager in Terminal' +
          Fore.YELLOW + '\n\t (type \"help\" - for help message)\n\n')
    while True:
        command = input(Fore.YELLOW + '\n-->: ')
        if command.strip() == 'help':
            clear()
            print(help_message)
        elif command.strip() == 'add':
            clear()
            name = input(Fore.YELLOW + "Enter Name: ")
            login = input(Fore.YELLOW + "Enter Login: ")
            password = input(Fore.YELLOW + "Enter Password: ")
            if db.check_name(name):
                db.add_data(name, login, password)
                clear()
                print(Fore.GREEN + "Success!\nNew password added!")
            else:
                print(Fore.RED + f'\nERROR!\nThe name "{name}" is already in use!')
        elif command.startswith('get '):
            name = command.split('get ')[1]
            if not db.check_name(name):
                data = db.get_byname(name)[0]
                print(Fore.GREEN + f'\nName: {data[0]}\nLogin: {data[1]}\nPassword: {src.caesar.decrypt(data[2], 3)} ')
                pyperclip.copy(f"{data[1]}:{src.caesar.decrypt(data[2], 3)}")
                print(Fore.GREEN + f"login:password Copied to the Clipboard!")
            else:
                print(Fore.RED + f'\nERROR!\nThere is no such {name}!')
        elif command == 'get_all':
            names_list = db.get_all()
            names = ''
            for n in names_list:
                names += n[0] + ', '
            names = names[:-2]
            clear()
            if names == '':
                print(Fore.RED + 'You Have No Saved Passwords!')
            else:
                print(Fore.GREEN + names)
        elif command == 'clear':
            clear()
        elif command == 'update':
            clear()
            while True:
                password = input(Fore.YELLOW + "Enter a New Password: ")
                retype = input(Fore.YELLOW + "Confirm New Password: ")
                if retype == password:
                    print(Fore.GREEN + "Success!")
                    db.update_password(password)
                    break
                else:
                    print(Fore.RED + "Password mismatch!")
        elif command.startswith('delete '):
            name = command.split('delete ')[1]
            if not db.check_name(name):
                clear()
                sure = input(Fore.YELLOW +
                             f'Are You Sure You Want to Delete {name}? (Y / n): ')
                if sure.lower() == 'y':
                    db.delete_data(name)
                    print(Fore.GREEN + f"\n{name} Successfully Deleted!\n")
                else:
                    print(Fore.YELLOW + 'OK, Deletion Canceled.')
            else:
                print(Fore.RED + f'\nERROR!\nThere is no such {name}!')
        elif command.strip() == 'delete_all':
            clear()
            sure = input(Fore.YELLOW + f'Are You Sure You Want to Delete All? (Y / n): ')
            if sure.lower() == 'y':
                db.delete_all()
                print(Fore.GREEN + "\nAll Successfully Deleted!")
            else:
                print(Fore.YELLOW + 'OK, Deletion Canceled.')
        elif command == 'exit':
            print(Fore.YELLOW + "Exit...")
            print(Fore.WHITE)
            break
        else:
            print(Fore.RED + "Sorry... Im not Understand You...\nType \"help\" for help message.")



if __name__ == '__main__':
    main()
    exit(1)

