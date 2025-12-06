# Modélisation, Graphes et Algorithmes Projet : calcul d’un couplage dans un graphe biparti

>- Joachim Larrouy [joachim.larrouy@etu.univ-orleans.fr](mailto:nathan.rissot@etu.univ-orleans.fr)
>- Nathan Rissot [nathan.rissot@etu.univ-orleans.fr](mailto:nathan.rissot@etu.univ-orleans.fr)

## Questions

**Question 1** *Expliquez pourquoi le graphe représentant l’échiquier mutilé est un graphe biparti*.

<!-- Un echiquier est 2-colorable, le graphe représentant l'échiquier est donc 2-colorable, un graphe est bipartite ssi il est 2-colorables, ce graphe est donc bipartite. CF : "Bipartite Graphs and their Applications", Cambridge Tracts in Mathematics, Cambridge University Press, vol. 131, 1998 (ISBN 9780521593458) -->

Soit le graphe $G=(V, E)$ representant l'échiquier tel qu'indiqué dans l'énoncé. Soit deux ensembles $N$ et $B$ tel que $V = N \biguplus B$, chaque sommet representant une case noire (resp. blanche) est placé dans l'ensemble $N$ (resp. $B$).

Chaque arête de $E$ représente une présence des cases représentées par les sommets dans le voisinnage l'une de l'autre, comme chaque case de l'échiquier (mutilé ou non) ne peut être adjacente qu'a des cases de l'autre couleur, les sommets du graphe ne peuvent eux aussi n'êtres adjacent qu'a des sommets représentant des cases de l'autre couleur.

(Bonus: le graphe $G$ est 2-colorable, ce qui est évident sachant qu'il est bipartite, une bipartition etant équivalente à une 2-coloration.)

Donc $\nexists (v_1, v_2) \in E \text{ tq } v_1, v_2 \in B$ et $\nexists (v_1, v_2) \in E \text{ tq }  v_1, v_2 \in N$, la séparation des ensembles entre $N$ et $B$ est donc bien une bipartion du graphe.

**Question 2** *Montrez que ce graphe contient au plus 2n arêtes, où n est le nombre de cases de l’échiquier mutilé.*

On note $n_{i,j}$ le sommet du graphe représentant la case de l'échiquier aux coordonnées $i,j$ et soit $m$ le nombre d'arêtes de $G$ ($m = |E|$).

Nous cherchons a reconstruire un graphe mutilé en ajoutant une par une les cases. Pour cela on choisis de les ajouters dans l'ordre suivant : soit $n_{i,j}$ la dernière case ajoutée et on ajoute $n'_{i',j'}$ tel que $min(j') > j$ et $i'=i$ si aucune case ne respect ces propriété dans notre échiquier, alors on choisis la case respectant $min(i') > i$; $min(j')$  sinon. (ie. la case la plus en haut a gauche n'ayant pas encore été ajoutée.)

<u><b>Cas de base</b></u> : Prenons un échiquier contenant une seule case, ce graphe respecte bien la propriétée $m = 0 \le 2n = 2$

<u><b>Récurrence</b></u> : Prenons un échiquier mutilé de taille $N - 1$, auquel on veut rajouter une case $n_{i',j'}$. Par hypothèse de récurrence, il possède la propriété : $(m - 2) \le 2(n - 1) $.

Rajoutons cette case. De par notre méthode de construction : cette nouvelle case peut avoir pour voisins $n_{i'-1,j'}$ ou $n_{i', j'-1}$. On ajoute donc au maximum 2 arrêtes si ces deux voisins existent. ce qui nous donne donc $(m-2)+2\le 2(n - 1) + 1$. On a bien : $m \le 2n$

**Question 3** *Expliquez en quoi un couplage parfait, dans le graphe représentant l’échiquier mutilé, est utile pour le paver des dominos.*

Chaque arête de $E$ represente une paire de cases adjacentes de l'échiquier. Un couplage est un sous ensemble de $E$, c'est a dire une collection de paires de cases adjacentes, ne se chevauchant pas les unes les autres.

Un couplage parfait est donc une collection de paire de cases adjacentes telles que toutes les cases soient incluses, sans qu'il y-ait de de chevauchement.

Une collection de paire de cases adjacentes telles que toute les cases soient couvertes sans chevauchement est un pavage avec des dominos.

