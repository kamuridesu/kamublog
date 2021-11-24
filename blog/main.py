from flask import Flask, request, redirect, render_template
import os

from apps.github_info import GithubInfo
from apps.functions import findRepos

app = Flask(__name__)
app.secret_key = "secret-key"


@app.route("/projects")
def projects():
    g_info = GithubInfo("kamuridesu").makeRequest()
    return render_template("projects.html", infos=g_info)


@app.route("/search")
def search():
    req = request.args.get("content")
    response = []
    if req:
        response = findRepos(req, GithubInfo("kamuridesu").makeRequest())
        print(response)
    return render_template("search.html", items=response)


@app.route("/")
def index():
    print("a")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)