from warnings import simplefilter
from numpy_indexed.utility import axis_as_object
import pygame
import math
import random as r
import numpy as np
from PIL import Image
class fractalTree:
	def __init__(self):
		self.SilhouetteMatrix = []
		self.FractalCoords = []
		self.FractalDict = {}
		self.topArboles = {}
		self.InitialParameters = []
		self.screen = None

	def windowSettings(self):
		pygame.init()
		self.window = pygame.display.set_mode((600, 600))
		pygame.display.set_caption("Fractal Tree")
		self.screen = pygame.display.get_surface()

	def convertirParamABin(self,cromosomas1,cromosomas2):
		bin1 = ""
		bin2 = ""
		for i in range(len(cromosomas1)):
				bin1+=bin(cromosomas1[i])[1:]
				bin2+=bin(cromosomas2[i])[1:]

		return bin1,bin2

	def swapBits(self,bin1,bin2):
		rand = r.randint(0,len(bin1))
		print(rand)
		print(bin1," ",bin2)
		aux1 = bin1[:rand]
		aux2 = bin2[:rand]

		mitad1 = bin1[rand:]
		mitad2 = bin2[rand:]

		aux1+=mitad2
		aux2+=mitad1
		print(aux1," ",aux2)
		return [aux1,aux2]


	def Cruces(self):
		parejas = self.Seleccion()

		for pair in parejas:
			cromosomas1 = self.topArboles[pair[0]]['Parametros']
			cromosomas2 = self.topArboles[pair[1]]['Parametros']

			bin1,bin2 = self.convertirParamABin(cromosomas1,cromosomas2)
			bin1,bin2 = self.swapBits(bin1,bin2)

	def Seleccion(self):
		notas = []
		arboles = []
		parejas = []

		for arbol in self.topArboles:
			arboles.append(arbol)
			notas.append(self.topArboles[arbol]['Nota'])
		seleccionados = r.choices(arboles,cum_weights= notas,k=len(self.topArboles))
		
		for i in range(0,len(seleccionados),2):	
			parejas.append([seleccionados[i],seleccionados[i+1]])
		return parejas

	def getScore(self, silhouetteArr, fractalArr):
		a = set(map(tuple,silhouetteArr))
		b = set(map(tuple,fractalArr))
		score = len(a.intersection(b))
		return score/len(silhouetteArr)*100

	def getDataFromSilhouette(self, path):
		img = Image.open(path)
		rgbImage = img.convert("RGB")
		im = np.array(rgbImage)
		black = [0, 0, 0]
		X, Y = np.where(np.all(im == black, axis=2))
		self.SilhouetteMatrix = np.column_stack((X, Y))
		return self.SilhouetteMatrix
		
	def checkImgResolution(self, imgPath):
		im = Image.open(imgPath)
		width, height = im.size

		if([width, height] != [600, 600]):
			return False
		return True

	def drawTree(self, x1, y1, angle, forkAng, depth, baseLen, lenDec, baseDiam, diamDec):
		if([x1,y1] not in self.FractalCoords):
			self.FractalCoords.append([x1, y1])
		if(lenDec >= baseLen):
			lenDec = 0
		elif(diamDec >= baseDiam):
			diamDec = 0
		if depth > 0:
			x2 = x1 + int(math.cos(math.radians(angle)) * depth * baseLen)
			y2 = y1 + int(math.sin(math.radians(angle)) * depth * baseLen)
			if(self.screen != None):
				pygame.draw.line(self.screen, (255, 255, 255),
								 (x1, y1), (x2, y2), baseDiam)
			self.drawTree(x2, y2, angle - forkAng, forkAng, depth - 1, baseLen -
						  lenDec, lenDec, baseDiam-diamDec, diamDec)
			self.drawTree(x2, y2, angle + forkAng, forkAng, depth - 1, baseLen -
						  lenDec, lenDec, baseDiam-diamDec, diamDec)
		return self.FractalCoords

	def PoblacionInicial(self, x1, y1, angle, forkAng, depth, baseLen, lenDec, baseDiam, diamDec):
		for i in range(2):
			rAngle = r.randint(80,angle*-1)*-1
			rforkAng = r.randint(0,forkAng)
			rDepth = r.randint(4,depth)
			rBaseLen = r.randint(4,baseLen)
			rLenDec =  r.randint(0,lenDec)
			rBaseDiam = r.randint(1,baseDiam)
			rDiamDec = r.randint(0,diamDec)
			parametros  = [rAngle, rforkAng, rDepth, rBaseLen, rLenDec, rBaseDiam, rDiamDec]
			coordenadas = self.drawTree(x1, y1, rAngle, rforkAng, rDepth, rBaseLen, rLenDec, rBaseDiam, rDiamDec)
			nota = self.getScore(self.SilhouetteMatrix,coordenadas)
			arbolDict = {'Coordenadas': coordenadas, 'Parametros':parametros, 'Nota': nota, 'Padres' : None, 'NotaNormalizada' : 0}
			self.FractalDict[i] = arbolDict
			self.FractalCoords = []
		self.topArboles = self.FractalDict
		self.Cruces()

	def algoritmoGenetico(self, imagePath):
		self.getDataFromSilhouette(imagePath)
		self.PoblacionInicial(300, 599, -90, 13, 15, 9, 1, 6, 1)


	def showTree(self, x1, y1, angle, forkAngle, depth, baseLen, lenDec, baseDiam, diamDec):
		self.windowSettings()
		self.drawTree(x1, y1, angle, forkAngle, depth,
					  baseLen, lenDec, baseDiam, diamDec)
		pygame.display.flip()
		while True:
			self.input(pygame.event.wait())

	def input(self, event):
		if event.type == pygame.QUIT:
			quit()

# f = fractalTree()
# f.algoritmoGenetico("silueta.gif")
# m = f.
# f.

