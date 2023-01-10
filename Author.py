#Classe auteur
class Author:
    def __init__(self, name, ndoc, production):
        self.name = name #nom auteur
        self.ndoc = ndoc #nombre de documents publiés
        self.production = production #dictionnaire des documents écris par l'auteur

    #Indente la variable ndoc(nombre de documents publiés)
    def add(self, document):
        self.production[self.ndoc] = document
        self.ndoc += 1

    #Affiche le nom et le nombre d'article de l'auteur
    def __str__(self):
        return("Le nom de l'auteur est : " + self.name + " et a écrit " + ndoc + " article(s).")

    #Longueur moyenne des documents d'un auteur
    def LongueurMoyenneDoc(self):
        longueur=0
        for doc in self.production:
            longueur+=len(doc[self.ndoc])
        return longueur/self.ndoc
