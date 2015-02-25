# Problème du voyageur du commerce
Par Kevin Baland, Gary Marigliano et Christophe Bolinhas


## Introduction

Le problème du voyageur de commerce consiste à calculer le chemin minimal afin de visiter n villes. Chaque solution de ce problème consiste donc en une liste indiquant l'ordre dans lequel le voyageur devra parcourir ces villes.

Les algorithmes génétiques sont utilisé dans le cadre de ce problème afin de résoudre le problème de la génération de toutes les solutions possible lorsque il y en a beaucoup trop. 

## Implémentations

### Génération de la population initiale
On shuffle plusieurs fois la liste de ville fournie initialement

### Sélection 
Voici les différentes méthodes que nous avons implémenté pour la sélection :
1) Sélection statistique avec 19/20 de la moyenne de la distance de nos solution. Problème : Trop grande population sélectionnée sur les grands problèmes.
2) Sélection par ranking, en sélectionnant les N meilleurs éléments de la population.
3) Sélection par random, en sélectionnant N éléments


Notre sélection s'effectue dans l'ordre suivant :

Sélection des éléments étant meilleurs que la moyenne
Sélection des meilleurs éléments de cette liste
Sélection d'éléments aléatoire de la population

### Croisements
Voici la méthode de croisement implémenté :
Pour chaque solution de notre population sélectionnée, on les paires par deux et on les croise ensemble afin de réaliser un enfant. Pour ce faire, on part de la première valeur d'un parent et on avance dans les deux solution en sélectionnant le prochain élément en fonction de la distance à son précédent. Si l'élément est déjà dans la nouvelle solution, on sélectionne un élément manquant au hasard.
Nous avons également tenté d'intégrer l'algorithme subtour indiqué dans un document du cours, mais celui-ci était moins efficace pour nous.


### Mutation

Pour la mutation, on part de la population générée par le croisement. Chaque solution à un pourcentage X d'avoir une mutation, puis chaque ville de l'élément en cours de mutation à Y% de chance d'être échangé avec un autre (aléatoire)
Une deuxième mutation implémentée est le décalage de l'ordre des villes afin de corriger la faiblesse de convergence dû à notre méthode de croisement

### Meilleure solution

Après avoir réalisé ces étapes, on sélectionne la meilleure solution de notre population et on refait ces étapes.

## Conclusion

Après une implémentation correcte et fonctionnelle du TP, voici les constats que nous pouvons faire :
	- Le voyageur de commerce permet bien de converger vers une solution optimale au fur et à mesure que plus de temps lui est fourni. On constate bien ce comportement lors de l'utilisation de beaucoup de données. 
	- Les algorithmes implémentés varient grandement les performances et le résultat final obtenu.