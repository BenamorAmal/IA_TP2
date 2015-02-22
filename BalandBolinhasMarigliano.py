# -*- coding: utf-8 -*-
import optparse
# from pydoc import GUI
import GUI_example
from City import City
from random import randrange, choice, shuffle
from Solution import Solution, getPythagoreDistance, getDistanceChessboard, getDistanceManathan
import time
import copy
from functools import reduce

# # Constants
N = 50
MUTATION_PROB = 33
SWAP_PROB = 44
CROSSED_N = 15
RANDOM_N = 10
DECAL_N = 15

def ga_solve(filename=None, gui=True, maxtime=0):
    # # Saisie des villes ou lecture depuis un fichier
    cities = []

    startTime = time.time()
    maxtime = maxtime * 0.9
    if filename is None:
        cities = getCitiesFromGUI()
        startTime = time.time()
    else:
        cities = parseCitiesFromFile(filename)

    # début de l'algorithme
    population = generatePopulation(cities,N)

    bestSolution = Solution(population[0])
    if gui:
        GUI_example.showGUI()

    i = 0
    while not isTimeout(startTime, maxtime):
        selected = selectionRanking(selection(population))
        selected.extend(selectionRandom(population,RANDOM_N))

        if isTimeout(startTime, maxtime):
            break
        crossed = crossover(selected, startTime, maxtime)
        if isTimeout(startTime, maxtime):
            break
        pop1 = mutation(crossed)
        pop1.extend(crossed)
        pop1.extend(selected)
        pop1.extend(decalList(selected))
        #pop1.append(bestSolution)
        population = pop1

        for solution in population:

            if isTimeout(startTime, maxtime):
                break
            if solution.evaluation < bestSolution.evaluation:
                bestSolution = solution
        if gui:
            GUI_example.drawPath(bestSolution.getPoints(), bestSolution.evaluation)

        i+=1

    lenght = bestSolution.evaluation
    path = bestSolution.getCities()

    return lenght, path



def isTimeout(startTime, maxTime):
    return time.time() - startTime > maxTime


def decalList(population):
    decalpopulation = []
    for i in range(DECAL_N):
        solution = choice(population).clone()
        solution.decal(randrange(len(solution)))
        decalpopulation.append(solution)
    return decalpopulation

def mutateSolution(solution):
    newSolution = solution.clone()
    for i in range(len(newSolution)):
        prob = randrange(100)
        if prob <= SWAP_PROB:
            #swapTarget = (i+1) % len(newSolution)
            swapTarget = randrange(len(newSolution))
            # temp = newSolution[swapTarget]
            #newSolution[swapTarget] = newSolution[i]
            #newSolution[i] = temp
            newSolution.swap(i,swapTarget)

            #newSolution[i], newSolution[swapTarget] = newSolution[swapTarget], newSolution[i]
    newSolution.evaluate()
    return newSolution


def mutation(population):
    mutatedPopulation = []
    for solution in population:
        prob = randrange(100)
        if prob < MUTATION_PROB:
            mutatedSolution = mutateSolution(solution)
            mutatedPopulation.append(mutatedSolution)
    return mutatedPopulation


def generatePopulation(cities, n):
    i = 0
    population = []
    while i < n:
        path = generateRandomPath(cities)
        population.append(path)
        i += 1
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
    average = sum / len(population)

    for solution in population:
        # -1 Corrige une erreur de suppression de résultats lorsque la moyenne est fixée
        if solution.evaluation >= average / (20 * 19):
            selected.append(solution)
    return selected


def selectionRanking(population):
    selected = []
    sum = 0

    # NO need copy car utilisation seulement dans cette fonctions
    population = sorted(population, key=lambda k: k.evaluation)

    NSOLUCE = N

    NSOLUCE = min([len(population), NSOLUCE])

    selected = population[0:NSOLUCE]

    return selected


def selectionRandom(population, n):
    selected = []
    for i in range(n):
        selected.append(choice(population).clone())

    return selected


def crossoverSubtour(parent1, parent2):
    fa = True
    fb = True
    indexList = [x for x in range(len(parent1))]
    cityList = [-1 for x in range(len(parent1))]
    listSize = len(parent1)
    startPoint = randrange(len(parent1))
    indexList.remove(startPoint)
    parent1Point = parent2Point = startPoint
    cityList[startPoint] = parent1[startPoint]
    while True:
        parent1Point = (parent1Point-1) % listSize
        parent2Point = (parent2Point+1) % listSize
        if fa:
            if not (parent1[parent1Point] in cityList):
                cityList[parent1Point] = parent1[parent1Point]
                refIndex = parent1.index(parent1[parent1Point])
                if refIndex in indexList:
                    indexList.remove(refIndex)
            else:
                fa = False
        if fb:
            if not (parent2[parent2Point] in cityList):
                cityList[parent2Point] = parent2[parent2Point]
                refIndex = parent1.index(parent2[parent2Point])
                if refIndex in indexList:
                    indexList.remove(refIndex)
            else:
                fb = False


        if not fa and not fb:
            break

    while len(indexList) > 0:
            idx = choiceAndRemove(indexList)
            addIndex = cityList.index(-1) #(parent2Point+1) % listSize
            cityList[addIndex] = parent1[idx]

    return Solution(cityList)




def crossoverFixedpoint(parent1, parent2):
    child = Solution([])
    child.add(parent1[0])
    indexList = [x for x in range(len(parent1))]

    #if isTimeout(startTime, maxTime):
        #break
    mode = randrange(10) % 2 == 0
    for value in range(1, len(parent1)):
        if mode:
            distance1 = getPythagoreDistance(child[-1], parent1[value])
            distance2 = getPythagoreDistance(child[-1], parent2[value])
        else:
            distance1 = getDistanceChessboard(child[-1], parent1[value])
            distance2 = getDistanceChessboard(child[-1], parent2[value])

        if distance1 < distance2:
            first, second = parent1[value], parent2[value]
        else:
            first, second = parent2[value], parent1[value]

        if not child.contains(first):
            child.add(first)
        elif not child.contains(second):
            child.add(second)
        else:
            idx = choiceAndRemove(indexList)
            city = parent1[idx]
            while city in child:
                idx = choiceAndRemove(indexList)
                city = parent1[idx]
            child.add(city)
    child.evaluate()
    return child

def crossover(population, startTime, maxTime):
    """
    croisement en un points
    """

    crossed = []

    #index = randrange(0,len(population))
    for i in range(0, CROSSED_N):
        parent1 = population[randrange(0,len(population)-1)]
        parent2 = population[randrange(0,len(population)-1)]
        crossed.append(crossoverFixedpoint(parent1,parent2))
        #crossed.append(crossoverSubtour(parent1,parent2))
        # child = Solution([])
        # child.add(parent1[0])
        # indexList = [x for x in range(len(parent1))]
        #
        # if isTimeout(startTime, maxTime):
        #     break
        #
        # for value in range(1, len(parent1)):
        #     distance1 = getPythagoreDistance(child[-1], parent1[value])
        #     distance2 = getPythagoreDistance(child[-1], parent2[value])
        #
        #     if distance1 < distance2:
        #         first, second = parent1[value], parent2[value]
        #     else:
        #         first, second = parent2[value], parent1[value]
        #
        #     if not child.contains(first):
        #         child.add(first)
        #     elif not child.contains(second):
        #         child.add(second)
        #     else:
        #         idx = choiceAndRemove(indexList)
        #         city = parent1[idx]
        #         while city in child:
        #             idx = choiceAndRemove(indexList)
        #             city = parent1[idx]
        #         child.add(city)
        # child.evaluate()
        #crossed.append(child)


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
    parser.add_option('--maxtime', action="store", type="int", default=30)

    (opts, args) = parser.parse_args()

    nogui = opts.__dict__["nogui"]
    maxtime = opts.__dict__["maxtime"]
    filename = args[0] if len(args) > 0 else None


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
    # newSolution = mutateSolution(solution)
    #
    # print(solution)
    # print(newSolution)
    # newSolution.evaluate()
    # print(newSolution)


