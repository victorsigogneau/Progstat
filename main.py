#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08/05/2020

@author: julien and antoine
"""

# needs praw package, cf.:
# https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
import praw
import Document
from Author import Author
import datetime
from Corpus import Corpus
import pandas as pd

id2Doc = {}
indice = 0
id2Auth = {}

# Reddit

reddit = praw.Reddit(client_id='eFffkL5lzdTbtcPUUipKXw', client_secret='taZ5t60V6huKTps1UTlDvhrl4JLo5A', user_agent='td3')
subr = reddit.subreddit('Space')
textes_Reddit = []
#auteurs_Reddit = []
for post in subr.hot(limit=100):
    # for post in subr.controversial(limit=10):
    texte = post.title
    texte = texte.replace("\n", " ")
    textes_Reddit.append(texte)
    #création des instances
    dReddit = Document.DocumentGenerator.factory(post.title, post.author, datetime.datetime.fromtimestamp(post.created), post.url, post.selftext,"Reddit")
    id2Doc[indice] = dReddit
    indice += 1

    if not (post.author.name in id2Auth):
        aReddit = Author(post.author.name, 0, {})
        aReddit.add(dReddit)
        id2Auth[post.author.name] = aReddit
    if (post.author.name in id2Auth):
        aReddit = id2Auth.get(post.author.name)
        #ajoute un article ecrit a l'auteur dans la classe author
        aReddit.add(dReddit)
        id2Auth[post.author.name] = aReddit

import urllib.request
import xmltodict

textes_Arxiv = []

query = "space"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()

# url_read est un "byte stream" qui a besoin d'être décodé
data = url_read.decode()

dico = xmltodict.parse(data)  # xmltodict permet d'obtenir un objet ~JSON
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
            # print(auth.get("name"))
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

# print("Corpus length: %d" % len(corpus))
print("Longueur du corpus : " + str(len(corpus)))

for doc in corpus:
    # nombre de phrases
    print("Nombre de phrases : " + str(len(doc.split("."))))
    print("Nombre de mots : " + str(len(doc.split(" "))))

import numpy as np

nb_phrases = [len(doc.split(".")) for doc in corpus]
print("Moyenne du nombre de phrases : " + str(np.mean(nb_phrases)))

nb_mots = [len(doc.split(" ")) for doc in corpus]
print("Moyenne du nombre de mots : " + str(np.mean(nb_mots)))

print("Nombre total de mots dans le corpus : " + str(np.sum(nb_mots)))

corpus_plus100 = [doc for doc in corpus if len(doc) > 100]

chaine_unique = " ".join(corpus_plus100)

import pickle

with open("out.pkl", "wb") as f:
    pickle.dump(corpus_plus100, f)

with open("out.pkl", "rb") as f:
    corpus_plus100 = pickle.load(f)

import datetime

aujourdhui = datetime.datetime.now()
print(aujourdhui)

c = Corpus("Corpus", id2Auth, id2Doc)
c.trie_date(3)
c.trie_titre(4)

for doc in c.id2doc.values():
    print(doc.affichage())

for i in range(len(id2Doc)):
    print(id2Doc[i].getType())

print(c.search("planet"))

a=c.concorde("planet",5)

a.to_csv('output.csv', index=False)

b=c.stat(5)
b.to_csv('output2.csv', index=False)


