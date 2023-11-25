from User import User


class UserList():
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
