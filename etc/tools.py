import getpass
import os
from peewee import DoesNotExist
from termcolor import cprint
from werkzeug.security import check_password_hash, generate_password_hash
from entity.user import User
from base64 import b64encode


def list_users():
    """List users"""
    users = User.select()
    for user in users:
        print(f'Username: {user.username}, Created: {user.created}, Last login: {user.last_login}')


def test_password():
    """Test password"""
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
    """Delete user"""
    username = input('Enter username to delete: ')
    try:
        user = User.get(User.username == username)
    except DoesNotExist:
        cprint('User does not exist', 'red')
        return
    user.delete_instance()
    print('User deleted')


def change_password():
    """Change password"""
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


def base64_encode_password():
    """Encode password"""
    password = getpass.getpass('Enter password to encode: ')
    encoded_password = b64encode(password.encode()).decode()
    print(f'Encoded password: {encoded_password}')


def exit_program():
    """Exit"""
    print("Exiting.")
    exit()


def main():
    options = {
        '1': list_users,
        '2': test_password,
        '3': delete_user,
        '4': change_password,
        '5': base64_encode_password,
        '6': exit_program
    }

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
        for key, func in options.items():
            print(f"{key}. {func.__doc__}")
        option = input('Select an option: ')

        func = options.get(option)

        if func:
            func()
        else:
            print('Invalid option')


os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal

if __name__ == '__main__':
    main()
