#!/usr/env/dev python
# -*- coding: utf-8 -*-
"""IS211-Final-Course-Project - Tomasz Lodowski"""

import os
import re

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from sqlite3 import Error
import datetime

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
is_logged = False
posts = []


@app.route('/', methods=["POST", "GET"])
def index():
    if not is_logged:
        return redirect('/login')
    else:
        return redirect('/dashboard')


@app.route('/login', methods=["POST", "GET"])
def login():
    global is_logged
    if request.method == "POST":
        user_name = request.form['user_name']
        password = request.form['password']
        if user_name == "admin" and password == "password":
            is_logged = True
            return redirect("/dashboard")
        else:
            error = "The Username or Password is not correct"
            return render_template("Login.html", error=error)
    else:
        return render_template("Login.html", error="")


@app.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    global posts
    return render_template("dashboard.html", posts=posts)


@app.route('/new_post', methods=["POST", "GET"])
def new_post():
    global posts
    if request.method == "POST":
        title = request.form['Title']
        text = request.form['Text']
        author = "admin"
        now = datetime.datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        posts.insert(0, ((len(posts), date, title, text, author)))

        file = open("posts.txt", 'w')
        for idx, date, title, text, author in posts:
            file.write(date + "," + title + "," + text + "," + author + "\n")

        file.close()

        return redirect('/dashboard')
    else:
        return render_template("new_post.html")


@app.route("/Delete/<int:idx>", methods=["POST", "GET"])
def delete_index(idx):
    global posts
    del posts[idx]
    file = open("posts.txt", 'w')
    for idx, date, title, text, author in posts:
        file.write(date + "," + title + "," + text + "," + author + "\n")

    file.close()
    return redirect('/dashboard')


@app.route("/Edit/<int:idx>", methods=["POST", "GET"])
def edit_post(idx):
    global posts
    return render_template("edit_post.html", title=posts[idx][2], text=posts[idx][3], post_idx=idx)


@app.route("/edit_post/<int:idx>", methods=["POST", "GET"])
def modify_post(idx):
    global posts
    if request.method == "POST":
        title = request.form['Title']
        text = request.form['Text']
        author = "admin"
        now = datetime.datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        posts[idx] = (idx, date, title, text, author)

        file = open("posts.txt", 'w')
        for idx, date, title, text, author in posts:
            file.write(date + "," + title + "," + text + "," + author + "\n")

        file.close()

    return redirect('/dashboard')


if __name__ == '__main__':

    file = open("posts.txt", 'r')
    idx = 0
    for line in file:
        data = line.split(',')
        date = data[0]
        title = data[1]
        text = data[2]
        author = "admin"
        posts.append((idx, date, title, text, author))
        idx += 1

    app.run()
