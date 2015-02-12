# -*- coding: utf-8 -*-
import optparse
import GUI_example
from City import City


def ga_solve(filename=None, gui=True, maxtime=0):
	## Saisie des villes ou lecture depuis un fichier
	cities = []
	if filename is None:
		cities = getCitiesFromGUI()
		print(cities)
	else:
		cities = parseCitiesFromFile(filename)

	lenght = 0
	path = "toto"
	return lenght, path

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
	parser.add_option('--maxtime', action="store", type="int", default=0)

	(opts, args) = parser.parse_args()

	nogui = opts.__dict__["nogui"]
	maxtime = opts.__dict__["maxtime"]
	filename = args[0] if len(args) > 0 else None

	# print(nogui)
	# print(maxtime)
	# print(filename)

	## affichage en "temps réel" de l'évolution du meilleur chemin
	ga_solve(filename, not nogui, maxtime)