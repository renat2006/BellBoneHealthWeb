from helpers import (
    session,
    request,
    sqlite3,
    flash,
    message,
    redirect,
    addPoints,
    render_template,
    Blueprint,
    loginForm,
    sha256_crypt,
)
from flask import current_app as app

loginBlueprint = Blueprint("login", __name__)


@loginBlueprint.route("/login/redirect=<direct>", methods=["GET", "POST"])
def login(direct):
    direct = direct.replace("&", "/")
    match "userName" in session:
        case True:
            message("1", f'USER: "{session["userName"]}" ALREADY LOGGED IN')
            return redirect(direct)
        case False:
            form = loginForm(request.form)
            if request.method == "POST" or 'google_info' in session:
                if 'google_info' in session:
                    info = dict(session)['google_info']

                    userName = info["name"]

                    password = "google"

                    session.pop("google_info")
                else:
                    userName = request.form["userName"]
                    password = request.form["password"]
                userName = userName.replace(" ", "")
                connection = sqlite3.connect("db/users.db")
                cursor = connection.cursor()
                cursor.execute(
                    f'select * from users where lower(userName) = "{userName.lower()}"'
                )
                user = cursor.fetchone()
                if not user:
                    message("1", f'USER: "{userName}" NOT FOUND')
                    flash("пользователь не найден", "error")
                else:
                    if sha256_crypt.verify(password, user[3]) or user[9] == 1:
                        session["userName"] = user[1]
                        addPoints(1, session["userName"])
                        message("2", f'USER: "{user[1]}" LOGGED IN')
                        flash(f"Добро пожаловать, {user[1]}", "success")
                        return redirect(direct)
                    else:
                        message("1", "WRONG PASSWORD")
                        flash("Неверный пароль", "error")
            return render_template("login.html", form=form, hideLogin=True)
