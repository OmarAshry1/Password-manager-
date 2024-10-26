from cryptography.fernet import Fernet
import os


def write_key():

    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        print("New encryption key generated.")
    else:
        print("Using existing encryption key.")


def load_key():

    write_key()

    with open("key.key", "rb") as file:
        key = file.read()
    return key


def view():
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                if not data:
                    continue
                if '|' not in data:
                    continue
                try:
                    app, user, passw = data.split('|')
                    decrypted_pass = fer.decrypt(passw.encode()).decode()
                    print("App:", app, " [ Username:", user, ", Password:", decrypted_pass, "]")
                except:
                    continue
    except FileNotFoundError:
        print("No passwords file found.")


def add():
    app = input("Enter Application Name: ")
    username = input("Enter your Username/Email: ")
    password = input("Enter your password: ")

    with open('passwords.txt', 'a') as f:
        f.write(app + "|" + username + "|" + fer.encrypt(password.encode()).decode() + "\n")


def edit():
    app = input("Enter Application Name to Search: ")
    username = input("Enter your Username/Email to search: ")

    with open('passwords.txt', 'r') as f:
        lines = f.readlines()

    found = False

    with open('passwords.txt', 'w') as f:
        for line in lines:
            data = line.rstrip()
            c_app, c_user, c_passw = data.split('|')

            if c_app.lower() == app.lower() and c_user.lower() == username.lower():
                found = True
                edd = input("Which do you want to edit (username/password/both)? ").lower()
                while edd not in ['username', 'password', 'both']:
                    edd = input("Try Again (username/password/both): ").lower()

                if edd == 'username':
                    newusername = input("Enter your new username: ")
                    f.write(f"{c_app}|{newusername}|{c_passw}\n")
                    print("Username updated successfully!")
                elif edd == 'password':
                    newpassword = input("Enter your new password: ")
                    encrypted_password = fer.encrypt(newpassword.encode()).decode()
                    f.write(f"{c_app}|{c_user}|{encrypted_password}\n")
                    print("Password updated successfully!")
                else:
                    newusername = input("Enter your new username: ")
                    newpassword = input("Enter your new password: ")
                    encrypted_password = fer.encrypt(newpassword.encode()).decode()
                    f.write(f"{c_app}|{newusername}|{encrypted_password}\n")
                    print("Both updated successfully!")
            else:
                f.write(line)
    if not found:
        print("No account match")



mpwd = input("Enter your master password: ")
key = load_key() + mpwd.encode()
fer = Fernet(key)


while mpwd == "Ashry":
    mode = input("Enter your mode: ")
    if mode.lower() == "view":
        view()
    elif mode.lower() == "edit":
        edit()
    elif mode.lower() == "add":
        add()
    elif mode.lower() == "q":
        print("Bye Bye")
        break
    else:
        print("Invalid mode")