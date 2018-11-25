from flask import Flask, render_template
import markovify

app = Flask(__name__)

with open("wall.txt") as f:
    text = f.read()

text_model = markovify.Text(text, state_size=3)

oh_model = markovify.Text(open('wall-overhear.txt').read(), state_size=3)


def generate():
    # TODO
    return text_model.make_sentence(tries=1000)


def generate_oh():
    return oh_model.make_sentence(tries=1000)


@app.route("/")
def hello():
    return render_template('index.html', joke=generate(), subj='юморесок')


@app.route("/overhear")
def oh():
    return render_template('index.html', joke=generate_oh(), subj='подслушано')
