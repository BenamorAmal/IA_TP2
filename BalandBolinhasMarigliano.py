# -*- coding: utf-8 -*-
import optparse
#from pydoc import GUI
import GUI_example
from City import City
from random import randrange, choice, shuffle
from Solution import Solution, getPythagoreDistance
import time
import copy
from functools import reduce

## Constants
N = 5
MUTATION_PROB = 10
SWAP_PROB = 10

def ga_solve(filename=None, gui=True, maxtime=0):
	## Saisie des villes ou lecture depuis un fichier
	cities = []

	startTime = time.time()
	maxtime = maxtime*0.9
	if filename is None:
		cities = getCitiesFromGUI()
		startTime = time.time()
	else:
		cities = parseCitiesFromFile(filename)

	# début de l'algorithme
	population = generatePopulation(cities, N)

	bestSolution = Solution(population[0])
	if gui:
		GUI_example.showGUI()


	while not isTimeout(startTime, maxtime):
		selected = selection(population)
		if isTimeout(startTime, maxtime):
			break
		crossed = crossover(selected, startTime, maxtime)
		if isTimeout(startTime, maxtime):
			break
		pop1 = mutation(crossed)
		pop1.extend(crossed)
		pop1.extend(selected)
		population = pop1

		for solution in population:

			if isTimeout(startTime, maxtime):
				break
			if solution.evaluation < bestSolution.evaluation:
				bestSolution = solution
		if gui:
			GUI_example.drawPath(bestSolution.getPoints(), bestSolution.evaluation)


	lenght = bestSolution.evaluation
	path = bestSolution.getCities()
	return lenght, path

def isTimeout(startTime, maxTime):
	return time.time() - startTime > maxTime

def mutateSolution(solution):
	newSolution = copy.deepcopy(solution)
	for i in range(len(newSolution)):
		prob = randrange(100)
		if prob <= SWAP_PROB:
			swapTarget = randrange(len(solution))
			newSolution[i], newSolution[swapTarget] = newSolution[swapTarget], newSolution[i]
	newSolution.evaluate()
	return newSolution




def mutation(population):
	mutatedPopulation = []
	for solution in population:
		prob = randrange(100)
		if  prob < MUTATION_PROB:
			mutatedSolution = mutateSolution(solution)
			mutatedPopulation.append(mutatedSolution)
	return mutatedPopulation



def generatePopulation(cities, n):
	i = 0
	population = []
	while i < n:
		path = generateRandomPath(cities)
		population.append(path)
		i+=1
	return population


def generateRandomPath(cities):
	"""
	:param cities:
	:return: a path like this: "1-5-6-4" as Solution object
	"""
	return Solution(scrambled(cities))

def scrambled(orig):
	dest = orig[:]
	shuffle(dest)
	return dest

def selection(population):
	selected = []
	sum = 0

	for solution in population:
		sum += solution.evaluation
	average = sum/len(population)


	for solution in population:
		#-1 Corrige une erreur de suppression de résultats lorsque la moyenne est fixée
		if solution.evaluation >= average/(20*19):
			selected.append(solution)
	return selected

def crossover(population, startTime, maxTime):
	"""
	croisement en un points
	"""

	crossed = []

	for i in range(0,len(population)//2, 2):
		parent1 = population[i]
		parent2 = population[i+1]
		child = Solution([])
		child.add(parent1[0])
		indexList = [x for x in range(len(parent1))]

		if isTimeout(startTime,maxTime):
			break


		for value in range(1,len(parent1)):
			distance1 = getPythagoreDistance(child[-1],parent1[value])
			distance2 = getPythagoreDistance(child[-1],parent2[value])

			if distance1 < distance2:
				first, second = parent1[value], parent2[value]
			else:
				first, second = parent2[value], parent1[value]

			if not child.contains(first):
				child.add(first)
			elif not child.contains(second) :
				child.add(second)
			else :
				idx = choiceAndRemove(indexList)
				city = parent1[idx]
				while city in child:

					idx = choiceAndRemove(indexList)
					city = parent1[idx]
				child.add(city)

		crossed.append(child)

	# Ajout Dernier Parent si liste Impair
	if len(population)%2 == 1:
		crossed.append(Solution(population[-1]))

	return crossed


def choiceAndRemove(indexList):
	choiced = choice(indexList)
	indexList.remove(choiced)
	return choiced

def parseCitiesFromFile(filename):
	cities = []
	with open(filename, encoding="utf-8", mode="r") as f:
		for line in f:
			name, x, y = line.split(" ")
			cities.append(City(int(x), int(y), name))
	return cities

def getCitiesFromGUI():
	GUI_example.showGUI()
	return GUI_example.getCitiesPoints()

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('--nogui', action="store_true", default=False)
	parser.add_option('--maxtime', action="store", type="int", default=10)

	(opts, args) = parser.parse_args()

	nogui = opts.__dict__["nogui"]
	maxtime = opts.__dict__["maxtime"]
	filename = args[0] if len(args) > 0 else None


	## affichage en "temps réel" de l'évolution du meilleur chemin
	ga_solve(filename, not nogui, maxtime)

