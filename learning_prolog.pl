
% prédicat factoriel fac(+N, ?Res)
fac(0, 1).
fac(N, Res) :-
	N > 0,
	N2 is N - 1,
	fac(N2, Res2),
	Res is N * Res2.

% fac(5, X).
% fac(5, 120).


%%%%%%%%%%


%
ami(X, Y) :- schtroumpf(X), schtroumpf(Y), dif(X, Y).

ami(johan, pirlouit).
ami(pirlouit, johan).
schtroumpf(grand_schtroumpf).
schtroumpf(coquet).
schtroumpf(costaud).

% ami(costaud,X)
% ami(X, Y).


%%%%%%%%%% PREDICAT !
% Coupe toutes les clauses alternative en dessous de lui
% Coupe toutes les solutions alternatives des sous-buts à gauche cut 
% Possibilité de retour arrière sur les sous-buts à la droite du cut


%
ami2(X, Y) :- schtroumpf2(X), schtroumpf2(Y), dif(X, Y), !.

ami2(johan, pirlouit).
ami2(pirlouit, johan).
schtroumpf2(grand_schtroumpf).
schtroumpf2(coquet).
schtroumpf2(costaud).


%%%%%%%%%%


ami3(X, Y) :- schtroumpf3(X), !, schtroumpf3(Y), dif(X, Y).

ami3(johan, pirlouit).
ami3(pirlouit, johan).
schtroumpf3(grand_schtroumpf).
schtroumpf3(coquet).
schtroumpf3(costaud).

% ami3(X, Y).


%%%%%%%%%%


ami4(X, Y) :- schtroumpf4(X), schtroumpf4(Y), !, dif(X, Y).

ami4(johan, pirlouit).
ami4(pirlouit, johan).
schtroumpf4(grand_schtroumpf).
schtroumpf4(coquet).
schtroumpf4(costaud).


%%%%%%%%%%


% factoriel avec un cut
fac2(0, 1) :- !.
fac2(N, Res) :-
	N2 is N - 1,
  	fac(N2, Res2),
 	Res is N * Res2.

% fac2(5, X).
% fac2(5, 120).


%%%%%%%%%%


% Algorithme général : generate and test
solve(X) :-
	generate(X),
	test(X).


%
couleur(bleu).
couleur(blanc).
couleur(rouge).

% couleur(X).


% member(?E, ?L) liste les éléments de L
% member(X, [1, 2, 3, 4, 10, 12]).


%%%%%%%%%%


commence_par_b(X) :- atom_chars(X, [b|_]).

% atom_chars(blanc, [b|_]).
% commence_par_b(blanc).


% renvoit toutes les couleurs commençant par b
solve1(X) :-
  couleur(X),
  commence_par_b(X).

% solve1(X)


%%%%%%%%%% trouver tous les nombres impairs entre 0 et 100 


% Génèrer tous les nombres entre Min et Max = range(+Min, +Max, -Res)
% cas de base
range(Res, Max, Res) :- Res < Max.

range(Min, Max, Res) :-
    Min < Max,
    Min2 is Min + 1,
    range(Min2, Max, Res).


% Tester la parité = odd(+X) , rem = reste de la division euclidienne
odd(X) :- X2 is X rem 2, X2 =:= 1.


% algo général
solve3(X) :-
	range(0, 101, X), % génération 
    odd(X). % test

% solve3(X).

