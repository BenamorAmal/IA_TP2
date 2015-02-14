# -*- coding: utf-8 -*-
import optparse
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

	if filename is None:
		cities = getCitiesFromGUI()
	else:
		cities = parseCitiesFromFile(filename)

	# début de l'algorithme
	population = generatePopulation(cities, N)

	while time.time() - startTime < maxtime:
		selected = selection(population)

		crossed = crossover(selected)


		# print("mutation: %s" % mutation(crossed))
		# print("crossed %s: " % crossed)
		# print("selected %s: " % selected)
		pop1 = mutation(crossed)
		pop1.extend(crossed)
		# print("pop1 %s: " % pop1)
		pop1.extend(selected)
		population = pop1
	bestSolution = population[0]

	for solution in population:
		if solution.evaluation < bestSolution.evaluation:
			bestSolution = solution

	print("bestSolution: %s" % bestSolution)

	lenght = 0
	path = "toto"
	return lenght, path

def mutateSolution(solution):
	newSolution = copy.deepcopy(solution)
	for i in range(len(newSolution)):

		prob = randrange(100)
		if prob <= SWAP_PROB:
			swapTarget = randrange(len(solution))
			print("swapTarget: %s" % swapTarget)
			newSolution[i], newSolution[swapTarget] = newSolution[swapTarget], newSolution[i]
	return newSolution




def mutation(population):
	mutatedPopulation = []
	for solution in population:
		prob = randrange(100)
		if  prob < MUTATION_PROB:
			mutatedPopulation.append(mutateSolution(solution))
	return mutatedPopulation



def generatePopulation(cities, n):
	i = 0
	population = []
	while i < n:
		path = generateRandomPath(cities)
		population.append(path)
		i+=1
	# print(population)
	return population


def generateRandomPath(cities):
	"""
	:param cities:
	:return: a path like this: "1-5-6-4" as Solution object
	"""
	nbCities = len(cities)
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
		if solution.evaluation >= average:
			selected.append(solution)

	return selected

def crossover(population):
	"""
	croisement en un points
	"""

	crossed = []

	for i in range(0,len(population)//2, 2):
		parent1 = population[i]
		parent2 = population[i+1]
		child = []
		child.append(parent1[0])

		for value in range(1,len(parent1)):
			distance1 = getPythagoreDistance(child[-1],parent1[value])
			distance2 = getPythagoreDistance(child[-1],parent2[value])

			if distance1 < distance2:
				first, second = parent1[value], parent2[value]
			else:
				first, second = parent2[value], parent1[value]

			if (first not in child) :
				child.append(first)
			elif (second not in child) :
				child.append(second)
			else :
				#TODO Ameliorer Temps
				idx = randrange(len(parent1))
				city = parent1[idx]
				while city in child:
					idx = randrange(len(parent1))
					city = parent1[idx]
				child.append(city)

		crossed.append(Solution(child))

	# Ajout Dernier Parent si liste Impair
	if len(population)%2 == 1:
		crossed.append(Solution(population[-1]))

	return crossed




def parseCitiesFromFile(filename):
	cities = []
	with open(filename, encoding="utf-8", mode="r") as f:
		for line in f:
			name, x, y = line.split(" ")
			cities.append(City(int(x), int(y), name))
	return cities

def getCitiesFromGUI():
	return GUI_example.getCitiesPoints()

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('--nogui', action="store_true", default=False)
	parser.add_option('--maxtime', action="store", type="int", default=1)

	(opts, args) = parser.parse_args()

	nogui = opts.__dict__["nogui"]
	maxtime = opts.__dict__["maxtime"]
	filename = args[0] if len(args) > 0 else None

	# print(nogui)
	# print(maxtime)
	# print(filename)

	## affichage en "temps réel" de l'évolution du meilleur chemin
	ga_solve(filename, not nogui, maxtime)

	# cities = []
	# c1 = City(0, 0)
	# c2 = City(0, 5)
	# c3 = City(0, 10)
	# c4 = City(0, 15)
	# cities.append(c1)
	# cities.append(c2)
	# cities.append(c3)
	# cities.append(c4)
	#
	# solution = Solution(cities)

	# a = 0
	# while a < 10:
	# 	#print("solution: %s" % solution)
	# 	solutionMutated = mutateSolution(solution)
	# 	print("solution: %s" % solutionMutated)
	# 	a += 1
