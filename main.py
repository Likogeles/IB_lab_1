from flask import Flask, request, redirect

app = Flask(__name__)


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


@app.route("/admin")
def admin():
    return f"""<!DOCTYPE html>
            <html>
                {head_html("Административный интерфейс")}
                <body>
                    <h1>Админский аккаунт</h1>
                </body>
            </html>"""


if __name__ == "__main__":
    app.run(debug=True)
