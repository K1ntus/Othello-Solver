# UndeepReverBlue


Notre intelligence artificielle agit diff�remment en fonction de l'�tat du jeu.

Nous s�parons le d�but de la partie ( <= 12 jetons pos�s), la fin de la partie (~15 cellules libres) et le reste.

### D�but de Partie
Durant le d�but de la partie, nous avons choisi d'utiliser les Opening Move. Ceux-ci ont �t� r�cup�r�s depuis un site les listant int�gralement, qui ont ensuite �t� convertis pour un board en 10x10 et ajout� � un filtre de Bloom � l'aide d'une fonction de Hashage custom. Si un board est trouv� dans le filtre, alors nous r�cup�rons ce mouvement et le jouons.

### Milieu de Partie
Pour le mid-game, nous utilisons un algorithme Alpha-Beta. Dans le cas d'un processeur sur plusieurs coeurs, nous pourrions augmenter la profondeur. Cependant, du fait des conditions d'�valuations, nous devons le laisser en s�quentiel avec une profondeur moindre.

Une documentation plus d�taill�e des fonctionnalit�s se trouve dans le code source. 
cf: intelligence.movemanager.AlphaBeta

### Fin de Partie

En fin de partie, le nombre de mouvements possible diminue. Gr�ce � cela, nous pouvons indiquer � notre algorithme qu'il peut aller plus profond�ment dans l'arbre des coups possibles.

Un r�sum� d�taill� se trouve dans la documentation du code au niveau du player
(myPlayer ou player.ai.AlphaBetaPlayer)


## Heuristiques
- Mobilty : limite le nombre de movements legals 
- corner : les disques sur les 4 coins avec un poids tres important 
- stability : les diques qui ne peuvent plus retourner durant la partie, avec un poids important aussi - nombre de disques : le nombre de disque sur le board, un poids important vers le lara game 
-  parity : le joeur qui joue le derniere coup est en avantage 
-  staticboardScore : evaluer le board par rapport au table de poids et selon les joueurs
