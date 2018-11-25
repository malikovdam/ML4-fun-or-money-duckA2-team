from flask import Flask, render_template

app = Flask(__name__)


def generate():
    # TODO
    return '<JOKE TEXT>'


@app.route("/")
def hello():
    return render_template('index.html', joke=generate())
