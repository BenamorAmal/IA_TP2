class City:
	""" Ville est une classe représentant une ville composé de points x et y
	"""
	counter = 0

	def __init__(self, x, y, name=None):
		self._x = x
		self._y = y

		if name is None:
			City.counter += 1
			self._name = "Ville " + City.counter
		else:
			self._name = name

	def getPos(self):
		return (self._x, self._y)

	def getName(self):
		return self._name
