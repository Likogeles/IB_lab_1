import hashlib
from datetime import datetime


class User:
    _login: str = ""
    _email: str = ""
    _password: str = ""
    _is_blocked: bool = False
    _is_password_limited: bool = True
    _min_password_len: int = 0
    _last_password_edit: datetime = datetime.now()
    _password_time: int = 0

    @classmethod
    def hash_password(cls, password: str) -> str:
        new_hash_password = hashlib.md5(password.encode())
        return new_hash_password.hexdigest()

    def check_password(self, text: str) -> bool:
        if self.hash_password(text) == self._password:
            return True
        return False

    def __init__(self, login: str, email: str, hash_password: str, is_blocked: bool, is_password_limited: bool, min_password_len: int, last_password_edit: datetime, password_time: int):
        self._login = login
        self._email = email
        self._password = hash_password
        self._is_blocked = is_blocked
        self._is_password_limited = is_password_limited
        self._min_password_len = min_password_len
        self._last_password_edit = last_password_edit
        self._password_time = password_time

    @classmethod
    def new_user(cls, login: str, email: str, password: str, is_blocked: bool, is_password_limited: bool, min_password_len: int, password_time: int):
        # Тут нужно захешировать пароль
        hash_password = cls.hash_password(password)
        new_user = cls(login, email, hash_password, is_blocked, is_password_limited, min_password_len, datetime.now(), password_time)
        return new_user

    def to_json(self) -> str:
        return f'"login":"{self._login}","email":"{self._email}","password":"{self._password}",' \
               f'"is_blocked":"{self._is_blocked}","is_password_limited":"{self._is_password_limited}",' \
               f'"min_password_len":"{self._min_password_len}","last_password_edit":"{self._last_password_edit}",' \
               f'"password_time":"{self._password_time}"'

    def get_login(self) -> str:
        return self._login

    def get_email(self) -> str:
        return self._email

    def get_password(self) -> str:
        return self._password

    def set_password(self, new_password: str):
        self._password = self.hash_password(new_password)

    def get_is_blocked(self) -> bool:
        return self._is_blocked

    def set_is_blocked(self, is_blocked: bool):
        self._is_blocked = is_blocked

    def get_is_password_limited(self) -> bool:
        return self._is_password_limited

    def set_is_password_limited(self, is_password_limited: bool):
        self._is_password_limited = is_password_limited

    def get_min_password_len(self) -> int:
        return self._min_password_len

    def get_password_time(self) -> int:
        return self._password_time

    def set_last_password_edit(self, last_password_edit: datetime):
        self._last_password_edit = last_password_edit

    def get_last_password_edit(self) -> datetime:
        return self._last_password_edit
