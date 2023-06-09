from flask import session

from helpers import (
    sqlite3,
    render_template,
    Blueprint, updateSteps, getStepCounts, getProfileAuyhByGoogle, message, getProfilePoints
)

indexBlueprint = Blueprint("index", __name__)


@indexBlueprint.route("/")
def index():
    if "userName" in session:
        if getProfileAuyhByGoogle(session["userName"]):
            message("1", f'STEPS UPDATED')
            updateSteps(getStepCounts(), session["userName"])
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    posts = sorted(posts, key=lambda x: int(getProfilePoints(x[4])), reverse=True)
    print(posts)
    return render_template(
        "index.html",
        posts=posts,
    )
