

% TD 6 ŒDIPE FAMILY



%  ECRITURE DES REGLES


pere(X, Y) :- homme(X), parent(X, Y).
mere(X, Y) :- femme(X), parent(X, Y).

epoux(X, Y) :- homme(X), couple(X, Y).
epoux(X, Y) :- homme(X), couple(Y, X).

epouse(X, Y) :- femme(X), couple(X, Y).
epouse(X, Y) :- femme(X), couple(Y, X).

fils(X, Y) :- homme(X), parent(Y, X).
fille(X, Y) :- femme(X), parent(Y, X).


enfant(X, Y) :- parent(Y, X).

grandPere(X, Y) :- pere(X, Z), pere(Z, Y).
grandMere(X, Y) :- mere(X, Z), mere(Z, Y).

grandParent(X, Y) :- grandPere(X, Y).
grandParent(X, Y) :- grandMere(X, Y).


petitFils(X, Y) :- homme(X), parent(Z, X), parent(Y, Z).
petitFille(X, Y) :- femme(X), parent(Z, X), parent(Y, Z).



memePere(X, Y) :- pere(Z, X), pere(ZZ, Y), Z=ZZ.
memeMere(X, Y) :- mere(Z, X), mere(ZZ, Y), Z=ZZ.

memeParent(X, Y) :- memePere(X, Y).
memeParent(X, Y) :- memeMere(X, Y).
memeParents(X, Y) :- memePere(X, Y), memeMere(X, Y).

frere(X, Y) :- homme(X), memeParents(X, Y).
soeur(X, Y) :- femme(X), memeParents(X, Y).

demiFrere(X, Y) :- homme(X), memeParent(X,Y), \+(memeParents(X,Y)).
demiSoeur(X, Y) :- femme(X), memeParent(X, Y), \+(memeParents(X,Y)).

oncle(X, Y) :- frere(X, Z), parent(Z, Y).
oncle(X, Y) :- epoux(X, Z), soeur(Z, W), parent(W, Y).

tante(X, Y) :- soeur(X, Z), parent(Z, Y).
tante(X, Y) :- epouse(X, Z), oncle(Z, Y).

neveu(X, Y) :- homme(X), oncle(Y, X).
neveu(X, Y) :- homme(X), tante(Y, X).

niece(X, Y) :- femme(X), oncle(Y, X).
niece(X, Y) :- femme(X), tante(Y, X).

cousin(X, Y) :- fils(X, Z), oncle(Z, Y).
cousin(X, Y) :- fils(X, Z), tante(Z, Y).

cousine(X, Y) :- fille(X, Z), oncle(Z, Y).
cousine(X, Y) :- fille(X, Z), tante(Z, Y).

gendre(X, Y) :- epoux(X, Z), fille(Z, Y).
bru(X, Y) :- epouse(X, Z), fils(Z, Y).

maratre(X, Y) :- epouse(X, Z), pere(Z, Y), \+(mere(X, Y)).

belleMere(X, Y) :- femme(X), bru(Y, X).
belleMere(X, Y) :- femme(X), gendre(Y, X).

beauPere(X, Y) :- homme(X), gendre(Y, X).
beauPere(X, Y) :- homme(X), bru(Y, X).

ascendant(X, Y) :- parent(X, Y).
ascendant(X, Y) :- parent(X, Z), ascendant(Z, Y).

descendant(X, Y) :- ascendant(Y, X).

lignee(X, Y) :- ascendant(X, Y).
lignee(X, Y) :- descendant(X, Y).

parente(X, Y) :- ascendant(Z, X), ascendant(Z, Y), diff(X, Y).



%%%%%%%%%% FAITS %%%%%%%%%%



homme(dionysos).

femme(harmonie).
femme(agavé).
femme(sémélé).
femme(jocaste).
femme(eurydice).
femme(antigone).
femme(ismène).

couple(cadmos, harmonie).
couple(agavé, echion).
couple(zeus, sémélé).
couple(laïos, jocaste).
couple(créon, eurydice).
couple(oedipe, jocaste).

parent(oedipe, etéocle).
parent(jocaste, etéocle).
parent(oedipe, polynice).
parent(jocaste, polynice).
parent(oedipe, antigone).
parent(jocaste, antigone).
parent(oedipe, ismène).
parent(jocaste, ismène).

parent(créon, hémon).
parent(eurydice, hémon).

parent(laïos, oedipe).
parent(jocaste, oedipe).


parent(cadmos, polydore).
parent(harmonie, polydore).
parent(cadmos, sémélé).
parent(harmonie, sémélé).
parent(cadmos, agavé).
parent(harmonie, agavé).

parent(labdacos, laïos).

parent(polydore, labdacos).

parent(ménécée, jocaste).
parent(ménécée, créon).
parent(penthée, ménécée).

parent(agavé, penthée).
parent(echion, penthée).

parent(sémélé, dionysos).
parent(zeus, dionysos).






