
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# UndeepReverBlue

Notre intelligence artificielle agit différemment en fonction de l'état du jeu.

Nous séparons le début de la partie ( <= 12 jetons posés), la fin de la partie (~15 cellules libres) et le reste.

### Début de Partie
Durant le début de la partie, nous avons choisi d'utiliser les Opening Move. Ceux-ci ont été récupérés depuis un site les listant intégralement, qui ont ensuite été convertis pour un board en 10x10 et ajouté à un filtre de Bloom à l'aide d'une fonction de Hashage custom. Si un board est trouvé dans le filtre, alors nous récupérons ce mouvement et le jouons.

### Milieu de Partie
Pour le mid-game, nous utilisons un algorithme Alpha-Beta. Dans le cas d'un processeur sur plusieurs coeurs, nous pourrions augmenter la profondeur. Cependant, du fait des conditions d'évaluations, nous devons le laisser en séquentiel avec une profondeur moindre.

Une documentation plus détaillée des fonctionnalités se trouve dans le code source. 
cf: intelligence.movemanager.AlphaBeta

### Fin de Partie

En fin de partie, le nombre de mouvements possible diminue. Grâce à cela, nous pouvons indiquer à notre algorithme qu'il peut aller plus profondément dans l'arbre des coups possibles.

Un résumé détaillé se trouve dans la documentation du code au niveau du player
(myPlayer ou player.ai.AlphaBetaPlayer)


## Heuristiques
- Mobilty : limite le nombre de movements legals 
- corner : les disques sur les 4 coins avec un poids tres important 
- stability : les diques qui ne peuvent plus retourner durant la partie, avec un poids important aussi - nombre de disques : le nombre de disque sur le board, un poids important vers le lara game 
-  parity : le joeur qui joue le derniere coup est en avantage 
-  staticboardScore : evaluer le board par rapport au table de poids et selon les joueurs
