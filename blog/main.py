from flask import Flask, request, redirect, render_template
import os

from apps.github_info import GithubInfo, UserNotSupportedError
from apps.functions import findRepos

app = Flask(__name__)
app.secret_key = "secret-key"


@app.route("/callback")
def callback():
    return redirect("/")


@app.route("/error")
def error_handler():
    req = request.args.get("error")
    err_code = request.args.get("code")
    if not req or not err_code:
        return redirect("/")
    return render_template("generic_error.html", error=req), err_code


@app.route("/projects")
def projects():
    try:
        g_info = GithubInfo("kamuridesu").makeRequest()
        return render_template("projects.html", infos=g_info)
    except UserNotSupportedError:
        return redirect("/error?error=github api error&code=500")
    return redirect("/")



@app.route("/")
def index():
    logos = [
        {"image": "/static/images/github_logo.png", "url": "https://github.com/kamuridesu", "alt": "github logo"},
        {"image": "/static/images/twitter-logo.png", "url": "https://twitter.com/kamuri_chan", "alt": "twitter logo"},
        {"image": "/static/images/telegram-logo.png", "url": "https://t.me/kamuridesu", "alt": "telegram logo"}
    ]
    return render_template("index.html", logos=logos)


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)