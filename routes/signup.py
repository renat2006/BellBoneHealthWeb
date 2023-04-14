import os

from dotenv import load_dotenv

from helpers import (
    session,
    secrets,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    currentDate,
    currentTime,
    render_template,
    Blueprint,
    signUpForm,
    sha256_crypt,
)

from flask import current_app as app

signUpBlueprint = Blueprint("signup", __name__)
load_dotenv()


@signUpBlueprint.route("/signup", methods=["GET", "POST"])
def signup():
    match "userName" in session:
        case True:
            message("1", f'USER: "{session["userName"]}" ALREADY LOGGED IN')
            return redirect("/")
        case False:
            form = signUpForm(request.form)

            if request.method == "POST" or 'google_info' in session:
                print('snxksnxk')
                authByGoogle = 0
                if 'google_info' in session:

                    authByGoogle = 1
                    info = dict(session)['google_info']
                    picture = info["picture"]
                    userName = info["name"]
                    email = info["email"]
                    password = info["name"] + str(secrets.token_urlsafe(32))
                    passwordConfirm = password

                    session.pop("google_info")

                else:

                    picture = f"https://api.dicebear.com/5.x/identicon/svg?seed={secrets.token_urlsafe(32)}"
                    userName = request.form["userName"]
                    email = request.form["email"]
                    password = request.form["password"]
                    passwordConfirm = request.form["passwordConfirm"]

                userName = userName.replace(" ", "")
                connection = sqlite3.connect("db/users.db")
                cursor = connection.cursor()
                cursor.execute("select userName from users")
                users = str(cursor.fetchall())
                cursor.execute("select email from users")
                mails = str(cursor.fetchall())
                if not userName in users and not email in mails:
                    if passwordConfirm == password:
                        match userName.isascii():
                            case True:
                                password = sha256_crypt.hash(password)
                                connection = sqlite3.connect("db/users.db")
                                cursor = connection.cursor()
                                cursor.execute(
                                    f"""
                                    insert into users(userName,email,password,profilePicture,role,points,creationDate,creationTime, authByGoogle) 
                                    values("{userName}","{email}","{password}",
                                    "{picture}",
                                    "user",0,
                                    "{currentDate()}",
                                    "{currentTime()}",
                                    "{authByGoogle}")
                                    """
                                )
                                connection.commit()
                                message("2", f'USER: "{userName}" ADDED TO DATABASE')
                                return redirect("/")
                            case False:
                                message(
                                    "1",
                                    f'USERNAME: "{userName}" DOES NOT FITS ASCII CHARACTERS',
                                )
                                flash("имя пользователя не соответсвует кодировке ascii", "error")
                    elif passwordConfirm != password:
                        message("1", " PASSWORDS MUST MATCH ")
                        flash("пароли не совпадают", "error")
                elif userName in users and email in mails:
                    message("1", f'"{userName}" & "{email}" IS UNAVAILABLE ')
                    flash("Эти имя пользователя и email уже заняты.", "error")
                elif not userName in users and email in mails:
                    message("1", f'THIS EMAIL "{email}" IS UNAVAILABLE ')
                    flash("Этот email уже занят.", "error")
                elif userName in users and not email in mails:
                    message("1", f'THIS USERNAME "{userName}" IS UNAVAILABLE ')
                    flash("Это имя пользователя уже занято.", "error")

            return render_template("signup.html", form=form, hideSignUp=True,
                                   client_secret=os.getenv("GOOGLE_CLIENT_SECRET"))
