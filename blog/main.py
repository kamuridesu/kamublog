from flask import Flask, request, redirect, render_template, jsonify
import os
import json
import uuid

from apps.github_info import GithubInfo, UserNotSupportedError
from apps.functions import checkGetParams, checkTokenScope
from apps.translation.translate import translate
from apps.chatbot.chatbot import Bot

app = Flask(__name__)
app.secret_key = "secret-key"

tokens = {}
with open("allowed_keys.json", "r", encoding="utf-8") as f:
    tokens = json.loads(f.read())

chatboat = Bot()


@app.route("/api/chatbot/train", methods=["GET"])
def train():
    if checkGetParams(request, "token"):
        if checkTokenScope(tokens, request.args.get("token"), "admin"):
            chatboat.train_from_file("filename")
    return redirect("/")


@app.route("/api/chatbot", methods=["GET"])
def chatbot():
    if checkGetParams(request, "token", "text"):
        if checkTokenScope(tokens, request.args.get("token"), "chatbot"):
            return chatboat.get_response(request.args.get("text"))
    return jsonify({"status": 'fail', "message": 'Invalid parameters'}), 404


@app.route('/api/translate', methods=['GET'])
def translate_text():
    if checkGetParams(request, "token", "text", "target"):
        if checkTokenScope(tokens, request.args.get("token"), "translate"):
            response = translate(request.args.get('text'), request.args.get('target'))
            return jsonify({"status": "OK", "text": response})
        return jsonify({"status": "error", "response": "Invalid token"}), 401
    return jsonify({"status": "error", "response": "No parameter"}), 404


@app.route("/api/add_user", methods=["GET"])
def add_user():
    if checkGetParams(request, "username", "scope", "token"):
        if checkTokenScope(tokens, request.args.get("token"), "admin"):
            username = request.args.get("username")
            scope = request.args.get("scope").split(",")
            user_uuid = str(uuid.uuid4())
            tokens[user_uuid] = {"name": username, "scopes": scope}
            with open("allowed_keys.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(tokens))
            return jsonify({"status": "ok"})
        return jsonify({"status": "fail"}), 401
    return jsonify({"status": "fail"}), 404


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


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects():
    try:
        g_info = GithubInfo("kamuridesu").makeRequest()
        return render_template("projects.html", infos=g_info)
    except UserNotSupportedError:
        return redirect("/error?error=github api error&code=500")


@app.route("/")
def index():
    logos = [
        {"image": "/static/images/github_logo.png", "url": "https://github.com/kamuridesu", "alt": "github logo"},
        {"image": "/static/images/twitter-logo.png", "url": "https://twitter.com/kamuri_chan", "alt": "twitter logo"},
        {"image": "/static/images/telegram-logo.png", "url": "https://t.me/kamuridesu", "alt": "telegram logo"}
    ]
    return render_template("index.html", logos=logos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)