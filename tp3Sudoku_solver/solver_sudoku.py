"""
[IA02] TP SAT/Sudoku template python
author:  Sylvain Lagrue
version: 1.0.2
"""

from typing import List, Tuple
import subprocess


Literal = int
Clause = List[Literal]
Model = List[Literal]
Clause_Base = List[Clause]
Grid = List[List[int]]

grid1 = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


grid2 = [
    [0, 0, 0, 0, 2, 7, 5, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 8, 1, 0, 0, 0, 0],
    [4, 0, 6, 3, 0, 1, 0, 0, 9],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 0, 0, 0, 0, 3, 1, 0],
]


grid3 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]





#### fonctions fournies


def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:].split(" ")

    return True, [int(x) for x in model]




########## FONCTIONS DEFINIES UTILITAIRES ##########


"""
at_least_one = chaque cellule a au moins une valeur -> avec ou (pour abc on a : a v b v c) -> 1 clause par cellule

unique = chaque chiffres apparait une seule fois -> xor (pour abc on a : not(a) v not(b) and not(b) v not(c)) -> combinaison(de 2 dans 9) -> 36 clauses par cellules

on a 37 clauses par cellules donc 37*81 = 2997
"""
#  9 lignes 9 colonnes 9 boxs = 729 variables


# décomposition en base 9
def en_base9(n):
    l = []
    while n != 0 :
        l.append(n%9)
        n//=9
    return l



# coordonnées d’une cellule (entre 0 et 8) et une valeur (entre 1 et 9 inclus) renvoie le numéro de variable correspondant
# cell_to_variable(1, 3, 4) = 112
def cell_to_variable(i, j, val):
    return i*9**2 + j*9 + val



# étant donné un numéro de variable renvoie le triplet ligne/colonne/valeur associé
def variable_to_cell(var):
    var -=1
    x = var // 9**2
    y = (var % 9**2) // 9
    z = (var % 9**2) % 9
    return (x,y,z+1)


variable_to_cell(729) # (8, 8, 9)
variable_to_cell(112) # (1, 3, 4)
variable_to_cell(1) # (0, 0, 1)



########## FONCTIONS DE CONTRAINTES ##########



# at_least_one(vars: List[int]) -> List[int], étant donné une liste de variables propositionnelles, renvoie la clause at_least_one associée


def at_least_one(vars):
    return vars

at_least_one([1, 3, 5]) # [1, 3, 5]




"""unique(vars: List[int]) -> List[List[int]], étant donné une liste de variables propositionnelles, renvoie la base de clauses unique associée.utiliser fonction combinations du package itertools"""


def unique(vars):
    cc=[]
    alo = at_least_one(vars)
    cc.append(alo)
    for i in alo:
        clause = []
        for j in alo:
            clause = []
            if i != j and list((-i, -j)) not in cc and list((-j, -i)) not in cc:
                clause = list((-i, -j))
                cc.append(clause)
    return cc



unique([1, 3, 5]) # [[1, 3, 5], [-1, -3], [-1, -5], [-3, -5]]



########## CONTRAINTES REGLES SUDOKU ##########


# create_cell_constraints() -> List[List[int]] renvoyant une base de clauses représentant la contrainte d’unicité de valeur pour toutes les cellules du Sudoku

def create_cell_constraints(n):  #
    clause = []
    for i in range(0,n):
        for j in range(0,n):
            l = []
            for k in range(1,n+1):
                l.append(cell_to_variable(i, j, k))

            clause += unique(l)

    return clause


create_cell_constraints(3)
# create_cell_constraints(9)



# fonctions renvoyant base de clauses représentant les contraintes sur les lignes, colonnes et carrés du Sudoku


create_line_constraints()
create_column_constraints()
create_box_constraints() # il faut 81




#### fonction principale


def main():
    pass


if __name__ == "__main__":
    main()
