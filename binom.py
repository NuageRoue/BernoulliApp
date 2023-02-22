class Node:
    """
        un des éléments du binome de newton. il comprend comme attribut:
        val, sa valeur; next, le prochain binome
    """

    def __init__(self, isA, val, other,repet):
        self.val = val
        if repet >= 0:
            if isA: #cela veut dire que val = A et other = B, utile pour la génération de l'objet Binome
                self.next = Binome(val,other,repet)
            else: #ici c'est l'inverse
                self.next = Binome(other,val,repet)
        else:
            self.next = None #si on est a plus de noeud à générer on ne crée pas d'autre épreuve
    
    def isLeaf(self):
        """
            méthode indiquant si l'on se trouve en bout de branche ou non
        """
        return self.next is None



class Binome:
    """
        objet agrégat caractérisée par ses 2 éléments
    """
    def __init__(self,A,B,exp):
        self.A = Node(True,A,B,exp-1)
        self.B = Node(False,B,A,exp-1)



def parcoursBinome(binom, listBinom,key):
    """
    on parcourt l'arbre généré
    """
    A = binom.A
    B = binom.B
    if not A.isLeaf(): #si on est pas en bout de branche;
        parcoursBinome(A.next, listBinom,key+1) #on parcourt le schéma associé au noeud A
        parcoursBinome(B.next, listBinom,key)#on parcourt le schéma associé au noeud B
    else: #si on est en bout de branche
        if key not in listBinom: #et que la clé n'est pas rencontrée (soit que l'on a pas de branche avec key A)
            listBinom[key] = 1
        else: #sinon on l'incrémente de 1
            listBinom[key] += 1

    return listBinom #on a donc en fin de parcours un dictionnaire qui associe le coefficient binomial de k parmi n (pour k allant de 0 à n) à k (soit la puissance de A)

def calcul(Binom):
    """
        fonction qui renvoie la forme développée d'une expression de la forme (A+B)^N
    """
    listBinom = parcoursBinome(Binom, {},0) #on récupère la liste des coeff binomiaux associés aux k respectifs
    A = Binom.A.val
    B = Binom.B.val
    N = max([key for key in listBinom]) #on a N
    calc = ""
    result = 0
    for i in range(len(listBinom)):
        result += listBinom[i] * A**i * B**(N-i) #on fait la somme de (K,N) * A**K * B**(N-K) pour K allant de 0 à N (mais  dans l'ordre du programme c'est de N à 0)
        calc += " + " + "({} x {}^{} x {}^{})".format(listBinom[i],A,i,B,N-i) #ici, on récupère l'expression sous forme de texte

    return calc[2::], result #on récupère le résultat textuel (on retire les 1ers éléments car se sont des "+")


#pas de tests, ils sont effectuées dans l'application graphique