
########## COLORATION DE GRAPHES ##########

"""
on execute == gophersat fich.cnf
pour compter le nombre de modèle == gophersat -count fich.cnf
"""


# clause = []  # clause =[]
clauses = [] # clauses = [clause, clause ...]


colors, nodes = [], []

nc = int(input("\n Entrez le nombre de couleurs : "))
ns = int(input("\n Entrez le nombre de noeuds : "))

nodes = list(range(1,ns+1))

for i in range(nc):
    print("\n Entrez la couleur", i+1,": ",end="")
    color = input()
    colors.append(color)

print("\n couleurs = ",colors, "\n sommets = ",nodes)


# exemple pour un graphe à 3 sommets
#colors = ["R","G", "B"]
#nodes = [1, 2, 3]   #



def genCnf(nodes, colors):
    # Chaque sommet doit être colorié par une couleur = 1 clause par sommet
    for n in nodes:
        clause = []
        for c in colors:
            clause.append(str(str(n)+c))
        clauses.append(clause)
    # Chaque sommet ne peut être colorié qu'avec une seule couleur = 3 clauses par sommet
    clause =[]
    for n in nodes:
        clause = []
        for c1 in colors:
            clause = []
            for c2 in colors:
                clause = []
                # éviter les doublons
                if c1 != c2 and [str(str(-n)+c2),str(str(-n)+c1)] not in clauses:
                    clause.append(str(str(-n)+c1))
                    clause.append(str(str(-n)+c2))
                    clauses.append(clause)
    # 2 sommets voisins n'ont pas la même couleur = 3 clauses par couleur
    clause =[]
    for c in colors:
        clause = []
        for n1 in nodes:
            clause = []
            for n2 in nodes:
                clause = []
                # éviter les doublons
                if n1 != n2 and [str(str(-n2)+c),str(str(-n1)+c)] not in clauses:
                    clause.append(str(str(-n1)+c))
                    clause.append(str(str(-n2)+c))
                    clauses.append(clause)

    return clauses



# permet de générer les valeurs associées aux différentes variables pour le fichier dimacs
def variablesDico(nodes, colors):
    i = 1
    d = dict()
    for n in nodes:
        for c in colors:
            d[str(str(n)+c)] = i
            d[str(str(-n)+c)] = -i
            i +=1
    return d


########## FICHIER DIMACS ##########


def genFichier(nodes, colors):
    # dico contenant les valeurs correspondantes aux variables
    dico = variablesDico(nodes, colors)

    # pour récupérer les clauses
    clauses = genCnf(nodes, colors)

    # nom du fichier à créer
    name = input("\n Entrer le nom du fichier pour enregistrer les clauses : ")
    name += ".cnf"

    # création et ouverture du fichier en écriture
    name = 'documents/school/utc/sem02/ia02/tp/tp2_SAT_solvers/' + name
    file = open(name, 'w')

    # écriture des commentaires
    file.write("c\nc Fichier Dimacs ")
    file.write(name)
    file.write("\nc")

    #écritures du nombre de variables | nombre de clauses
    file.write("\np cnf ")
    file.write(str(len(nodes)*len(colors))+" ")
    file.write(str(len(clauses)) + "\n")

    # écriture des valeurs correspondantes aux variables
    for c in clauses:
        for var in c:
            file.write(str(dico[var])+" ")
        file.write("0\n")

    # fermeture du fichier
    file.close()


genFichier(nodes, colors)


"""
nombre de modèles :

--- 4 pour 2 couleurs et 2 sommets
--- 0 pour 2 couleurs et 3 sommets
--- 6 pour 3 couleurs et 2 sommets
--- 6 pour 3 couleurs et 3 sommets

--- 0 pour 3 couleurs et 10 sommets
--- 0 pour 4 couleurs et 10 sommets
--- 0 pour 5 couleurs et 10 sommets
--- 0 pour 6 couleurs et 10 sommets
--- 0 pour 7 couleurs et 10 sommets
--- 0 pour 8 couleurs et 10 sommets
--- 0 pour 9 couleurs et 10 sommets

--- 3628800 pour 10 couleurs et 10 sommets

On peut conclure qu'il n'y a aucune façon de colorier un graphe lorsque le nombre
de couleur < nombre de sommet

Quand le nombre de couleurs n = nombre de sommets il y'a alors n! façons de
colorier le graphe (n! modèles)
"""