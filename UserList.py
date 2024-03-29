import json
import os
from base64 import b64encode, b64decode
from datetime import datetime

from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES

from User import User


# Пример использования
# text_to_encrypt = "Hello, World!"
# encryption_key = get_random_bytes(16)
#
# encrypted_text = encrypt(text_to_encrypt, encryption_key)
# print(f"Encrypted Text: {encrypted_text}")
#
# decrypted_text = decrypt(encrypted_text, encryption_key)
# print(f"Decrypted Text: {decrypted_text}")


class UserList:
    _userList = []

    data_file_name = "static/data.txt"
    temp_file_name = "static/temp.txt"

    def __init__(self):
        self._userList = []

    def add_user(self, user: User):
        self._userList.append(user)
        os.remove(self.temp_file_name)
        with open(self.temp_file_name, 'w') as f:
            tmp_text = ""
            for i in self._userList:
                tmp_text += "{" + i.to_json() + "}\n"
            f.write(tmp_text)

    def get_all_users(self) -> list[User]:
        return self._userList

    def get_user_by_login(self, login) -> None | User:
        user: User
        for user in self._userList:
            if user.get_login() == login:
                return user
        return None

    def frase_check(self, secret_key: str) -> bool:
        if len(secret_key) != 16:
            return False
        with open(self.data_file_name, 'r') as f:
            self._userList.clear()
            file_text = self.decrypt(f.read(), secret_key)
            print(file_text)
            with open(self.temp_file_name, 'w') as f:
                f.write(file_text)
        text = ""
        with open(self.temp_file_name, 'r') as f:
            text = f.read()
        return '{"login":"ADMIN","email":"Admin@ya.ru","password":"' in text

    def load(self, secret_key: str):
        with open(self.data_file_name, 'r') as f:
            self._userList.clear()
            file_text = self.decrypt(f.read(), secret_key)
            json_arr = json.loads(file_text.replace('\\', '\\\\'))
            for i in json_arr:
                is_blocked: bool = i['is_blocked'] == "True"
                is_password_limited: bool = i['is_password_limited'] == "True"
                min_password_len: int = int(i['min_password_len'])
                last_password_edit: datetime = datetime.strptime(i['last_password_edit'].split()[0], '%Y-%M-%d')
                password_time: int = int(i['password_time'])
                self._userList.append(User(i['login'], i['email'], i['password'], is_blocked, is_password_limited, min_password_len, last_password_edit, password_time))

        self._userList.append(User("old_user", "old_user@yadnex.ru", "d41d8cd98f00b204e9800998ecf8427e", False, False, 0, datetime(year=1970, month=1, day=1), 30))

        with open(self.temp_file_name, 'w') as f:
            tmp_text = ""
            for i in self._userList:
                tmp_text += "{" + i.to_json() + "}\n"
            f.write(tmp_text)

    def save(self, secret_key: bytes):
        text = "["
        for user in self._userList:
            text += "{" + user.to_json() + "},"
        text = text[:-1]
        text += "]"
        data = self.encrypt(text, secret_key)

        os.remove(self.data_file_name)
        with open(self.data_file_name, 'w') as f:
            f.write(data.decode())

    def encrypt(self, text, key):
        cipher = AES.new(key, AES.MODE_CFB, iv=get_random_bytes(16))
        ciphertext = cipher.encrypt(text.encode('utf-8'))
        return b64encode(cipher.iv + ciphertext)

    def decrypt(self, ciphertext, key: str):
        data = b64decode(ciphertext)
        cipher = AES.new(bytes(key, encoding='utf-8'), AES.MODE_CFB, iv=data[:16])
        decrypted_text = cipher.decrypt(data[16:]).decode('utf-8')
        return decrypted_text
