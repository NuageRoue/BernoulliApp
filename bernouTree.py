class Issue():
    """
        une des issues du schéma de Bernoulli. elle comprend comme attributs:
        - un booléen isSuccess (succès ou échec);
        - un float proba (p ou 1 - p)
        - suivant qui contient l'adresse mémoire du schéma suivant (ou None si on est en fin de branche)
        - un tuple contenant la somme des succès y menant
    """

    def __init__(self, isSuccess, p, restant):
        """
            restant désigne le nombre de succès restant à parcourir pour la génération récursive
        """

        # définition des attributs

        #isSuccess, attribut désignant succès ou échec
        self.isSuccess = isSuccess

        #proba, la probabilité d'avoir cette issue
        self.p = p if self.isSuccess else 1 - p

        #génération du schéma suivant (cas d'arrêt)
        self.suivant = None if restant == 0 else Epreuve(p,restant)

    def isSchem(self):
        """
            permet de savoir si le schéma auquel appartient l'issue testée est en bout de branche (une feuille)
        """
        
        return self.suivant == None

class Epreuve():
    """
        une classe représentant une épreuve de Bernoulli, qui peut faire partie d'un schéma de Bernoulli
    """

    def __init__(self,p,repet):
        """
            repet désigne le nombre de répétition: repet est donc supérieur ou égal à 1
        """
        self.Success = Issue(True, p, repet-1)
        self.Failure = Issue(False, p, repet-1)

def parcoursBinom(epreuve, listIssue, listProba, proba, path):
    """
        fonction parcourant un arbre de Bernoulli pour récupérer les probabilités
        d'arriver au bout de chaque branche ainsi que le nombre de branche en fonction du nombre de succès
    """

    success =  epreuve.Success
    failure = epreuve.Failure

    if not success.isSchem(): #si on est pas au bout d'une branche :
        if proba != 0: #c'est-à-dire si on est pas au 1er tour du parcours
            parcoursBinom(success.suivant, listIssue, listProba, proba * success.p, path + 1) #on parcours la suite de la branche "succès" en récupérant la probabilité du noeud actuel
            parcoursBinom(failure.suivant, listIssue, listProba, proba * failure.p, path) #même chose mais pour la branche "échec"
        else:
            parcoursBinom(success.suivant, listIssue, listProba, success.p, path + 1) #même chose, mais comme proba est à 0 on ne peut pas multiplier par success.p donc proba = success.p 
            parcoursBinom(failure.suivant, listIssue, listProba, failure.p, path) #même chose mais avec la branche échec

    else: #si on se trouve au bout d'une branche:
        if path not in listIssue: #si l'échec n'est pas dans les dictionnaires:
            listIssue[path] = 1 #on initie le nombre de branche avec path succès à 1 dans le dictionnaire
            listProba[path] = proba * failure.p #la probabilité d'une branche à path succès est égale à proba, multiplié à la probabilité du noeud échec; on l'ajoute donc à un dictionnaire
        else:
            listIssue[path] += 1 #sinon, on incrémente de 1 le nombre de branche à path succès (car on a donc déjà fait l'étape précédente)
        
        if path+1 not in listIssue: #même chose pour path+1, soit le noeud succès
            listIssue[path+1] = 1
            listProba[path+1] = proba * success.p
        else:
            listIssue[path+1] += 1

    return listIssue,listProba


def initParcours(arbre):
    return parcoursBinom(arbre,{},{},0,0)

def Pdf(m,arbre):
    """
        probabilité d'avoir m succès dans l'arbre
    """
    branche,proba = initParcours(arbre)
    if m not in branche:
        return 0
    return branche[m] * proba[m]

def binomPdf(m,n,p):
    """
        P(X = m) où X suit B(n,p)
    """
    return Pdf(m,Epreuve(p,n))

def Cdf(m,arbre):
    """
        probabilité d'avoir m succès ou moins dans l'arbre
    """
    branche,proba = initParcours(arbre)
    if m >= max(branche):
        return 1
    elif m < 0:
        return 0
    result = branche[m] * proba[m]
    for i in range(0,m):
        result += branche[i] * proba[i]
    return result

def binomCdf(m,n,p):
    """
        P(X <= m) où X suit B(n,p)
    """
    return Cdf(m,Epreuve(p,n))


def listProba(arbre):
    """
        renvoie la liste complètes des probabilités de l'arbre
    """
    branche, proba = initParcours(arbre)
    listProba = []
    for i in range(len(branche)):
        listProba.append(branche[i] * proba[i])
    return listProba


def esp(arbre,n):
    success = arbre.Success
    if success.isSchem():
        return n * success.p
    return esp(success.suivant, n+1)

def getEsperance(arbre):
    """
        renvoie le nombre de succès moyen après un très grand nombre de répétitions du schéma
    """
    return esp(arbre,1)

    