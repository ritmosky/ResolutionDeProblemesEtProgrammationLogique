

########## SOKOBAN ##########

from collections import namedtuple


########## DESCRIPTION ##########


# action = un couple (verbe, direction)
Action = namedtuple('action',('verb','direction'))

actions = {d : Action('move',d) for d in 'udrl'} | {d.upper() : Action('move',d) for d in 'udrl'}


"""
- positions sont des couples d’entiers
- fluents => positions des caisses et de l'homme

- état = position du perso et l’ensemble des positions des caisses
"""


# état initial
s0 = {
'me': (2, 2),
'boxes': {(4, 4), (3, 4), (6, 5), (6, 1), (6, 4), (2, 3), (6, 3)}
}


# caractéristiques non-fluantes = mûrs et goals
map_rules = {
'goals': {(7, 4), (2, 1), (6, 6), (5, 4), (6, 3), (4, 1), (3, 5)},
'walls': {(4, 0), (4, 3), (3, 1), (4, 6), (5, 7), (8, 0),
(0, 2), (8, 3), (0, 5), (8, 6), (1, 0), (1, 6), (7, 7), (4, 2),
(3, 0), (5, 0), (5, 6), (3, 6), (8, 2), (8, 5), (1, 2), (0, 4),
(7, 0), (6, 7), (3, 2), (5, 2), (8, 4), (8, 1), (8, 7), (1, 1),
(0, 3), (2, 0), (0, 6), (2, 6), (6, 0)},
'actions': actions
}



########## FONCTIONS INTERMEDIAIRES ##########


# one_step joue le rôle du prédicat positionRelative
def one_step(position, direction) :
    i, j = position
    return {'r': (i,j+1), 'l': (i,j-1), 'u': (i-1,j), 'd': (i+1,j)}[direction]

# représenter les cases accessibles
def free(position) :
    return not(position in map_rules['walls'])



########## do(action, état) ##########

#do_fn(a,state._asdict())

# retourne un nouvel état = fonction et non une procédure
def do_fn(action, state) :
    X0 = state['me']
    boxes = state['boxes']
    X1 = one_step(X0, action.direction)
    if action.verb == 'move' :
        if free(X1) and not (X1 in boxes) :
            return {'me' : X1, 'boxes' : boxes}
        else :
            return None
    if action.verb == 'push' :
        X2 = one_step(X1, action.direction)
        if X1 in boxes and free(X2) and not (X2 in boxes) :
            return {'boxes' : {X2} | boxes - {X1} ,
                    'me' : X1}
        else :
            return None
    return None


# cloner s0 pour ne pas l'écraser
state = {k: v for k,v in s0.items()}
print(0,state)


for a in 'RurrddddlDRuuuuLLLrdRDrddlLdllUUdR' :
   do_inplace(actions[a],state)
   print(a,state)

print(state['boxes'] == map_rules['goals'])



"""
il n’est pas possible d’utiliser une clé mutable dans un dictionnaire
SOLUTION:

- utiliser le transtypage pour utiliser ces types immuables lors du stockage

- représenter les états par un type non-mutable ayant une interface similaire(collections.namedtuple)
->
State = namedtuple('state',('me','boxes'))
state = State(**s0)
print(0,state)
save = {}
for a in 'RurrddddlDRuuuuLLLrdRDrddlLdllUUdR' :
    newstate = State(**do_fn(actions[a],state._asdict()))
    save[state] = newstate
    state = newstate
    print(a,state)

print(state['boxes']==rules['goals'])
"""


State = namedtuple('state',('me','boxes'))
state = State(**s0)



########## ALGORITHME DE RECHERCHE NON INFORMÉE (LARGEUR ##########


def search_with_parent(s0, goals, succ,
                       remove, insert, debug=True) :
    l = [s0]
    save = {s0: None}
    s = s0
    while l:
        if debug:
            print("l =", l)
        s, l = remove(l)
        for s2,a in succ(s).items():
            if not s2 in save:
                save[s2] = (s,a)
                if goals(s2):
                    return s2, save
                insert(s2, l)
    return None, save



def insert_largeur(s, l): # les états sont insérés en queue de file
    l.append(s)
    return l


def remove_largeur(l): # les états sont retirés en tête de file
    return l.pop(0), l


# reconstruit le chemin -> liste de couples (état, action)
def dict2path(s, d):
    l = [(s,None)]
    while not d[s] is None:
        parent, a = d[s]
        l.append((parent,a))
        s = parent
    l.reverse()
    return l


#
def goal_factory(rules) :
    def goals(state) :
        return state.boxes == rules['goals']
    return goals


# succ renvoie un dico (états_suivants, actions_correspondantes)
def succ_factory(rules) :
    def succ(state) :
        l = [(do_fn(a,state._asdict()),a) for a in actions]
        return {State(**x) : a for x,a in l if x}
    return succ



########## EXEMPLES ##########

s_end, save = search_with_parent(s0, goal_factory, succ_factory,
                         remove_largeur, insert_largeur, debug=False)

plan = ''.join([a for s,a in dict2path(s_end,save) if a])


"""plan de longueur 34, presque identique à celui mis en oeuvre dans le gif, après avoir visité 481 975 états intermédiaires"""
