from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    addPoints,
    currentDate,
    currentTime,
    render_template,
    Blueprint,
    createPostForm,
)

createPostBlueprint = Blueprint("createPost", __name__)


@createPostBlueprint.route("/createpost", methods=["GET", "POST"])
def createPost():
    match "userName" in session or "from_cron_task" in dict(request.form):
        case True:
            form = createPostForm(request.form)
            if request.method == "POST":
                req_data = dict(request.form)
                if "from_cron_task" in req_data:
                    postTitle = req_data["postTitle"]
                    postTags = req_data["postTags"]
                    postContent = req_data["postContent"]
                    postDescription = req_data["postDescription"]
                    cur_user = req_data["postAuthor"]
                else:
                    postTitle = request.form["postTitle"]
                    postTags = request.form["postTags"]
                    postContent = request.form["postContent"]
                    postDescription = request.form["postDescription"]
                    cur_user = session["userName"]
                match postContent == "":
                    case True:
                        flash("контент не может быть пустым", "error")
                        message(
                            "1",
                            f'POST CONTENT NOT BE EMPTY USER: "{cur_user}"',
                        )
                    case False:
                        connection = sqlite3.connect("db/posts.db")
                        cursor = connection.cursor()
                        print(postContent)
                        cursor.execute(
                            f"""
                            insert into posts(title,tags,content, description, author,views,date,time,lastEditDate,lastEditTime) 
                            values('{postTitle}',"{postTags}",'{postContent}', '{postDescription}',
                            "{cur_user}",0,
                            "{currentDate()}",
                            "{currentTime()}",
                            "{currentDate()}",
                            "{currentTime()}")
                            """
                        )
                        connection.commit()
                        message("2", f'POST: "{postTitle}" POSTED')
                        addPoints(20, cur_user)
                        flash("Вы заработали 20 очков за создание поста ", "success")
                        return redirect("/")
            return render_template("createPost.html", form=form)
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need loin for create a post", "error")
            return redirect("/login/redirect=&")
