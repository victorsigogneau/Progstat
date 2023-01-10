#Class qui genere un document de classe fille soit reddit soit arxiv
class DocumentGenerator:
    @staticmethod
    #Suivant le champ type créer un Document de type Arxiv ou Reddit si il est incconu retourne une erreur
    def factory(titre, auteur, url, texte, date,type):
        if type == "Arxiv" : return ArxivDocument(titre, auteur, url, texte, date,type)
        if type == "Reddit" : return RedditDocument(titre, auteur, url, texte, date,type)

        assert 0, "Erreur type inconnu: "+ type # si le type entré n'est pas arxiv ou reddit
class Document:
    def __init__(self, titre, auteur, date, url,type, texte="vide"):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = type

    #affiche les différents champs de la CLasse Document
    def affichage(self):
        print("Titre: " + self.titre)
        print("Auteur: " , self.auteur)
        print("Date: ", self.date)
        print("URL: " ,self.url)
        #print("Texte: " + self.texte)

    def getType(self):
        pass

    #Affiche le titre du document
    def __str__(self):
        return("Le titre du doc est : " + self.titre)

#Classe fille de Document RedditDocument
class RedditDocument(Document):
    def __init__(self,titre, auteur, date, url, texte,type='Reddit'):
        super().__init__(titre, auteur, date, url,type, texte)
        self.nbcommentaire=0

    #Affiche le titre du document
    def __str__(self):
        return("Document reddit dont le titre est :" + self.titre)
    def set_nbcommentaire(self,nbcommentaire):
        self.nbcommentaire=nbcommentaire
    def getType(self):
        return self.type

#Classe fille de Document ArxivDocument
class ArxivDocument(Document):
    def __init__(self,titre, auteur, date, url, texte,type='Arxiv'):
        super().__init__(titre, auteur, date, url,type, texte)
        self.coauthors=[]
    #Affiche le titre du document
    def __str__(self):
        return("Document Arxiv dont le titre est :" + self.titre)
    #Configure les coauteurs
    def set_coauthors(self,coauthors):
        self.coauthors=coauthors
    #Retourne le type de ArxivDocument
    def getType(self):
        return self.type


