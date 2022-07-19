from base64 import b64encode
import re
import json
import hashlib
import os

class Account:
    def __init__(self, name: str, email: str, password: str, id: int, age: int):
        self.name = name
        self.email = email
        self.password = password
        self.id = id
        self.age = age

class Login:
    def __init__(self, action: str) -> None:
        """
        @action: Entweder `login` oder `registrierung`
        """
        print(action)
        if action.lower() == "registrieren" or action == "r":
            try:
                self.register()
            except ValueError: # Oh EMail existiert schon
                print("Die E-Mail ist schon vergeben.")
            except BaseException: # Oh EMail ist nicht valide
                print("Eingegebene E-Mail ist keine gültige E-Mail.")
        elif action.lower() == "einloggen" or action == "l":
                print(self.login())
        else:
            return "ungültig"

    def get_hashed_password(password: str, salt: str):
        return hashlib.sha1((password + salt).encode('utf-8')).hexdigest()

    def login(self):
        email = input(("E-Mail: "))
        pw = input(("Password: "))
        return self.check_login(email, pw)


    def check_login(self, email, password):
        with open("account.txt", "r", encoding="utf-8") as file:
            for content in file:
                accontdata = content.split(", ")
                salt = accontdata[4]
                if email == accontdata[1] and self.get_hashed_password(password, salt) == accontdata[2]:
                    return True
            return False

    def register(self):
        email = input("Bitte gebe deine E-Mail an: ")
        if not self.is_valid_email(email):
            raise BaseException("EMail nicht valide")
        if self.is_user_registered(email):
            raise ValueError("EMail schon vergeben")

        info_name = input("Name: ")
        info_password = input("Password: ")
        info_age = input("Age: ")

        self.save_user(email, info_name, info_password, info_age)

    def save_user(self, emailAddress: str, info_name: str, info_password: str, info_age: int):
        with open("account.txt", "a", encoding="utf-8") as file:
            salt = b64encode(os.urandom(16))
            file.write(", ".join([info_name, emailAddress, self.get_hashed_password(info_password, salt), info_age, salt, '\n']))
        
        """
        Nutzer wird mit EMail-Addresse registriert
        @emailaddress: E-Mail Adresse des zu registrierenden Nutzers
        """
    
    
    def is_user_registered(self, emailAddress: str):
        with open("account.txt", "r", encoding="utf-8") as userfile:
            # Überspringe erste Zeile in der Textdatei
            users = userfile.readlines()
            if len(users) > 0:
                users.pop(0)
            
            for user in users:
                """
                user.split()[1] entspricht der gespeicherten Emailadresse der aktuellen Zeile
                """
                accountData = user.split(", ")
                if len(accountData) != 4:
                    continue

                if emailAddress == accountData[1]:
                    return True
        return False
    
    def is_valid_email(self, emailAddress: str):
        valid_email_regex = "^[a-zA-Z0-9\-\_\.]+\@[a-zA-Z0-9\-\_\.]+$"
        match = re.search(valid_email_regex, emailAddress)
        if match is None:
            return False
        return True


class LoginJSON(Login):
    def __init__(self, action: str) -> None:
        super().__init__(action)

    def check_login(self, email: str, password: str):
        users = None

        with open('account.json', 'r', encoding='utf-8') as file:
            users = json.loads(file.read())

        for user in users['users']:
            if user['email'] == email and user['password'] == self.get_hashed_password(password, user['salt']):
                return True
        return False

    def save_user(self, emailAddress: str, info_name: str, info_password: str, info_age: int):
        users = None
        with open('account.json', 'r', encoding="utf-8") as file:
            users = json.loads(file.read())

        salt = b64encode(os.urandom(16))

        users["users"].append({
            'name': info_name,
            'email': emailAddress,
            'password': self.get_hashed_password(info_password, salt),
            'age': info_age,
            'salt': salt
        })

        with open('account.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(users))

    def is_user_registered(self, emailAddress: str):
        users = None
        with open('account.json', 'r', encoding="utf-8") as file:
            users = json.loads(file.read())
        
        for user in users['users']:
            if user['email'] == emailAddress:
                return True
        return False


# tim = Login(input("Registrieren(r) oder einloggen?(l) "))
jsonLogin = LoginJSON(input("Registrieren(r) oder einloggen?(l) "))
