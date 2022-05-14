
########## TP1 IA02 logique propositionnelle et model checking ##########

"""
étant donné une formule donnée en argument et un ensemble de variables propositionnelles, on veut afficher sa table de vérité. On se limite aux connecteurs ∧ = and ∨ = or et ¬ = not
"""

## Q1 Décomposition en binaire en nb_bits


# décompose n en binaire
def en_binaire(n):
    l_bin = []
    while n != 0 :
        l_bin.append(n%2)
        n//=2
    return l_bin


# décompose n en nb_bits booléen
def decomp(n, nb_bits):
    l_bin = []
    while n != 0 :
        if n%2:
            l_bin.append(True)
        else:
            l_bin.append(False)
        n//=2

    if len(l_bin) > nb_bits:
        return f"Il faut au moins {len(l_bin)-nb_bits} bits en plus pour la décomposition !"
    while len(l_bin) < nb_bits:
        l_bin.append(False)
    return l_bin


decomp(3, 4)


## Q2 Interprétation = List[str], List[bool] -> Dict[str, bool]


# Interpretation = dictionnaire associant à chaque variable propositionnelle un booléen
def interpretation(voc, vals):
    if len(voc) != len(vals):
        return f"Erreur ! il faut que les listes aient la m\ême taille"

    dico = dict()
    for i in range(len(vals)):
        dico[voc[i]] = vals[i]
    return dico


interpretation(["A", "B", "C"],[True, True, False])


## Q3 Créer un générateur d’interprétations


# on va generer la liste des booléens avec decomp(i,len(voc))
def genInterpretations(voc):
    for i in range(pow(2,len(voc))):
        vals = decomp(i,len(voc))
        yield interpretation(voc, vals)  # cree les champ d'un générateur


# 1ère façon d'accéder aux différentes valeurs
g = genInterpretations(["A", "B", "C"])
next(g)
next(g)


# 2eme façon d'accéder aux différentes valeurs
for i in genInterpretations(["toto", "tutu"]):
    print(i)



## Q4 Fonction renvoie l'évaluation d'une formule


def valuate(formula, interpretation):
    """for cle in interpretation.keys():
        print(cle, "=", interpretation[cle])
    print("formule = ", formula)"""
    return eval(formula, interpretation)


valuate("(A or B) and not(C)", {"A": True, "B": False, "C": False})



## Q5 génération automatique de tables de vérités


# affiche l'en tête
def en_tete(formula, voc):
    # affiche la formule
    print("\nFORMULE : ", formula.upper(), "\n")

    # pour la ligne d'en tête
    for j in range(len(voc)):
        print("+", end='')
        print("---", end='')
    print("+-------+")
    print("| ", end='')

    # affichage des variables
    for var in voc:
        print(var, end='')
        print(" | ", end='')
    print("eval.", end='')
    print(" | ")

    for j in range(len(voc)):
        print("+", end='')
        print("---", end='')
    print("+-------+")


# pour afficher T si la valeur est True dans le tableau
def t(x):
    return "T" if x else "F"


def table(formula, voc):
    # affiche l'en tête
    en_tete(formula, voc)

    # pour la table
    for dico in genInterpretations(voc): # pour chaque ligne
        print("| ", end='')

        for var in voc:
            # afficher T ou F
            print(t(dico[var]), end='')
            print(" | ", end='')

         # evalution de la formule et affichage
        print(" ", t(valuate(formula, dico)), end='')
        print("   |")

    # les bordures de la fin
    for j in range(len(voc)):
        print("+", end='')
        print("---", end='')
    print("+-------+")


table("A or B", ["A", "B"])
table("A and B", ["A", "B"])
table("(A or B) and not(C)", ["A", "B", "C"])
table("(A or B) and not(C) and D", ["A", "B", "C", "D"])


## Q6 Vérifier si une formule est valide, contradictoire ou contingeante

"""
formule valide = tautologie = toutes les interprétation satisfont la formule (formule vraie pour toutes les interprétation)

formule contradictoire = toutes interprétations falsifient la formule (formule fausse pour toutes les interprétation)

formule contingeante = il existe une interprétation satisfaisant la formule et une interprétation falsifiant la formule

une formule est contingeante si elle n'est ni valide, ni contradictoire

"""

# si on rencontre une evaluation fausse -> formule n'est pas valide
def is_valide(formula, voc):
    for dico in genInterpretations(voc):
        if not valuate(formula, dico):
            return False
    return True


# si on rencontre une evaluation vraie -> formule n'est pas contradictoire
def is_contradictoire(formula, voc):
    for dico in genInterpretations(voc):
        if valuate(formula, dico):
            return False
    return True


# si on rencontre une evaluation vraie et ube fausse -> formule est contingente
def is_contingente(formula, voc):
   return not is_contradictoire(formula, voc) and not is_valide(formula, voc)


is_valide("A and B", ["A", "B"])
is_valide("A and B and C or D and not(E)", ["A", "B", "C", "D", "E"])

is_contradictoire("A and B", ["A", "B"])
is_contradictoire("A and B and C or D and not(E)", ["A", "B", "C", "D", "E"])

is_contingente("A and B", ["A", "B"])
is_contingente("A and B and C or D and not(E)", ["A", "B", "C", "D", "E"])


## Q7 Vérifier si une formule f2 est la conséquence logique de f1 (implication)


# verif f1 -> f2 === si f1=V alors f2 forcément V
# a -> b = not(a) or b
def isCons(f1, f2, voc):
    for dico in genInterpretations(voc):
        eval_f1, eval_f2 = valuate(f1, dico), valuate(f2, dico)
        if eval_f1:
            if not eval_f2 :
                return False
    return True


isCons("A and B", "A or B", ["A", "B"])
isCons("A or B", "A and B", ["A", "B"])



"""
# itérable, itérateur, generateur(sorte d'itérateur)
import sys

yy=[x for x in range(50000)]
sys.getsizeof(yy)  # 444 376

y=(x for x in range(50000))
sys.getsizeof(112)  # 112
"""