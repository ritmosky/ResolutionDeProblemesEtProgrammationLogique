
% l’algorithme de backtracking de Prolog ne permet pas de découvrir des plans
% victorieux de taille 15 ou plus


% PLAN VALIDE
% planValide(Actions, Etats, Longueur

planValide([], [_], 0).
planValide([A|AT], [S1, S2 | ST], N) :-
    N > 0,
    N1 is N-1,
    do(A, S1, S2),
    planValide(AT, [S2 | ST], N1).



% positionRelative(Direction, Case1, Case2) , Direction = up, down, right, left
% case(X,Y) vérifie si la position(X,Y) est une case du plateau 

positionRelative(up, pos(X,Y), pos(X,Y1)) :-
    case(X,Y),
    case(X,Y1),
    Y1 is Y+1.


positionRelative(down, pos(X,Y), pos(X,Y1)) :-
    case(X,Y),
    case(X,Y1),
    Y1 is Y-1.


positionRelative(right, pos(X,Y), pos(X1,Y)) :-
    case(X,Y),
    case(X1,Y),
    X1 is X+1.


positionRelative(left, pos(X,Y), pos(X,Y1)) :-
    case(X,Y),
    case(X1,Y),
    X1 is X-1.



% notIn(X,L) verfie qu'il n'y a pas de case en X

notIn(_,[]).
notIn(X, [H|T]) :- dif(X,H), notIn(X,T).



% trouveEnleve(X,L,L1) s efface ssi L contient X et 
% L1 = liste obtenue en supprimant de L la première occurence de X

 trouveEnleve(X, [X|T], T).
 trouveEnleve(X, [Y|T], [Y|T1]) :-
    dif(X,Y),
    trouveEnleve(X,T,T1).



% actions -> do(Action, EtatOrigine, EtatDestination)
% Fluents : position homme et position des caisses
% Un état -> state(me(X,Y), boxes(L)) avec L la liste des positions des caisses


do(act(move,D),
   state(me(X,Y)  , boxes(L)),
   state(me(X1,Y1), boxes(L))) :-
      positionRelative(D, pos(X,Y), pos(X1,Y1)),
      notIn(pos(X1,Y1), L).


do(act(push,D),
   state(me(X,Y)  , boxes(L)),
   state(me(X1,Y1), boxes(pos(X2,Y2)|L))) :-
      positionRelative(D, pos(X,Y), pos(X1,Y1)),
      positionRelative(D, pos(X1,Y1), pos(X2,Y2)),
      trouveEnleve(pos(X1,Y1),L,L1)
      notIn(pos(X2,Y2), L).




%%%%%%%%%% CONDITIONS DE VICTOIRES %%%%%%%%%%


% état final ssi toutes les caisses sont à des positions cibles (repérées avec target)

allOnTarget([]).
allOnTarget([H|T]) :- target(X), allOnTarget(T).

victory(state(_,boxes(L))) :- allOnTarget(L).




%%%%%%%%%% CARTES %%%%%%%%%%


% niveau décrit par un plateau contenant des cases accessibles, cibles et un état initial

case(2,5). 
case(3,5).
case(X,4) :- between(2,5,X).

target(pos(1,3)).

initial(state(me(2,4), boxes([pos(2,5), pos(3,5)])))



%%%%%%%%%% REQUÊTES %%%%%%%%%%


% trouver plan
% Etats = [X|_], initial(X), planValide(Etats, Actions, 3)


% endsWith(X,L) s efface lorsque L se termine par X

endsWith(X,[X]).
endsWith(X,[_|T]) :- endsWith(X,T).


% trouver plan victorieux
% Etats = [X|_], initial(X),
% planValide(Etats, Actions, 3),
% endsWith(Y,Etats), victory(Y)
