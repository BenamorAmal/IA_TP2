import math
from City import City

class Solution:
	def __init__(self, cities):
		self._cities = cities
		self._evaluation = self.evaluate()

	def evaluate(self):
		length = 0
		for i in range(len(self._cities)-1):
			print(i)
			cityA = self._cities[i]
			cityB = self._cities[i+1]
			length += getPythagoreDistance(cityA, cityB)

		length+= getPythagoreDistance(self._cities[0], self._cities[-1])
		return length

	def __repr__(self):
		names = ""
		for city in self._cities:
			names += city._name + ", "
		names += "("+ str(self._evaluation) + ")\n"
		return names

	@property
	def evaluation(self):
		return self._evaluation

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