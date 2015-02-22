# Problème du voyageur du commerce
Par Kevin Baland, Gary Marigliano et Christophe Bolinhas


## Introduction

Le problème du voyageur de commerce consiste à calculer le chemin minimal afin de visiter n villes. Chaque solution de ce problème consiste donc en une liste indiquant l'ordre dans lequel le voyageur devra parcourir ces villes.

Les algorithmes génétiques sont utilisé dans le cadre de ce problème afin de résoudre le problème de la génération de toutes les solutions possible lorsque il y en a beaucoup trop. 

## Implémentations

### Génération de la population initiale
On shuffle plusieurs fois la liste de ville fournie initialement

### Sélection 
Voici comment a été implémenté la sélection :
1) Sélection statistique avec 19/20 de la moyenne de la distance de nos solution. Problème : Trop grande population sélectionnée sur les grands problèmes.
2) Sélection par ranking, en sélectionnant les N meilleurs éléments de la population.
3) Sélection par roulette, tire partie du ranking afin de disposer les solutions sur une surface équivalent à leur valeur et on effectue ensuite un tirage de valeur indiquant quel élément sélectionner.

### Croisements
Voici la méthode de croisement implémenté :
Pour chaque solution de notre population sélectionnée, on les paires par deux et on les croise ensemble afin de réaliser un enfant. Pour ce faire, on part de la première valeur d'un parent et on avance dans les deux solution en sélectionnant le prochain élément en fonction de la distance à son précédent. Si l'élément est déjà dans la nouvelle solution, on sélectionne un élément manquant au hasard.

### Mutation

Pour la mutation, on part de la population générée par le croisement. Chaque solution à un pourcentage X d'avoir une mutation, puis chaque ville de l'élément en cours de mutation à Y% de chance d'être échangé avec un autre (aléatoire)

### Meilleure solution

Après avoir réalisé ces étapes, on sélectionne la meilleure solution de notre population et on refait ces étapes.

## Conclusion

Après une implémentation correcte et fonctionnelle du TP, voici les constats que nous pouvons faire :
	- Le voyageur de commerce permet bien de converger vers une solution optimale au fur et à mesure que plus de temps lui est fourni. On constate bien ce comportement lors de l'utilisation de beaucoup de données. 
	- Les algorithmes implémentés varient grandement les performances et le résultat final obtenu.