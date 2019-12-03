from flask import Flask, render_template, request
from MakeData import Pokedex, Pokemon
from backend import Data, package, readData, preprocess1, preprocess2, preprocess3
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return phase1()

@app.route('/phase1')
def phase1():
    active = 'phase1'
    modes = {'No Stopwords':'P1', 'Lemmatized':'P2', 'Stemmed':'P3'}

    query = request.args.get('query')
    if query != None:
        data = readData(request.args.get('mode'))
        pkg = package(query, data, 5)
        return render_template('phase1_results.html', active=active, modes=modes, package=pkg)
    return render_template('phase1.html', active=active, modes = modes)

@app.route('/phase2')
def phase2():
    active = 'phase2'
    return render_template('phase2.html', active=active)

@app.route('/phase3')
def phase3():
    active = 'phase3'
    return render_template('phase3.html', active=active)

@app.route('/about')
def about():
    active = 'about'
    return render_template('about.html', active=active)

if __name__ == "__main__":
    app.run(debug = True)