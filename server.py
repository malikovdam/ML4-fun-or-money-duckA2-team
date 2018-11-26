from flask import Flask, render_template
import markovify

app = Flask(__name__)

datasets = ['jumoreski', 'overhear', 'che', 'horo']

models = {}
for k in datasets:
    models[k] = markovify.Text(open('data/wall-%s.txt' % k).read(), state_size=3)


def generate(model):
    return model.make_sentence(tries=1000)


@app.route("/")
def hello():
    return render_template('index.html', joke=generate(models['jumoreski']), subj='юморесок')


@app.route("/overhear")
def oh():
    return render_template('index.html', joke=generate(models['overhear']), subj='подслушано')


@app.route("/che")
def che():
    return render_template('index.html', joke=generate(models['che']), subj='"че"')


@app.route("/horo")
def horo():
    return render_template('index.html', joke=generate(models['horo']), subj='гороскопов')
