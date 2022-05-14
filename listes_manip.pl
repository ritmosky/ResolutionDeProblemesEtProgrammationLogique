
% TD7 LISTES

% + ==> var doit être instanciée avant l'appel
% - ==> var sera unifiée à la fin de l'appel
% ? ==> var peut être instanciée avant ou lors de l'appel

%%%%%%%%%% PREDICATS DE BASE %%%%%%%%%%



%tete(+L, -H) unifie H avec la tête L
tete(L, H) :-
    [H|_] = L.

tete2([T|_], T).


% reste(+L, -R) unifie R avec le reste L
reste([_|Y], Y).

reste2(L, R) :-
    [_|Y] = L,
    R = Y.


% vide(+L) vrai si L vide
vide([]).

vide2(L) :-
    L == [].


% element(?X, ?L) vrai si X est dans L
element(X, [T|_]) :-
    X == T.

element(X, [T|R]) :-
    X \= T,
    element(X, R).


element1(X, L) :-
    tete(L, T),
    X == T.

element1(X, L) :-
    tete(Y,L),
    X \= Y,
    reste(L, R),
    element(X, R).


% dernier(+L, -X) unifie X avec le dernier élément de L 
dernier([X|[]], X).

dernier([_|R], X) :-
    \+vide(R),
    dernier(R,X).


% longueur(+L, -Lg) Lg avec la longueur de L
longueur([], 0).
longueur([_|R], Lg) :-
    longueur(R, N),
    Lg is N+1.
    

% nombre(+L, +X, ?N) nombre d'occurence de X dans L et unifie avec N
nombre([X|_], X, 1).
nombre([T|R], X, N) :-
    X \= T,
    nombre(R, X, M),
    N is M+1.
    

% concat(+L1, +L2, -L3) concatène L1 avec L2 et unifie avec L3
concat([], L2, L2).
concat([T1|R1], L2, [T1|R3]) :-
    concat(R1,L2,R3).
    

% inverse(+L, -R) renvoit R, l’inverse L 
inverse([], []).
inverse([T|R], L) :-
    inverse(R, M), 
    concat(M, [T], L).


% sous_liste(+L1, +L2) verifie que L1 est une sous liste de L2
sous_liste(L1, L2) :-
    concat(L1, _, L2).
    

% retire_element(+L, +X, -R) retire la 1ere occurrence de X dans L et place résultat dans R 
retire_element([],_,[]).
retire_element([X|H], X, H).

retire_element([T|H], X, [T|Rr]) :-
    X =\= T,
    retire_element(H, X, Rr).


    
%%%%%%%%%% Les ensembles %%%%%%%%%%



% retire_elements(+X, +L, -R) retire toutes les occurrences de X dans L et renvoit R
retire_elements(X, L, R) :-
    \+element(X, L),
    R = L.

retire_elements(X, L, R) :-
    element(X, L),
    retire_element(L, X, R1),
    retire_elements(X, R1, R).


% retire_doublons(+L, -E) transforme L en un ensemble E (sans redondance)
retire_doublons([], []).
retire_doublons([T|R], [T|R1]) :-
    retire_elements(T, [T|R], R2),
    retire_doublons(R2, R1).


% union(+E1, +E2, -E) unie ensemble E1 avec E2 et place résultat dans E 
union(E1, E2, E) :-
    concat(E1, E2, E).


% intersection(+E1, +E2, -E) intersection de E1 avec E2 et place résultat dans E 
intersection([], _, []).

intersection([T1|R1], L2, [T1|R]) :-
    element(T1, L2),
    intersection(R1, L2, R).

intersection([T1|R1], L2, E) :-
    \+element(T1, L2),
    intersection(R1, L2, E).



%%%%%%%%%% Tri quicksort en Prolog %%%%%%%%%%



% partition(+X, +L, -L1, -L2) dans L1 les éléments de L <= X ,dans L2 les éléments de L > X
partition(_, [], [], []).

partition(X, [T|R], [T|R1], L2) :-
    X >= T,
    partition(X, R, R1, L2).
    
partition(X, [T|R], L1, [T|R2]) :-
    X < T,
    partition(X, R, L1, R2).   


% tri(+L1, ?L2) trie L1 et unifie résultat avec L2 
tri([], []).
%tri([X,Y], [Y,X]).
tri([T|R], L2) :-
    partition(T, R, G, D),
    tri(G, L3),
    tri(D, L4),
    concat(L3, [T|L4], L2).





   


