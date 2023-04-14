from wtforms import validators, Form, StringField, PasswordField, TextAreaField
from flask_ckeditor import CKEditorField

class commentForm(Form):
    comment = TextAreaField(
        "Comment",
        [validators.Length(min=20, max=500), validators.InputRequired()],
        render_kw={"placeholder": "оставьте комментарий"},
    )



class loginForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "имя"},
    )
    password = PasswordField(
        "Password",
        [validators.Length(min=8), validators.InputRequired()],
        render_kw={"placeholder": "пароль"},
    )


class createPostForm(Form):
    postTitle = StringField(
        "Post Title",
        [validators.Length(min=4, max=75), validators.InputRequired()],
        render_kw={"placeholder": "заголовок поста"},
    )
    postDescription = TextAreaField(
        "Post Description", [validators.InputRequired(), validators.Length(min=25, max=200)], render_kw={"placeholder": "описание"}
    )
    postTags = StringField(
        "Post Tags", [validators.InputRequired()], render_kw={"placeholder": "тэги"}
    )
    postContent = CKEditorField(
        "Post Content",
        [validators.Length(min=50)],
    )


class changePasswordForm(Form):
    oldPassword = PasswordField(
        "oldPassword",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "старый пароль"},
    )
    password = PasswordField(
        "password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "новый пароль"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "подтвердите ваш пароль"},
    )


class changeUserNameForm(Form):
    newUserName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "новое имя"},
    )


class signUpForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "имя"},
    )
    email = StringField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"placeholder": "email"},
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "пароль"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "подтвердите пароль"},
    )
