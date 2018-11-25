from flask import Flask, render_template
import markovify

app = Flask(__name__)

with open("wall.txt") as f:
    text = f.read()

text_model = markovify.Text(text, state_size=3)


def generate():
    # TODO
    return text_model.make_sentence(tries=1000)


@app.route("/")
def hello():
    return render_template('index.html', joke=generate())
