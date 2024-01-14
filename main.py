from flask import Flask, request, redirect

from User import User
from UserList import UserList

app = Flask(__name__)
userList = UserList()
userList.add_user(User("1", "1@ya.ru", "1", False, True, 0, 30))
userList.add_user(User("12", "12@ya.ru", "12", False, True, 0, 30))
userList.add_user(User("123", "123@ya.ru", "123", False, True, 0, 30))
userList.add_user(User("1234", "1234@ya.ru", "1234", False, True, 0, 30))


def head_html(title):
    return f"""
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
                <title>{title}</title>
            </head>
            """


@app.route("/")
@app.route("/home")
def index():
    return f"""<!DOCTYPE html>
            <html>
                {head_html("Система учёта пользователей")}
                <body>
                    <div class="container mt-5">
                        <h1>Система учёта пользователей</h1>
                        <br>
                        <a class="btn btn-primary" href="log_in">Войти</a>
                    </div>
                </body>
            </html>"""


@app.route("/log_in", methods=["POST", "GET"])
def log_in():
    if request.method == "POST":
        login_form = request.form['login_form']
        password_form = request.form['password_form']
        if login_form == "ADMIN":
            return redirect("/admin")
    return f"""<!DOCTYPE html>
            <html>
                {head_html("Вход")}
                <body>
                    <div class="container mt-5">
                        <h1>Вход в аккаунт</h1>
                        <br>
                        <form method="POST">
                            <input type="text" name="login_form" id="login_form" class="form-control" placeholder="Введите логин">
                            <br>
                            <input type="text" name="password_form" id="password_form" class="form-control"  placeholder="Введите пароль">
                            <br>
                            <input type="submit" class="btn btn-success" value="Войти">
                            <br>
                        </form>
                    </div>
                </body>
            </html>"""


@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        login_form = request.form['login_form']
        email_form = request.form['email_form']
        password_form = request.form['password_form']
        second_password_form = request.form['second_password_form']
        min_password_len_form = request.form['min_password_len_form']
        password_time_form = request.form['password_time_form']
        is_password_limited_switch = request.form.getlist('is_password_limited_switch')

        print(login_form)
        print(email_form)
        print(password_form)
        print(second_password_form)
        print(is_password_limited_switch)
        print(min_password_len_form)
        print(password_time_form)

    return f"""<!DOCTYPE html>
                <html>
                    {head_html("Редактирование")}
                    <body>
                        <div class="container mt-5">
                            <h1>Пользователь</h1>
                            <br>
                            <div class="alert alert-danger" role="alert">
                                <ul class="errors">
                                    <li>Ошибка 1!</li>
                                    <li>Ошибка 2!</li>
                                    <li>Ошибка 3!</li>
                                    <li>Ошибка 4!</li>
                                </ul>
                            </div>
                            <form method="POST">
                                <h4>Логин</h4>
                                <input type="text" name="login_form" id="login_form" class="form-control">
                                <br>
                                <h4>Почта</h4>
                                <input type="text" name="email_form" id="email_form" class="form-control">
                                <br>
                                <h4>Пароль</h4>
                                <input type="text" name="password_form" id="password_form" class="form-control">
                                <br>
                                <h4>Повторите пароль</h4>
                                <input type="text" name="second_password_form" id="second_password_form" class="form-control">
                                <br>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" role="switch" id="is_password_limited_switch" name="is_password_limited_switch" checked>
                                    <label class="form-check-label" for="is_password_limited_switch">Ограничения пароля</label>
                                </div>
                                <br>
                                <h4>Минимальная длина пароля</h4>
                                <div class="form-outline">
                                    <input type="number" id="min_password_len_form" name="min_password_len_form" value="0" min="0" class="form-control"/>
                                </div>
                                <h4>Срок действия пароля</h4>
                                <div class="form-outline">
                                    <input type="number" id="password_time_form" name="password_time_form" value="0" min="0" class="form-control"/>
                                </div>
                                <input type="submit" class="btn btn-success" value="Сохранить">
                                <br>
                            </form>
                        </div>
                    </body>
                </html>"""


@app.route("/admin")
def admin():

    def row_generator(newUserList: list[User]) -> str:

        rows = ""

        for i in range(len(newUserList)):
            check = """
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-lg" viewBox="0 0 16 16">
                            <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425z"/>
                        </svg>
                    """
            not_check = """
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                            </svg>
                        """

            rows += f"""
                <tr>
                    <th scope="row">{i+1}</th>
                    <td>{newUserList[i].get_login()}</td>
                    <td>{newUserList[i].get_email()}</td>
                    <td>{check if not newUserList[i].get_is_blocked() else not_check}</td>
                    <td>{check if newUserList[i].get_is_password_limited() else not_check}</td>
                    <td>{newUserList[i].get_min_password_len()}</td>
                    <td>{newUserList[i].get_password_time()}</td>
                    <td><a class="btn btn-primary" href="/">Редактировать</a> <a class="btn btn-danger" href="/">Заблокировать</a></td>
                </tr>
               """

        return rows

    table = f"""
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Логин</th>
                        <th scope="col">Почта</th>
                        <th scope="col">Активен</th>
                        <th scope="col">Ограничения пароля</th>
                        <th scope="col">Мин. длина пароля</th>
                        <th scope="col">Срок действия пароля</th>
                        <th scope="col">Действия</th>
                    </tr>
                </thead>
                <tbody>
                    {row_generator(userList.get_all_users())}
                </tbody>
            </table>
            """

    return f"""<!DOCTYPE html>
            <html>
                {head_html("Административный интерфейс")}
                <body>
                    <div class="container mt-5">
                        <h1>Административный интерфейс</h1>
                        <a class="btn btn-primary" href="/">Сменить пароль</a>
                        <br>
                        <br>
                        <a class="btn btn-primary" href="/edit">Добавить пользователя</a>
                        <br>
                        <br>
                        <h3>Пользователи:</h3>
                        <br>
                        {table}
                    </div>
                </body>
            </html>"""


if __name__ == "__main__":
    app.run(debug=True)
