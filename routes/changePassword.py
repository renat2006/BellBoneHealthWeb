from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    render_template,
    Blueprint,
    sha256_crypt,
    changePasswordForm,
)

changePasswordBlueprint = Blueprint("changePassword", __name__)


@changePasswordBlueprint.route("/changepassword", methods=["GET", "POST"])
def changePassword():
    match "userName" in session:
        case True:
            form = changePasswordForm(request.form)
            if request.method == "POST":
                oldPassword = request.form["oldPassword"]
                password = request.form["password"]
                passwordConfirm = request.form["passwordConfirm"]
                connection = sqlite3.connect("db/users.db")
                cursor = connection.cursor()
                cursor.execute(
                    f'select password from users where userName = "{session["userName"]}"'
                )
                if sha256_crypt.verify(oldPassword, cursor.fetchone()[0]):
                    if oldPassword == password:
                        flash("старый пароль не может совпадать с новым", "error")
                        message("1", "NEW PASSWORD CANT BE SAME WITH OLD PASSWORD")
                    elif password != passwordConfirm:
                        message("1", "PASSWORDS MUST MATCH")
                        flash("пароли не совпадают", "error")
                    elif oldPassword != password and password == passwordConfirm:
                        newPassword = sha256_crypt.hash(password)
                        connection = sqlite3.connect("db/users.db")
                        cursor = connection.cursor()
                        cursor.execute(
                            f'update users set password = "{newPassword}" where userName = "{session["userName"]}"'
                        )
                        connection.commit()
                        message(
                            "2", f'USER: "{session["userName"]}" CHANGED HIS PASSWORD'
                        )
                        session.clear()
                        flash("вам нужно зайти с новым паролем", "success")
                        return redirect("/login")
                else:
                    flash("неверный старый пароль", "error")
                    message("1", "OLD PASSWORD WRONG")

            return render_template("changePassword.html", form=form)
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("вам нужно зайти, чтобы сменить пароль", "error")
            return redirect("/login")
