from flask import Flask, request, jsonify, redirect
from bot import send_message


app = Flask(__name__)


@app.route("/")
def hello():
    return redirect()


@app.route("/message", methods=['GET'])
def message():
    try:
        chat_id = request.args.get('chat_id')
        message = request.args.get('message')
        send_message(chat_id, message)
        return jsonify({'status': 'OK'})
    except Exception as e:
        return jsonify({'status': 'ERROR', 'error': str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)