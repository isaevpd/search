import random

from flask import (
    Flask,
    render_template,
    jsonify
)

app = Flask(__name__)

SUGGESTIONS = [
    ["metallica", "machine head", "manowar"],
    ["bloodline", "ac/dc", "pretty reckless"],
    ["ritchie kotzen", "steve vai", "joe bonamassa"]
]


@app.route('/search', methods=['POST'])
def search():
    return jsonify(random.choice(SUGGESTIONS))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5033)
