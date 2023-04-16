import os
import secrets
import sqlite3
import time
from os import mkdir
from os.path import exists
from datetime import datetime, timedelta

import requests
from passlib.hash import sha256_crypt
from flask import render_template, Blueprint
from forms import (
    loginForm,
    signUpForm,
    commentForm,
    createPostForm,
    changePasswordForm,
    changeUserNameForm,
)
from flask import (
    request,
    session,
    flash,
    redirect,
    render_template,
    send_from_directory,
    Flask,
    Blueprint,
)


def currentDate():
    return datetime.now().strftime("%d.%m.%y")


def currentTime(seconds=False):
    match seconds:
        case False:
            return datetime.now().strftime("%H:%M")
        case True:
            return datetime.now().strftime("%H:%M:%S")


def message(color, message):
    print(
        f"\n\033[94m[{currentDate()}\033[0m"
        f"\033[95m {currentTime(True)}]\033[0m"
        f"\033[9{color}m {message}\033[0m\n"
    )
    logFile = open("log.log", "a")
    logFile.write(f"[{currentDate()}" f"|{currentTime(True)}]" f" {message}\n")
    logFile.close()


def addPoints(points, user):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'update users set points = points+{points} where userName = "{user}"'
    )
    connection.commit()
    message("2", f'{points} POINTS ADDED TO "{user}"')


def updateSteps(steps, user):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'update users set steps = {steps} where userName = "{user}"'
    )
    connection.commit()
    message("2", f'{steps} STEPS ADDED TO "{user}"')


def getProfilePicture(userName):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'select profilePicture from users where lower(userName) = "{userName.lower()}"'
    )
    return cursor.fetchone()[0]


def getProfilePoints(userName):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'select points from users where lower(userName) = "{userName.lower()}"'
    )
    return cursor.fetchone()[0]


def getProfileNameColor(userName):
    points = getProfilePoints(userName)
    if points > 1000:
        color = "amethyst"
    elif points > 900:
        color = "sapphire"
    elif points > 800:
        color = "emerald"
    elif points > 700:
        color = "ruby"
    elif points > 500:
        color = "gold"
    elif points > 400:
        color = "bronze"
    else:
        color = "standard"
    return color


def getProfileAuyhByGoogle(userName):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'select authByGoogle from users where lower(userName) = "{userName.lower()}"'
    )
    return cursor.fetchone()[0]


def getStepCounts(days=1):
    api_url = 'https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate'
    headers = {"Authorization": f"Bearer {session['google_access_token']}"}

    agg_data = {
        "aggregateBy": [
            {"dataTypeName": "com.google.step_count.delta",
             "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"}
        ],
        "bucketByTime": {"durationMillis": 86400000},
        "startTimeMillis": int((datetime.now() - timedelta(days=days)).timestamp()) * 1000,
        "endTimeMillis": int(time.time() * 1000),

    }

    response = requests.post(api_url, headers=headers, json=agg_data)
    session['google_fit_data'] = response.json()
    print(session['google_fit_data'])
    step_counts = []
    try:
        for bucket in session['google_fit_data']['bucket']:
            for dataset in bucket['dataset']:
                for point in dataset['point']:
                    for value in point['value']:
                        if value['intVal']:
                            step_counts.append(value['intVal'])
    except BaseException as e:
        step_counts = 0

    session["step_count"] = sum(step_counts)
    return session["step_count"]
