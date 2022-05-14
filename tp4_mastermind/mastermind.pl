% TP 4 Mastermind



% nBienPlace(+Code1, +Code2, -BP)

% condition d'arrêt 
nBienPlace([], [], 0).

% cas si où les têtes sont égales
nBienPlace([A|R1], [A|R2], BP) :-
    nBienPlace(R1, R2, N),
    BP is N+1.

% cas si où les têtes sont différentes
nBienPlace([A1|R1], [A2|R2], BP) :-
    A1\=A2,
    nBienPlace(R1, R2, BP).
    
   

% longueur(+L, -N)
longueur([], 0).
longueur([_|R], N) :-
    longueur(R, M),
    N is M+1.



% gagne(+Code1, +Code2) vérifiant que Code1 = Code2
gagne(C1, C2) :-
    nBienPlace(C1, C2, BP),
    longueur(C1, N),
    N=BP.



% element(+E, +L) vérifie si E appartient à L
element(E, [E|_]).
element(E, [T|R]) :-
    E=\=T,
    element(E,R).



% enleve(+E, +L1, -L2) renvoie L2 = L1 privée de la première occurrence de E
enleve(_, [], []).

enleve(E, [E|R1], R1).

enleve(E, [A1|R1], [A1|L2]) :-
    E=\=A1,
    enleve(E, R1, L2).



% enleveBP(+Code1, +Code2, -Code1Bis, -Code2Bis) CodeiBis renvoit Codei privé des éléments bien placés 
enleveBP([], [], [], []).

enleveBP([A|R1], [A|R2], C1Bis, C2Bis) :-
    enleveBP(R1, R2, C1Bis, C2Bis).

enleveBP([A1|R1], [A2|R2], [A1|R1B], [A2|R2B]) :-
    A1=\=A2,
    enleveBP(R1, R2, R1B, R2B).
    


% nMalPlacesAux(+Code1, +Code2, -MP) avec aucun élément bien placé
nMalPlacesAux([], _, 0).

nMalPlacesAux([A1|R1], L2, MP) :-
    element(A1, L2),
    enleve(A1, L2, L3),
    nMalPlacesAux(R1, L3, MP1),
    MP is MP1+1.

nMalPlacesAux([A1|R1], L2, MP) :-
    \+element(A1, L2),
    nMalPlacesAux(R1, L2, MP).



% nMalPlaces(+Code1, +Code2, -MP) donnent le nombre d’éléments mal placés MP
nMalPlaces([], _, 0).

nMalPlaces([A1|R1], [A1|R2], MP) :-
    nMalPlaces(R1, R2, MP).

nMalPlaces([A1|R1], L2, MP) :-
    \+element(A1, L2),
    nMalPlaces(R1, L2, MP).

nMalPlaces([A1|R1], [A2|R2], MP) :-
    element(A1, [A2|R2]),
    A1=\=A2,
    nMalPlaces(R1, R2, MP1),
    MP is MP1+1.



% codeur(+M, +N, -Code) produit aléatoirement un code de taille 
% N basé sur M couleurs
% random(+Base, +Max, -Number) unifie Number avec un nombre compris 
% entre Base inclus et Max exclu

codeur(_, 0, []).

codeur(M, N, [T|R]) :-
    N > 0,
    Max is M+1,
    random(1, Max, X),
    T=X,
    P is N-1,
    codeur(M, P, R).


% jouons(+M, +N, +Max) permettant de jouer à Mastermind en tant que décodeur
% en choisissant aléatoirement un code de taille N, avec au plus M couleurs différentes
% puis demande à un joueur humain un code
% Ce dernier aura Max essais pour trouver le code
% On pourra s’aider de prédicats auxiliaires pour simplifier le code. 


% initialise le jeu = création du Codeur
start(M, N, C) :-
    codeur(M, N, C),
    format('--- Début de la partie --- ~n~n').


% il y'a fin lorsqu'on a autant de Bien Placé que la taille du Décodeur
fin(L, X) :-
    longueur(L, Y),
    X = Y.
    
    

% déroulement d'un tour de jeu
tour(Code, Max) :-
    format('Il reste ~d coup(s).~n', Max),
    format('Donner un code(Decodeur) : '),
    read(Decodeur),
    nBienPlace(Code, Decodeur, BP),
    nMalPlaces(Code, Decodeur, MP),
    format("BP : ~d / ", BP),
	format("MP : ~d ~n~n", MP),
    fin(Decodeur, BP),
    format(" --- Gagné !!! --- ~n~n").
    


tour(Code, Max) :-
    format('Il reste ~d coup(s).~n', Max),
    format('Donner un code(Decodeur) : '),
    read(Decodeur),
    nBienPlace(Code, Decodeur, BP),
    nMalPlaces(Code, Decodeur, MP),
    format("BP : ~d / ", BP),
	format("MP : ~d ~n~n", MP),
    tour(Code, Max);
    
    

% déroulement du jeu 

jouons(M, N, Max) :-
    Max > 0,
    start(M, N, Codeur),
    tour(Codeur, Max),
    Coup is Max-1.
    



     

    