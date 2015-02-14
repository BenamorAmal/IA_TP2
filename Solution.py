import math
from City import City

class Solution:
	def __init__(self, cities):
		self._cities = cities
		if len(cities) > 0:
			self._evaluation = self.evaluate()
		else:
			self._evaluation = 0

	#Evaluation en fonction des distances entre les villes
	def evaluate(self):
		length = 0
		for i in range(len(self._cities)-1):
			# print(i)
			cityA = self._cities[i]
			cityB = self._cities[i+1]
			length += getPythagoreDistance(cityA, cityB)

		length+= getPythagoreDistance(self._cities[0], self._cities[-1])
		return length

	def add(self, city):
		self._cities.append(city)
		self._evaluation = self.evaluate()

	def __repr__(self):
		names = ""
		for city in self._cities:
			names += city._name + ", "
		names += "("+ str(self._evaluation) + ")\n"
		return names

	@property
	def evaluation(self):
		return self._evaluation

	@property
	def cities(self):
		return self._cities

	#Recuperation d'une liste de tuple (x,y) pour l'affichage sur le GUI
	def getPoints(self):
		points = []
		for city in self._cities:
			points.append((city.x, city.y))
		return points
		#return (lambda x,y: for x,y in )

	# utilisé pour accéder aux villes contenues dans une Solution
	def __getitem__(self, item):
		return self._cities[item]

	def __setitem__(self, key, value):
		self._cities[key] = value

	def __len__(self):
		return len(self._cities)

	def __iter__(self):
		for city in self._cities:
			yield city

	#Fonction pour savoir si une ville appartient a la solution
	def contains(self,citySrc):
		for city in self._cities:
			if city == citySrc:
				return True
		return False


	def getDict(self):
		dico = dict()
		for city in self._cities:
			dico[city._name] = (city._x,city._y)

		return dico

	def getCities(self):
		cityList = []
		for city in self._cities:
			cityList.append(city.name)
		return cityList

#Retourne le distance entre 2 villes
def getPythagoreDistance(cityA, cityB):
	deltaX = abs(cityA.x - cityB.x)
	deltaY = abs(cityA.y - cityB.y)
	return math.sqrt(deltaX**2 + deltaY**2)

## Test unitaire !
if __name__ == '__main__':
	cities = []
	c1 = City(0, 0)
	c2 = City(0, 5)
	c3 = City(0, 10)
	c4 = City(0, 15)
	cities.append(c1)
	cities.append(c2)
	cities.append(c3)
	cities.append(c4)

	solution = Solution(cities)
	length = solution.evaluate()
	print(length)