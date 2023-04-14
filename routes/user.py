from flask import redirect, url_for, session

from helpers import (
    sqlite3,
    message,
    render_template,
    Blueprint,
    getStepCounts,
    getProfileAuyhByGoogle,
    getProfileNameColor
)

userBlueprint = Blueprint("user", __name__)


@userBlueprint.route("/user/<userName>")
def user(userName):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(f"select userName from users")
    users = cursor.fetchall()
    match str(userName).lower() in str(users).lower():
        case True:
            message("2", f'USER: "{userName}" FOUND')

            cursor.execute(f'select * from users where lower(userName) = "{userName}"')
            user = cursor.fetchone()
            show_login_text = 0
            if "userName" in session and session["userName"] == userName:
                if not getProfileAuyhByGoogle(session["userName"]):
                    show_login_text = 1
            step_count = int(user[10])
            if step_count > 12000:
                frame_color = "ruby"
            elif step_count > 10000:
                frame_color = "gold"
            elif step_count > 8000:
                frame_color = "silver"
            elif step_count > 6000:
                frame_color = "bronze"
            else:
                frame_color = "standard"
            userNameColor = getProfileNameColor(userName)
            print(userNameColor)
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute(f'select views from posts where author = "{user[1]}"')
            viewsData = cursor.fetchall()
            views = 0
            for view in viewsData:
                views += int(view[0])
            cursor.execute(f'select * from posts where author = "{user[1]}"')
            posts = cursor.fetchall()
            connection = sqlite3.connect("db/comments.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select * from comments where lower(user) = "{userName.lower()}"'
            )
            comments = cursor.fetchall()
            if posts:
                showPosts = True
            elif not posts:
                showPosts = False
            if comments:
                showComments = True
            elif not comments:
                showComments = False
            message("2", f'USER: "{userName}"s PAGE LOADED')
            return render_template(
                "user.html",
                user=user,
                views=views,
                posts=posts,
                comments=comments,
                showPosts=showPosts,
                showComments=showComments,
                steps=step_count,
                frame_color=frame_color,
                show_login_text=show_login_text,
                userNameColor=userNameColor
            )

        case _:
            message("1", f'USER: "{userName}" NOT FOUND')
            return render_template("404.html")
