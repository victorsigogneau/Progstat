import praw
import Document
from Author import Author
import datetime
from Corpus import Corpus
import pandas as pd
import dash

#Utilise les API reddit et arxiv pour créer des documents et remplir un objet corpus

id2Doc = {}
indice = 0
id2Auth = {}
"""
# API Reddit
reddit = praw.Reddit(client_id='eFffkL5lzdTbtcPUUipKXw', client_secret='taZ5t60V6huKTps1UTlDvhrl4JLo5A', user_agent='td3')
subr = reddit.subreddit('Saturn')
textes_Reddit = []
#Parours 100 post Reddit
for post in subr.hot(limit=10):
    # for post in subr.controversial(limit=10):
    texte = post.title
    texte = texte.replace("\n", " ")
    textes_Reddit.append(texte)
    #création des instances
    dReddit = Document.DocumentGenerator.factory(post.title, post.author, datetime.datetime.fromtimestamp(post.created), post.url, post.selftext,"Reddit")
    id2Doc[indice] = dReddit
    indice += 1

    if (post.author.name not in id2Auth):
        aReddit = Author(post.author.name, 0, {})
        aReddit.add(dReddit)
        id2Auth[post.author.name] = aReddit
    else:
        aReddit = id2Auth.get(post.author.name)
        #ajoute un article ecrit a l'auteur dans la classe author
        aReddit.add(dReddit)
        id2Auth[post.author.name] = aReddit

import urllib.request
import xmltodict

#API Arxiv
textes_Arxiv = []
query = "Saturn"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()
data = url_read.decode()
#Transformation en un objet json
dico = xmltodict.parse(data)
docs = dico['feed']['entry']
for d in docs:
    texte = d['title'] + ". " + d['summary']
    texte = texte.replace("\n", " ")
    textes_Arxiv.append(texte)
    #création des instances
    dArxiv = Document.DocumentGenerator.factory(d["title"], d["author"], datetime.datetime.strptime(d["published"], "%Y-%m-%dT%H:%M:%SZ"), d.get('@href'), d["summary"],"Arxiv")
    id2Doc[indice] = dArxiv
    indice += 1
    # S'il y a plusieurs auteurs
    if len(d["author"]) > 1:
        for auth in d["author"]:
            if not (auth.get("name") in id2Auth):
                aArxiv = Author(auth.get("name"), 0, {})
                aArxiv.add(dArxiv)
                id2Auth[auth.get("name")] = aArxiv
            if (auth.get("name") in id2Auth):
                aArxiv = id2Auth.get(auth.get("name"))
                aArxiv.add(dArxiv)
                id2Auth[auth.get("name")] = aArxiv
    else:
        if not (d["author"].get("name") in id2Auth):
            aArxiv = Author(d["author"].get("name"), 0, {})
            aArxiv.add(dArxiv)
            id2Auth[d["author"].get("name")] = aArxiv
        if (d["author"].get("name") in id2Auth):
            aArxiv = id2Auth.get(d["author"].get("name"))
            aArxiv.add(dArxiv)
            id2Auth[d["author"].get("name")] = aArxiv


corpus = textes_Reddit + textes_Arxiv
#Longueur du corpus
print("Longueur du corpus : " + str(len(corpus)))
import numpy as np
#Nombre de phrases dans le corpus
nb_phrases = [len(doc.split(".")) for doc in corpus]
print("Moyenne du nombre de phrases : " + str(np.mean(nb_phrases)))
#Nombre de mots dans le corpus et moyenne de mots
nb_mots = [len(doc.split(" ")) for doc in corpus]
print("Moyenne du nombre de mots : " + str(np.mean(nb_mots)))
print("Nombre total de mots dans le corpus : " + str(np.sum(nb_mots)))
"""
#Création d'un objet Corpus
CorpusObjet = Corpus("Saturn", id2Auth, id2Doc)
#charge le corpus
CorpusObjet=CorpusObjet.load("Saturn.pkl")
#trie le corpus par date et print les six premieres
CorpusObjet.trie_date(6)
#trie le corpus par titre et print les six premiers
CorpusObjet.trie_titre(6)
#Sauvegarde le Corpus
CorpusObjet.save("test.pkl")

#retourne les phrases qui contiennt le mot saturn
print(CorpusObjet.search("Saturn"))

#Data frame ou le mot Saturn apparait on retrouve les 5 caracteres a droite et a gauche
a=CorpusObjet.concorde("Saturn",5)
a.to_csv('concorde_saturne.csv',index=False)

#Affiche les 5 premieres lignes du DF(word, term_frequency, document_frequency
b=CorpusObjet.stat(5)



#Interface graphique Dash
from dash import Dash, dcc, html, Input, Output, State, dash_table
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Outil de recherche article Reddit et Arxiv",
        style = {
            'font-family': 'Verdana, sans-serif',
            'font-size': '30px',
            'color': 'white',
            'text-align' : 'center',
            'border': '2px solid black',
            'background-color' : 'black'

    }
    ),
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Valider', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',children="Entrez le nom d un corpus")
])


@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')

)
#Retourne le nom du corpus(value) , le nombre de mots dans le corpus(nombre_de_mot) et le nombre de document(nombre_de_doc) l'affichage du df(word,term_frequency,document_frequency
def update_output(n_clicks, value):
    CorpusInput = CorpusObjet.load(value + ".pkl")
    nom = CorpusInput.get_name()
    table2=CorpusInput.stat(3)
    txt=CorpusInput.texteComplet()
    nombre_de_mot =len(txt)
    nombre_de_doc=CorpusInput.get_ndoc()
    return html.Div([
        html.H4('Vous avez choisi le corpus : {} avec un total de {} mots pour {} documents'.format(nom,nombre_de_mot,nombre_de_doc)),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in table2.columns],
            data=table2.to_dict("rows"),
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)

