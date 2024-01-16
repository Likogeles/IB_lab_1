import sys

from flask import Flask, request, redirect
import re

from User import User
from UserList import UserList

app = Flask(__name__)
userList = UserList()
max_password_tries = 3
password_tries = 0

pattern = r'(?:\d[^\d]+)*\d(?:[^\d]+\d)*'

userList.add_user(User("ADMIN", "1@ya.ru", "", False, True, 0, 30))
userList.add_user(User("1", "1@ya.ru", "1", False, True, 0, 30))
userList.add_user(User("12", "12@ya.ru", "12", False, True, 0, 30))
userList.add_user(User("123", "123@ya.ru", "123", False, True, 0, 30))
userList.add_user(User("1234", "1234@ya.ru", "1234", False, True, 0, 30))

# <meta charset="utf-8">
# <meta name="viewport" content="width=device-width, initial-scale=1">
# <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">

# <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">


@app.route("/drop")
def drop():
    sys.exit()


def head_html(title):
    return f"""
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
                <title>{title}</title>
            </head>
            """


def nav_html():
    return """<nav class="navbar navbar-expand-lg navbar-light bg-light">
              <a class="navbar-brand" href="#">Лабораторная работа ИБ №1</a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
            
              <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <div class="dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                Справка
                            </a>
                            <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                <a class="dropdown-item" href="/about">О программе</a>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
            </nav>"""


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
                        <a class="btn btn-primary" href="/log_in">Войти</a>
                        <br>
                        <br>
                        <a class="btn btn-warning" href="/about">Справка</a>
                    </div>
                </body>
            </html>"""


@app.route("/about")
def about():
    return f"""<!DOCTYPE html>
            <html>
                {head_html("О программе")}
                <body>
                    <div class="container mt-5">
                        <h1>О программе</h1>
                        <br>
                        <h3>Система учёта пользователей</h3>
                        <br>
                        <h4>Автор: Долгов Кирилл Сергеевич (ПИбд-42)</h4>
                        <br>
                        <h4>Вариант - 11</h4>
                        <br>
                        <h4>Ограничения на выбираемые пароли: чередование цифр, знаков препинания и снова цифр.</h4>
                        <br>
                        <h4>Используемый режим шифрования алгоритма DES для шифрования файла: CFB.</h4>
                        <br>
                        <h4>Добавление к ключу случайного значения: Да.</h4>
                        <br>
                        <h4>Используемый алгоритм хеширования пароля: MD5.</h4>
                        <br>
                        <br>
                        <a class="btn btn-primary" href="javascript:history.back()">Назад</a>
                    </div>
                </body>
            </html>"""


@app.route("/exit")
def exitApp():
    return redirect("/")




@app.route("/change_is_password_limited")
def change_is_password_limited():
    user_login = request.args.get("user")
    if user_login:
        user = userList.get_user_by_login(user_login)
        if user:
            user.set_is_password_limited(not user.get_is_password_limited())

    return redirect("/admin")


@app.route("/change_is_blocked")
def change_is_blocked():
    user_login = request.args.get("user")
    if user_login:
        user = userList.get_user_by_login(user_login)
        if user:
            user.set_is_blocked(not user.get_is_blocked())

    return redirect("/admin")


@app.route("/log_in", methods=["POST", "GET"])
def log_in():
    global password_tries
    login_errors = []
    if request.method == "POST":
        login_form = request.form['login_form']
        password_form = request.form['password_form']

        errors_flag = True

        if login_form not in [user.get_login() for user in userList.get_all_users()]:
            login_errors.append("Пользователя с таким логином не существует")
            errors_flag = False
        else:
            user = userList.get_user_by_login(login_form)
            if user.get_password() != User.hash_password(password_form):
                password_tries += 1
                login_errors.append(f"Неверный пароль. Осталось попыток: {max_password_tries-password_tries}")
                if password_tries >= max_password_tries:
                    return redirect('/drop')
                errors_flag = False
            else:
                if user.get_is_blocked():
                    login_errors.append("Пользователь заблокирован")
                    errors_flag = False

        if errors_flag:
            password_tries = 0
            if userList.get_user_by_login(login_form).get_password() == "":
                return redirect(f"/set_password?user={login_form}")
            if login_form == "ADMIN":
                return redirect("/admin")
            else:
                return redirect(f"/user?user={login_form}")

    error_message = ""
    if len(login_errors) != 0:
        error_message = '<div class="alert alert-danger" role="alert"><ul class="errors">'
        for i in login_errors:
            error_message += f"<li>{i}</li>"
        error_message += "</ul></div>"

    return f"""<!DOCTYPE html>
            <html>
                {head_html("Вход")}
                <body>
                    <div class="container mt-5">
                        <h1>Вход в аккаунт</h1>
                        <br>
                        {error_message}
                        <form method="POST">
                            <input type="text" name="login_form" id="login_form" class="form-control" placeholder="Введите логин">
                            <br>
                            <input type="password" name="password_form" id="password_form" class="form-control"  placeholder="Введите пароль">
                            <br>
                            <input type="submit" class="btn btn-success" value="Войти">
                            <br>
                            <br>
                            <a class="btn btn-danger" href="/drop">Завершить работу</a>
                            <br>
                        </form>
                    </div>
                </body>
            </html>"""


@app.route("/set_password", methods=["POST", "GET"])
def set_password():
    change_errors = []
    arg_user = request.args.get("user")
    if request.method == "POST":
        if arg_user:
            errors_flag = True
            user = userList.get_user_by_login(arg_user)
            new_password_form = request.form['new_password_form']
            second_new_password_form = request.form['second_new_password_form']

            if new_password_form != second_new_password_form:
                change_errors.append("Пароли не совпадают")
                errors_flag = False
            if user.get_is_password_limited():
                if not re.fullmatch(pattern, new_password_form):
                    change_errors.append(
                        "Пароль не удовлетворяет условию: Чередование цифр, знаков препинания и снова цифр.")
                    errors_flag = False
            if user.get_min_password_len() != 0:
                if len(new_password_form) < user.get_min_password_len():
                    change_errors.append(
                        "Пароль слишком короткий")
                    errors_flag = False

            if errors_flag:
                user.set_password(new_password_form)
                if user.get_login() == "ADMIN":
                    return redirect("/admin")
                else:
                    return redirect(f"/user?user={arg_user}")

    error_message = ""
    if len(change_errors) != 0:
        error_message = '<div class="alert alert-danger" role="alert"><ul class="errors">'
        for i in change_errors:
            error_message += f"<li>{i}</li>"
        error_message += "</ul></div>"

    return f"""<!DOCTYPE html>
            <html>
                {head_html("Изменить пароль")}
                <body>
                    <div class="container mt-5">
                        <h1>Задать пароль</h1>
                        <br>
                        <form method="POST">
                            <h5>Ваш пароль пуст, задайте новый (можно пропустить).</h5>
                            <br>
                            {error_message}
                            <h4>Новый пароль</h4>
                            <input type="password" name="new_password_form" id="new_password_form" class="form-control" placeholder="Новый пароль">
                            <br>
                            <h4>Повторите новый пароль</h4>
                            <input type="password" name="second_new_password_form" id="second_new_password_form" class="form-control" placeholder="Повторите новый пароль">
                            <br>
                            <input type="submit" class="btn btn-success" value="Задать">
                            <br>
                            <br>
                            {
                            '<a class="btn btn-primary" href="/admin">Пропустить</a>'
                            if arg_user == "ADMIN" else
                            f'<a class="btn btn-primary" href="/user?user={arg_user}">Пропустить</a>'
                            }
                            <br>
                            <br>
                            <a class="btn btn-danger" href="/drop">Завершить работу</a>
                            <br>
                        </form>
                    </div>
                </body>
            </html>"""


@app.route("/change_password", methods=["POST", "GET"])
def change_password():

    change_errors = []
    if request.method == "POST":
        arg_user = request.args.get("user")
        if arg_user:
            errors_flag = True
            user = userList.get_user_by_login(arg_user)
            old_password_form = request.form['old_password_form']
            new_password_form = request.form['new_password_form']
            second_new_password_form = request.form['second_new_password_form']

            if User.hash_password(old_password_form) != user.get_password():
                change_errors.append("Старый пароль введён неверно")
                errors_flag = False
            if new_password_form != second_new_password_form:
                change_errors.append("Новые пароли не совпадают")
                errors_flag = False
            if user.get_is_password_limited():
                if not re.fullmatch(pattern, new_password_form):
                    change_errors.append(
                        "Пароль не удовлетворяет условию: Чередование цифр, знаков препинания и снова цифр.")
                    errors_flag = False
            if user.get_min_password_len() != 0:
                if len(new_password_form) < user.get_min_password_len():
                    change_errors.append(
                        "Пароль слишком короткий")
                    errors_flag = False

            if errors_flag:
                user.set_password(new_password_form)
                if user.get_login() == "ADMIN":
                    return redirect("/admin")
                else:
                    return redirect(f"/user?user={arg_user}")

    error_message = ""
    if len(change_errors) != 0:
        error_message = '<div class="alert alert-danger" role="alert"><ul class="errors">'
        for i in change_errors:
            error_message += f"<li>{i}</li>"
        error_message += "</ul></div>"

    return f"""<!DOCTYPE html>
            <html>
                {head_html("Изменить пароль")}
                <body>
                    <div class="container mt-5">
                        <h1>Изменение пароля</h1>
                        <br>
                        <form method="POST">
                            {error_message}
                            <h4>Старый пароль</h4>
                            <input type="password" name="old_password_form" id="old_password_form" class="form-control" placeholder="Старый пароль">
                            <br>
                            <h4>Новый пароль</h4>
                            <input type="password" name="new_password_form" id="new_password_form" class="form-control" placeholder="Новый пароль">
                            <br>
                            <h4>Повторите новый пароль</h4>
                            <input type="password" name="second_new_password_form" id="second_new_password_form" class="form-control" placeholder="Повторите новый пароль">
                            <br>
                            <input type="submit" class="btn btn-success" value="Сохранить">
                            <br>
                        </form>
                    </div>
                </body>
            </html>"""


@app.route("/user")
def user():
    arg_user = request.args.get("user")

    if arg_user is None:
        return redirect("/")

    return f"""<!DOCTYPE html>
            <html>
                {head_html("Пользовательский интерфейс")}
                <body>
                    <div class="container mt-5">
                        <h1>Пользовательский интерфейс</h1>
                        <a class="btn btn-primary" href="/change_password?user={arg_user}">Сменить пароль</a>
                        <br>
                        <br>
                        <a class="btn btn-primary" href="/exit">Выйти</a>
                        <br>
                        <br>
                        <a class="btn btn-warning" href="/about">Справка</a>
                        <br>
                        <br>
                        <a class="btn btn-danger" href="/drop">Завершить работу</a>
                        <br>
                        <br>
                        <br>
                    </div>
                </body>
            </html>"""


@app.route("/edit", methods=["POST", "GET"])
def edit():

    login_form = ""
    email_form = ""
    password_form = ""
    second_password_form = ""
    min_password_len_form = 0
    password_time_form = 0
    is_password_limited_switch = True

    edit_errors = []

    if request.method == "POST":

        error_flag = True

        login_form = request.form['login_form']
        email_form = request.form['email_form']
        password_form = request.form['password_form']
        second_password_form = request.form['second_password_form']
        is_password_limited_switch = 'on' in request.form.getlist('is_password_limited_switch')
        min_password_len_form = request.form['min_password_len_form']
        password_time_form = request.form['password_time_form']

        if login_form == "":
            edit_errors.append("Логин не введён")
            error_flag = False
        if login_form in [user.get_login() for user in userList.get_all_users()]:
            edit_errors.append("Пользователь с этим логином уже существует")
            error_flag = False
        if email_form == "":
            edit_errors.append("Почта не введена")
            error_flag = False
        if password_form != second_password_form:
            edit_errors.append("Пароли не совпадают")
            error_flag = False

        if is_password_limited_switch:
            if not re.fullmatch(pattern, password_form):
                edit_errors.append("Пароль не удовлетворяет условию: Чередование цифр, знаков препинания и снова цифр.")
                error_flag = False

        if min_password_len_form != 0:
            if len(password_form) < int(min_password_len_form):
                edit_errors.append("Пароль слишком короткий")
                error_flag = False

        if error_flag:
            userList.add_user(User.new_user(login_form, email_form, password_form, False, is_password_limited_switch, int(min_password_len_form), int(password_time_form)))
            return redirect("/admin")

    error_message = ""
    if len(edit_errors) != 0:
        error_message = '<div class="alert alert-danger" role="alert"><ul class="errors">'
        for i in edit_errors:
            error_message += f"<li>{i}</li>"
        error_message += "</ul></div>"

    return f"""<!DOCTYPE html>
                <html>
                    {head_html("Редактирование")}
                    <body>
                        <div class="container mt-5">
                            <h1>Пользователь</h1>
                            <br>
                            {error_message}
                            <form method="POST">
                                <h4>Логин</h4>
                                <input type="text" name="login_form" id="login_form" class="form-control" value="{login_form}">
                                <br>
                                <h4>Почта</h4>
                                <input type="text" name="email_form" id="email_form" class="form-control" value="{email_form}">
                                <br>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" role="switch" id="is_password_limited_switch" name="is_password_limited_switch" {"checked" if is_password_limited_switch else ""}>
                                    <label class="form-check-label" for="is_password_limited_switch">Ограничения пароля (Чередование цифр, знаков препинания и снова цифр)</label>
                                </div>
                                <br>
                                <h4>Минимальная длина пароля</h4>
                                <div class="form-outline">
                                    <input type="number" id="min_password_len_form" name="min_password_len_form" value="{min_password_len_form}" min="0" class="form-control"/>
                                </div>
                                <h4>Срок действия пароля</h4>
                                <div class="form-outline">
                                    <input type="number" id="password_time_form" name="password_time_form" value="{password_time_form}" min="0" class="form-control"/>
                                </div>
                                <br>
                                <h4>Пароль</h4>
                                <input type="password" name="password_form" id="password_form" class="form-control" value="{password_form}">
                                <br>
                                <h4>Повторите пароль</h4>
                                <input type="password" name="second_password_form" id="second_password_form" class="form-control" value="{second_password_form}">
                                <br>
                                <input type="submit" class="btn btn-success" value="Сохранить">
                                <br>
                                <br>
                                <br>
                                <br>
                                <br>
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
                    <td>
                        <a class="btn btn-primary" href="/change_is_password_limited?user={newUserList[i].get_login()}">Изменить ограничения пароля</a>
                        {
                        f'<a class="btn btn-danger" href="/change_is_blocked?user={newUserList[i].get_login()}">Заблокировать</a>'
                        if not newUserList[i].get_is_blocked() else
                        f'<a class="btn btn-success" href="/change_is_blocked?user={newUserList[i].get_login()}">Разблокировать</a>'
                        }
                    </td>
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
                        <a class="btn btn-primary" href="/change_password?user=ADMIN">Сменить пароль</a>
                        <br>
                        <br>
                        <a class="btn btn-primary" href="/edit">Добавить пользователя</a>
                        <br>
                        <br>
                        <a class="btn btn-primary" href="/exit">Выйти</a>
                        <br>
                        <br>
                        <a class="btn btn-warning" href="/about">Справка</a>
                        <br>
                        <br>
                        <a class="btn btn-danger" href="/drop">Завершить работу</a>
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
