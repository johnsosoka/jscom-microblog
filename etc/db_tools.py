import getpass
import os
from peewee import DoesNotExist
from termcolor import cprint
from werkzeug.security import check_password_hash, generate_password_hash
from entity.user import User

def list_users():
    users = User.select()
    for user in users:
        print(f'Username: {user.username}, Created: {user.created}, Last login: {user.last_login}')

def test_password():
    username = input('Enter username: ')
    try:
        user = User.get(User.username == username)
    except DoesNotExist:
        cprint('User does not exist', 'red')
        return
    password = getpass.getpass('Enter password: ')
    if check_password_hash(user.password, password):
        print('Password is correct')
    else:
        print('Password is incorrect')

def delete_user():
    username = input('Enter username to delete: ')
    try:
        user = User.get(User.username == username)
    except DoesNotExist:
        cprint('User does not exist', 'red')
        return
    user.delete_instance()
    print('User deleted')

def change_password():
    username = input('Enter username: ')
    try:
        user = User.get(User.username == username)
    except DoesNotExist:
        cprint('User does not exist', 'red')
        return
    new_password = getpass.getpass('Enter new password: ')
    user.password = generate_password_hash(new_password)
    user.save()
    print('Password updated')

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
        print('1. List users')
        print('2. Test password')
        print('3. Delete user')
        print('4. Change password')
        print('5. Exit')
        option = input('Select an option: ')
        if option == '1':
            list_users()
        elif option == '2':
            test_password()
        elif option == '3':
            delete_user()
        elif option == '4':
            change_password()
        elif option == '5':
            break
        else:
            print('Invalid option')

if __name__ == '__main__':
    main()
