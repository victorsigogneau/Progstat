import datetime
import pickle
import regex
import re
import pandas as pd
def singleton(Corpus):
    instances= [None]
    def wrapper(nom,authors, id2doc):
        if instances[0] is None:
            instances[0]=Corpus(nom,authors,id2doc)
        return instances[0]
    return wrapper

#@singleton
class Corpus:
    def __init__(self, nom, authors, id2doc):
        self.nom = nom #nom du corpus
        self.authors = authors #dictionnaire des auteurs
        self.id2doc = id2doc #dictionnaire des documents
        self.ndoc = len(id2doc) #comptage des documents
        self.naut = len(authors) #comptage des auteurs
        self.textEntier = self.texteComplet() #concatenation de tous les textes du corpus

    #Donne le nom du corpus
    def get_name(self):
        return self.nom
    #affiche le nom du corpus de façon plus digeste
    def __repr__(self):
        return "Le theme du Corpus est : " + self.name

    #trie les documents par date et affiche les n premiers
    def trie_date(self, n):
        datesdico = []
        for i in range(len(self.id2doc)):
            datesdico.append(self.id2doc[i].date)
        datessorted = sorted(datesdico, reverse=True)
        for i in range(n):
            print(datessorted[i])

    #trie les documents par titre et affiche les n premiers
    def trie_titre(self, n):
        titlesdico = []
        for i in range(len(self.id2doc)):
            titlesdico.append(self.id2doc[i].titre)
        titlessorted = sorted(titlesdico)
        for i in range(n):
            print(titlessorted[i])

    #sauvegarde le corpus
    def save(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)

    #charge le corpus
    def load(cls, file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    #Concatene tous les textes des documents du corpus
    def texteComplet(self):
        txt=""
        for i in range(len(self.id2doc)):
            txt+=self.id2doc[i].texte
        return txt

    #Recherche les phrases qui contiennent le mot-clé (keyword)
    def search(self, keyword):
        txt=self.textEntier
        regex = re.compile(keyword)
        phrases = txt.split('.')
        passage = []
        for phrase in phrases:
            if regex.search(phrase):
                passage.append(phrase)
        return passage

    #Retourne dans un dataFrame l'expression, la phrase, le n termes a droite et gauche du mot-clé(keyword)
    def concorde(self, keyword,n):
        txt=self.textEntier
        regex = re.compile(keyword)
        phrases = txt.split('.')
        tableau=[]
        for phrase in phrases:
            if regex.search(phrase):
                start = regex.search(phrase).start()
                end = regex.search(phrase).end()
                left_size = phrase[max(0, start-n):start]
                right_size = phrase[end:end+n]
                tableau.append([keyword, left_size, right_size, phrase])
        return pd.DataFrame(tableau, columns=['Expression', 'Contexte gauche', 'Contexte droit', 'Phrase'])

    #Miniscule, supprimer les retours a la ligne, la ponctuation et les chiffres
    def nettoyer_texte(self,chaine):
        chaine=chaine.lower()
        chaine = chaine.strip()
        chaine=re.sub(r'[^\w\s]|\d', '', chaine)
        chaine=chaine.split()
        return chaine

    #Donne le nombre de mots uniques et les n mots les plus fréquents
    def stat(self,n):
        #nb de mots uniques
        txt=self.textEntier
        nbMotUnique = len(set(txt.split()))
        words = txt.split()
        word_count = {}
        for i in range(len(self.id2doc)):
            textDoc=self.id2doc[i].texte
            textDoc = self.nettoyer_texte(textDoc)
            nombre_de_doc=False
            for word in textDoc:
                if word in word_count:
                    word_count[word]["term_frequency"] += 1
                    if nombre_de_doc is False:
                        word_count[word]["document_frequency"] += 1
                else:
                    word_count[word] = {}
                    word_count[word]["term_frequency"] = 1
                    word_count[word]["document_frequency"] = 1
                    nombre_de_doc=True
        freq = pd.DataFrame.from_dict(word_count, orient='index')
        freq=freq.reset_index()
        freq=freq.rename(columns={'index': 'word'})
        freq = freq.sort_values(by='term_frequency', ascending=False)
        print (f"Il y a {nbMotUnique} mots uniques et les mots des plus fréquents sont \n {freq[0:5]}")
        return freq



