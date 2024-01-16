from base64 import b64encode, b64decode

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

    def __init__(self):
        self._userList = []

    def add_user(self, user: User):
        self._userList.append(user)

    def get_all_users(self) -> list[User]:
        return self._userList

    def get_user_by_login(self, login) -> None | User:
        user: User
        for user in self._userList:
            if user.get_login() == login:
                return user
        return None

    def load(self):
        pass

    def save(self):
        pass

    def encrypt(self, text, key):
        cipher = AES.new(key, AES.MODE_CFB, iv=get_random_bytes(16))
        ciphertext = cipher.encrypt(text.encode('utf-8'))
        return b64encode(cipher.iv + ciphertext)

    def decrypt(self, ciphertext, key):
        data = b64decode(ciphertext)
        cipher = AES.new(key, AES.MODE_CFB, iv=data[:16])
        decrypted_text = cipher.decrypt(data[16:]).decode('utf-8')
        return decrypted_text