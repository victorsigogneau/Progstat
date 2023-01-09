class DocumentGenerator: # OK
    @staticmethod
    def factory(titre, auteur, url, texte, date,type):
        if type == "Arxiv" : return ArxivDocument(titre, auteur, url, texte, date,type)
        if type == "Reddit" : return RedditDocument(titre, auteur, url, texte, date,type)

        assert 0, "Erreur : "+ type # si le type entré n'est pas arxiv ou reddit
class Document:
    def __init__(self, titre, auteur, date, url,type, texte="vide"):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = type

    def affichage(self):
        print("Titre: " + self.titre)
        print("Auteur: " , self.auteur)
        print("Date: ", self.date)
        print("URL: " ,self.url)
        #print("Texte: " + self.texte)

    def getType(self):
        pass

    def __str__(self):
        return("Le titre du doc est : " + self.titre)

class RedditDocument(Document):
    def __init__(self,titre, auteur, date, url, texte,type='Reddit'):
        super().__init__(titre, auteur, date, url,type, texte)
        self.nbcommentaire=0
    def __str__(self):
        return("Document reddit dont le titre est :" + self.titre)
    def set_nbcommentaire(self,nbcommentaire):
        self.nbcommentaire=nbcommentaire
    def getType(self):
        return self.type


class ArxivDocument(Document):
    def __init__(self,titre, auteur, date, url, texte,type='Arxiv'):
        super().__init__(titre, auteur, date, url,type, texte)
        self.coauthors=[]
    def __str__(self):
        return("Document Arxiv dont le titre est :" + self.titre)
    def set_coauthors(self,coauthors):
        self.coauthors=coauthors
    def getType(self):
        return self.type


