from binom import*
from tkinter import*
from tkinter import *
import matplotlib
from matplotlib.pyplot import text

from binom import calcul
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from bernouTree import *

introText = "Cet outil permet d'exploiter \n les structures arborescentes pour \n exploiter des problèmes mathématiques. \n Choisissez votre situation:"
menuBernTreeText = "Veuillez renseigner N et P \n pour générer un arbre représentant \n un schéma de Bernoulli à N répétition \n et P la probabilité d'un succès"
class App():

    def __init__(self):
        """
        méthode constructeur qui génère l'attribut central de l'objet: la fenêtre où tout est affiché.
        """
        self.mainWindow = Tk()

    def MainMenu(self):
        """
        une des fonctions de génération d'attributs: elle va créer le menu principal et en faire un attribut pour le garder en mémoire.
        """
        self.TreeImage = PhotoImage(file="menuImage.png") #on transforme l'image à afficher en objet PhotoImage de tkinter
        self.mainMenu = Menu = Frame(self.mainWindow, width=450, height=400)
        
        #on crée les différents éléments de la fenêtre;
        menuIntro = Label(Menu, text = introText, justify='center')
        menuImage = Label(Menu, image=self.TreeImage)
        BinomButton = Button(Menu, text='Binome de Newton', command= lambda: self.ShowBinom()) #le bouton qui permet de manipuler les binômes de Newton
        bernTreeButton = Button(Menu, text='schéma de Bernoulli', command=lambda: self.ShowBernTree()) #celui qui permet de manipuler la loi binomiale

        #on affiche dans la fenêtre les éléments au préalable généré
        menuIntro.grid(rowspan=10, columnspan=10, padx=20, pady=10)
        menuImage.grid(row=11, columnspan=10, padx=50)
        BinomButton.grid(row=12, padx=10, pady=10)
        bernTreeButton.grid(row=12, column=6, padx=10, pady=10)


    def MenuBernTree(self):
        """
        une des fonctions de génération d'attributs: elle va créer le menu de mise en place des probabilités et en faire un attribut pour le garder en mémoire.
        """

        self.menuBernTree = binom = Frame(self.mainWindow, height=400, width=450)
        
        #on crée les différents éléments de la fenêtre;
        labelN = Label(binom,text="valeur de n")
        entryN = Entry(binom) #là où l'utilisateur doit renseigner N
        labelP = Label(binom,text="valeur de p")
        entryP = Entry(binom) #là où l'utilisateur doit renseigner P
        labelExplic = Label(binom, text = menuBernTreeText)
        validButton = Button(binom, text="valider",command= lambda: self.ShowAnalyse()) #le bouton qui bascule sur le menu du graphique
        mainMenuButton = Button(binom, text="retour au menu", command=lambda:self.ShowMenu()) #un retour au menu principal
        quitButton = Button(binom, text="quitter", command = self.mainWindow.destroy)

        #on affiche dans la fenêtre les éléments au préalable généré
        labelN.grid(column=1)
        entryN.grid(row=0,column=2,columnspan=3)
        labelP.grid(row=1, column=1)
        entryP.grid(row=1,column=2,columnspan=3)
        labelExplic.grid(row=0,rowspan=10)
        validButton.grid(row=3,column=2,pady=10)
        mainMenuButton.grid(row=9,column=3)
        quitButton.grid(row=10,column=3)

    def MenuBinom(self):
        """
        une des fonctions de génération d'attributs: elle va créer le menu d'exploitation des binômes de Newton et en faire un attribut pour le garder en mémoire.
        """

        self.menuBinom = Frame(self.mainWindow)
        #les éléments de la fenêtre
        title = Label(self.menuBinom, text="Les binômes de Newton")
        labelExplicBinom = Label(self.menuBinom, text="Cette page sert à décomposer les expressions de type (a+b)^n \n veuillez renseigner ces 3 valeurs dans les champs correspondants.")
        self.A = Entry(self.menuBinom) # A de (A+B)^N
        self.B = Entry(self.menuBinom) # B de (A+B)^N
        self.N = Entry(self.menuBinom) # N de (A+B)^N
        Alabel = Label(self.menuBinom, text='A')
        Blabel = Label(self.menuBinom, text='B')
        Nlabel = Label(self.menuBinom, text='N')
        self.answerLabelBinom = Label(self.menuBinom,text="") #là où sera affichée la formule développée 
        validButton = Button(self.menuBinom, text="valider",command = lambda: self.genBinom()) #bouton qui exploite les valeurs entrées
        goMenu = Button(self.menuBinom,text='retour au menu', command=lambda:self.ShowMenu()) #retour au menu
        quitButton = Button(self.menuBinom,text='quitter', command = self.mainWindow.destroy) #fermeture de la fenêtre
        
        #affichage des éléments dans la fenêtre
        title.grid(row=0, column=1, pady=10)
        labelExplicBinom.grid(row=1, column=1, )
        self.A.grid(row=3, column=0, padx=20, sticky='n')
        self.B.grid(row=3, column=1, sticky='n')
        self.N.grid(row=3, column=2, padx=20, sticky='n')
        Alabel.grid(row=2, column=0, pady=(10,0), sticky='s')
        Blabel.grid(row=2, column=1, pady=(10,0), sticky='s')
        Nlabel.grid(row=2, column=2, pady=(10,0), sticky='s')
        self.answerLabelBinom.grid(row=4, column=1, pady=10)
        validButton.grid(row=5, column=1, pady=(0,10), sticky='s')
        goMenu.grid(row=6, column=1, sticky='n')
        quitButton.grid(row=7,column=1, pady=(0,10), sticky='n')

    def MenuAnalyse(self):
        """
        une des fonctions de génération d'attributs: elle va créer le menu d'exploitation des binômes de Newton et en faire un attribut pour le garder en mémoire.
        """
        self.menuAnalyse = fenetreAnalyse = Frame(self.mainWindow)
        
        #la figure, là où sera affichée le graphique
        f = Figure(figsize=(5,5), dpi=100)
        f.patch.set_facecolor((16/17, 16/17, 16/17)) #la même couleur que Tkinter de base (plutôt qu'être en rgb basique soit sur 255, elle est ramené à une fraction entre 0 et 1)

        self.canvasAnalyse = FigureCanvasTkAgg(f, fenetreAnalyse) #le canvas un peu spécial où sera affiché notre graphique (il vient de matplotlib et facilite l'affichage d'un graphique)
        self.ax = f.add_subplot(111) #le graphique en lui-même
        #les 2 éléments précédents sont en attribut car on les manipulera à chaque calcul

        #les autres éléments
        researchLabel = Label(fenetreAnalyse, text = "rechercher une probabilité")
        self.entry = Entry(fenetreAnalyse) #on passe en attribut tout ce qu'on va manipuler pour faciliter l'exploitation
        Xal = Button(fenetreAnalyse, text = 'X = ', command = lambda: self.XAL()) #bouton pour trouver (P(X=M))
        Xferior = Button(fenetreAnalyse, text = 'X <=', command = lambda: self.XFERIOR()) #bouton pour P(X<=M)
        quitAnalyse = Button(fenetreAnalyse, text='quitter',command=self.mainWindow.destroy)
        self.answerLabel = Label(fenetreAnalyse,text ="")
        goBack = Button(fenetreAnalyse,text = "accueil", command= lambda: self.ShowBernTree()) #retour à la génération de l'arbre
        self.explicLabel = Label(fenetreAnalyse, text="\n\n\n")
        self.hopeLabel = Label(fenetreAnalyse, text="azerty")
        maxButton = Button(fenetreAnalyse, text="max", command=lambda: self.XMAX())
        self.canvasAnalyse.get_tk_widget().grid(row = 0, column = 0,rowspan=100)
        researchLabel.grid(row = 0, column = 1,columnspan=2)
        self.entry.grid(row=1, column = 1, columnspan = 2)
        Xal.grid(row=2, column=1)
        Xferior.grid(row = 2, column=2)
        quitAnalyse.grid(row = 99,column = 2, sticky="e")
        self.answerLabel.grid(row = 3, column = 1, columnspan=2)
        goBack.grid(row=98,column=2, sticky="e")
        self.explicLabel.grid(row = 6, column = 1, columnspan= 2, padx=10)
        self.hopeLabel.grid(row = 8, column = 1, columnspan= 2)
        maxButton.grid(row = 10, column = 1)


    def allGrid(self):
        """
            par sécurité, on retire tous les attributs 'Frame' de la fenêtre principale
        """
        self.mainMenu.grid_remove()
        self.menuAnalyse.grid_remove()
        self.menuBinom.grid_remove()
        self.menuBernTree.grid_remove()


    def Run(self):
        """
        fonction centrale: on génère tous les attributs menus, on affiche le menu central puis on initialise la mainloop()
        """
        self.MainMenu()
        self.MenuBernTree()
        self.MenuAnalyse()
        self.MenuBinom()
        self.ShowMenu()
        self.mainWindow.mainloop()


    def ShowMenu(self):
        """
        une des fonctions d'affichage de menu. on les cache tous puis on affiche le menu principal
        """
        self.allGrid()
        self.mainMenu.grid()

    def ShowBinom(self):
        """
        une des fonctions d'affichage de menu. on les cache tous puis on affiche le menu principal de l'arbre
        """
        self.allGrid()
        self.menuBinom.grid()

    def genGraphe(self,Color):
        """
            fonction qui va générer un graphe à partir des probas de notre arbre en attribuant à chaque barre du graphique une couleur de la liste (pour avoir des barres de couleurs spéciales)
        """
        self.ax.clear() #on vide le graphique
        self.ax.set_title('les différentes probabilités') #on définit son titre
        self.ax.bar([x for x in range(len(self.listeProba))],self.listeProba, color = Color) #on génère le graphique
        self.canvasAnalyse.draw() #on actualise canvasAnalyse avec notre nouveau graphique


    def ShowAnalyse(self):
        """
        une des fonctions d'affichage de menu. on les cache tous puis on affiche le menu d'exploitation de l'arbre
        """
        while True: #boucle pour sécuriser le programme
            try:
                
                N,P = None,None        
                N,P = int(self.menuBernTree.winfo_children()[1].get()),float(self.menuBernTree.winfo_children()[3].get()) #on doit récuperer les valeurs des 2 entrées du menu de génération d'arbre.
                for i in self.menuAnalyse.winfo_children(): #on supprime le contenu des entrées (on le fait avec une boucle pour varier un peu)
                    if i.widgetName == 'entry':
                        i.delete(0,"end")

                #on prépare les éléments de la fenêtre analyse en effaçant les textes déjà existant (potentiellement)
                self.answerLabel.configure(text="")
                self.explicLabel.config(text="\n\n\n")
                self.hopeLabel.config(text="")

                self.epreuve = Epreuve(P,N) # on génère notre épreuve
                self.listeProba = listProba(self.epreuve) # on récupère les probabilités de l'épreuve

                #on génère les affichages (les textes)
                self.explicLabel.configure(text = "arbre de {} répétitions \n probabilité de succès: {} \n\n X suit B({},{})".format(N,P,N,P))
                self.hopeLabel.configure(text="E(x) = {} : \n on a donc une expérience {}".format(round(getEsperance(self.epreuve),6),"favorable" if getEsperance(self.epreuve) > 0 else "défavorable" ))
                
                #on génère notre graphique (toutes les colonnes en bleu car on a pas encore fait de recherche)
                self.genGraphe(["blue" for i in range(len(self.listeProba))])

                #affichage classique, on cache toute fenêtre préalable pour afficher celle-ci
                self.allGrid()
                self.menuAnalyse.grid()
                return True #on brise la boucle
            except ValueError: #si les 2 entrées ne sont pas convertibles en chiffre; on indique une erreur
                if type(N) != 'int':
                    self.menuBernTree.winfo_children()[1].delete(0,"end")
                    self.menuBernTree.winfo_children()[1].insert(0,'valeur invalide')
                if type(P) != 'float':
                    self.menuBernTree.winfo_children()[3].delete(0,"end")
                    self.menuBernTree.winfo_children()[3].insert(0,'valeur invalide')

                return False #on brise la  boucle
                        


    def ShowBernTree(self):
        """
            fonction d'affichage du menu de génération d'arbre
        """
        self.allGrid()
        for i in self.menuBernTree.winfo_children(): #on supprime au préalable le contenu potentiel des entrées de la fenêtre
            if i.widgetName == 'entry':
                i.delete(0,"end")
        self.menuBernTree.grid()


    def XMAX(self):
        """
        fonction associée à un bouton du menu d'analyse qui récupère la proba maximum de l'épreuve
        """
        maxProb = max(self.listeProba) #on récupère la proba max
        M = self.listeProba.index(maxProb) #et le M qui y est associé
        self.answerLabel.configure(text = "la probabilité maximale est \n celle d'avoir {} succès. elle est de {}".format(M, round(maxProb,6))) #on l'affiche
        self.genGraphe(self.color(M)) #puis on colore la colonne M du graphe en orange
        self.entry.delete(0,"end") 
        self.entry.insert(0,M) #on insère M dans l'entrée au préalable vidée

    def XAL(self):
        """
        fonction associé au menu d'analyse qui affiche P(X=M)
        """
        while True:
            try:
                M = int(self.entry.get())
                if M < 0:
                    raise ValueError
                self.menuAnalyse.winfo_children()[6].configure(text = "P(X={}) = {}\n\n".format(M,round(self.listeProba[M],6))) #on affiche la proba recherchée (arrondi à cause des problèmes du binaire)
                self.genGraphe(self.color(M)) #puis on colore la colonne M du graphe en orange 
                return True
            except ValueError: #si on a pas entré un entier naturel:
                self.entry.delete(0,"end")
                self.entry.insert(0,'valeur invalide') #on l'indique
                return False

    def XFERIOR(self):
        """
        fonction associé au menu d'analyse qui affiche P(X=M)
        """
        while True:
            try:
                M = int(self.entry.get())
                if M < 0:
                            raise ValueError
                proba = self.listeProba[M]
                for i in range(0,M):
                    proba+= self.listeProba[i]
                self.answerLabel.configure(text = "P(X<={}) = {}\n\n".format(M,round(proba,6))) #on affiche la proba recherchée (arrondi à cause des problèmes du binaire)
                self.genGraphe(self.multipleColors(M)) #puis on colore les colonnes inférieures ou égales à M du graphe en orange 
                return True
            except ValueError: #si on a pas entré un entier naturel:
                self.entry.delete(0,"end")
                self.entry.insert(0,'valeur invalide') #on l'indique
                return False

    def color(self,x):
        """
            fonction qui renvoie une liste de couleur pour le graphique, la couleur recherchée étant en orange
        """
        color = []
        for i in range(len(self.listeProba)):
            if i == x:
                color.append('orange')
            else:
                color.append('blue')
        return color

    def multipleColors(self,x):
        """
            fonction qui renvoie une liste de couleur pour le graphique, les couleurs inférieures ou égale à la valeur renseignée étant en orange
        """
        color = []
        for i in range(len(self.listeProba)):
            if i <= x:
                color.append('orange')
            else:
                color.append('blue')
        return color

    def genBinom(self):
        """
        on récupère les 3 entrées A,B et N puis on développe l'exppression (A+B)^N
        """
        A = int(self.A.get())
        B= int(self.B.get())
        N = int(self.N.get())
        self.answerLabelBinom.config(text="{} = {}".format(calcul(Binome(A,B,N))[0],calcul(Binome(A,B,N))[1]))
