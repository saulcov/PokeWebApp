from nltk import word_tokenize, WordNetLemmatizer, SnowballStemmer
from MakeData import Pokedex, Pokemon
from nltk.corpus import stopwords
import pickle
import math

punctuations = set([",","(",")","[","]","{","}","#","@","!",":",";",".","?","’","”"])
words = set(stopwords.words('english'))

## removes punctuations and stopwords
def preprocess1(doc):
    vector = {}
    tokens = word_tokenize(doc.lower())
    ignore_set = punctuations.union(words)
    for t in tokens:
        if t not in ignore_set:
            try:
                vector[t] += 1
            except KeyError:
                vector[t] = 1
    return vector

## lemmatizes preprocess1
def preprocess2(doc):
    vector = {}
    lemmatizer = WordNetLemmatizer()
    for t, f in preprocess1(doc).items():
        l = lemmatizer.lemmatize(t, pos='v')
        try:
            vector[l] += f
        except KeyError:
            vector[l] = f
    return vector

## stems preprocess1
def preprocess3(doc):
    vector = {}
    stemmer = SnowballStemmer('english')
    for t, f in preprocess1(doc).items():
        s = stemmer.stem(t)
        try:
            vector[s] += f
        except KeyError:
            vector[s] = f
    return vector

## calculates tf-values for a given vector process
def calc_tf(vector):
    M = sum(vector.values())
    return {t:(f/M) for t, f in vector.items()}

## Data container {doc : {term : tf}} w/ iidx = {term : [docs]}
# and numOfTokens such that freq = numOfTokens*tf
class Data(dict):
    def __init__(self, process):
        self.iidx = {}
        self.numOfTokens = {}
        self.process = process
    def add(self, doc, tag):
        vector = self.process(doc)
        self.numOfTokens[tag] = sum(vector.values())
        #self[tag] = calc_tf(vector)
        self[tag] = vector
        for t in self[tag].keys():
            try:
                self.iidx[t].append(tag)
            except KeyError:
                self.iidx[t] = [tag]

## preprocesses the pokedex into a dataset
def MakeData():
    dataset = {'P1':Data(preprocess1), 'P2':Data(preprocess2), 'P3':Data(preprocess3)}
    with open('data/pokedex_national.pickle', 'rb') as pickle_in:
        pokedex = pickle.load(pickle_in)
        for idx, pkm in pokedex.items():
            doc = ' '.join(pkm.title() + pkm.descriptions)
            dataset['P1'].add(doc , idx)
            dataset['P2'].add(doc , idx)
            dataset['P3'].add(doc , idx)
    with open('data/dataset.pickle', 'wb') as pickle_out:
        pickle.dump(dataset, pickle_out)

## assumes q is a query, D = {doc : {term : freq}}
def score_query(q, D, K):
    score = {}
    N = len(D)
    R = set(D.process(q).keys()).intersection(set(D.iidx.keys()))
    print(D.process(q))
    for t in R:
        df = len(D.iidx[t])
        idf = math.log(N/df)
        for d in D.iidx[t]:
            freq = D[d][t]
            tf = freq/D.numOfTokens[d]
            try:
                score[d] += tf*idf
            except KeyError:
                score[d] = tf*idf
    score = sorted(score.items(), key=lambda s:s[1], reverse=True)[:K]
    return score, R

## intermediate step
def work(q, Data, K):
    S, R = score_query(q, Data, K)
    N = len(Data); info = {}
    for d, _ in S:
        nT = Data.numOfTokens[d]
        info[d] = {}
        for t in R:
            try:
                freq = Data[d][t]
            except KeyError:
                freq = 0
            tf = freq/nT
            df = len(Data.iidx[t])
            idf = math.log(N/df)
            info[d][t] = {'freq':freq, 'tf':tf, 'df':df, 'idf':idf, 'tfidf':tf*idf}
    return info, S

## package = [{doc, score, info}], where info = {term : {freq, tf, df, idf, tfidf}}
def package(q, Data, K):
    info, Scores = work(q, Data, K)
    out = []
    with open('data/pokedex_national.pickle', 'rb') as pickle_in:
        pokedex = pickle.load(pickle_in)
    for d, s in Scores:
        title = ', '.join(pokedex[d].title())
        description = ' '.join(pokedex[d].descriptions)
        out.append({'doc':d, 'score':s, 'info':info[d], 'name':pokedex[d].name, 'title':title, 'description':description})
    return out

def readData(mode):
    with open('data/dataset.pickle', 'rb') as pickle_in:
        data = pickle.load(pickle_in)
    return data[mode]
