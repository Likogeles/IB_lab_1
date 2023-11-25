class User:
    _login: str = ""
    _password: str = ""
    _is_blocked: bool = False
    _is_password_limited: bool = True
    _min_password_len: int = 0
    _password_time: int = 0

    def __init__(self, login: str, hash_password: str, is_blocked: bool, is_password_limited: bool, min_password_len: int, password_time: int):
        self._login = login
        self._password = hash_password
        self._is_blocked = is_blocked
        self._is_password_limited = is_password_limited
        self._min_password_len = min_password_len
        self._password_time = password_time

    @classmethod
    def new_user(self, login: str, password: str, password_time: int):
        self.login = login
        self.password = password
        self._is_blocked = False
        self._is_password_limited = True
        self._min_password_len = 0
        self._password_time = password_time

    def get_login(self) -> str:
        return self._login
