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
		self.cromosomas1Len =[]
		self.cromosomas2Len = []
		self.screen = None
		self.rateMutation = None

	def windowSettings(self):
		pygame.init()
		self.window = pygame.display.set_mode((600, 600))
		pygame.display.set_caption("Fractal Tree")
		self.screen = pygame.display.get_surface()

	def mutacion(self, pBits):
		lista = list(pBits)
		for i in range(self.rateMutation):
			index  = r.randint(0,len(lista))
			if(lista[index]=='1'):
				lista[index]='0'
			else:
				lista[index]='1'
		return ''.join(lista)


	def remplazarTop(self,pDict,pId):
		id =0
		notaAct = 10000
		for dict in self.topArboles:
			if(self.topArboles[dict]['Nota']<notaAct):
				id = dict
				notaAct = self.topArboles[dict]['Nota']
		
		if(pDict['Nota']>self.topArboles[id]['Nota']):
			del self.topArboles[id]
			self.topArboles[pId] = pDict

	def convertirParamABin(self,cromosomas1,cromosomas2):
		bin1 = ""
		bin2 = ""
		for i in range(len(cromosomas1)):
			
			if(i == 0):
				bin1+=bin(cromosomas1[i])[3:]
				bin2+=bin(cromosomas2[i])[3:]
				self.cromosomas1Len.append(len(bin(cromosomas1[i])[3:]))
				self.cromosomas2Len.append(len(bin(cromosomas2[i])[3:]))
			else:
				bin1+=bin(cromosomas1[i])[2:] 
				bin2+=bin(cromosomas2[i])[2:]
				self.cromosomas1Len.append(len(bin(cromosomas1[i])[2:]))
				self.cromosomas2Len.append(len(bin(cromosomas2[i])[2:]))
			
		return [bin1,bin2]

	def swapBits(self,bin1,bin2):
		rand = r.randint(0,len(bin1))
		aux1 = bin1[:rand]
		aux2 = bin2[:rand]

		mitad1 = bin1[rand:]
		mitad2 = bin2[rand:]

		aux1+=mitad2
		aux2+=mitad1

		r1 = r.randint(0,100)
		r2 = r.randint(0,100)

		if(r1<=4):
			aux2 = self.mutacion(aux2)
		if(r2<=4):
			aux1 = self.mutacion(aux1)
		return [aux2,aux1]


	def Cruces(self):
		parejas = self.Seleccion()
		
		for pair in parejas:
			parametros1 = self.FractalDict[pair[0]]['Parametros']
			parametros2 = self.FractalDict[pair[1]]['Parametros']

			binarios = self.convertirParamABin(parametros1,parametros2)
			binarios = self.swapBits(binarios[0],binarios[1])

			newCromosomas1 = []
			newCromosomas2 = []
			act1=0
			act2=0
			for i in range(len(self.cromosomas1Len)):
				rango1 = self.cromosomas1Len[i]
				rango2 = self.cromosomas2Len[i]
				if(binarios[0][act1:act1+rango1]!=''):
					newCromosomas1.append(int(binarios[0][act1:act1+rango1],2))
				else:
					newCromosomas1.append(0)
				if(binarios[1][act2:act2+rango2]!=''):
					newCromosomas2.append(int(binarios[1][act2:act2+rango2],2))
				else:
					newCromosomas2.append(0)
				act1+=rango1
				act2+=rango2
			newCromosomas1[0] = newCromosomas1[0]*-1
			newCromosomas2[0] = newCromosomas2[0]*-1

			# Arbol nuevo #1
			newCoord1 = self.drawTree(300,599,newCromosomas1[0],newCromosomas1[1],newCromosomas1[2],
				newCromosomas1[3],newCromosomas1[4],newCromosomas1[5],newCromosomas1[6])
			self.FractalCoords = []
			nota1 = self.getScore(self.SilhouetteMatrix,newCoord1)
			arbolDict1 = {'Coordenadas': newCoord1, 'Parametros':newCromosomas1, 'Nota': nota1, 'Padres' : pair}
			self.FractalDict[len(self.FractalDict)] = arbolDict1
			self.remplazarTop(arbolDict1,len(self.FractalDict)-1)
			# Arbol nuevo #2
			newCoord2 = self.drawTree(300,599,newCromosomas2[0],newCromosomas2[1],newCromosomas2[2],
				newCromosomas2[3],newCromosomas2[4],newCromosomas2[5],newCromosomas2[6])
			self.FractalCoords = []
			nota2 = self.getScore(self.SilhouetteMatrix,newCoord2)
			arbolDict2 = {'Coordenadas': newCoord2, 'Parametros':newCromosomas2, 'Nota': nota2, 'Padres' : pair}
			self.FractalDict[len(self.FractalDict)] = arbolDict2
			self.remplazarTop(arbolDict2,len(self.FractalDict)-1)

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
		if(score == 0):
			score = 1
		return score/len(fractalArr)*100

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

	def algoritmoGenetico(self, imagePath):
		self.getDataFromSilhouette(imagePath)
		self.PoblacionInicial(300, 599, -90, 13, 15, 9, 1, 6, 1)


	def drawTree(self, x1, y1, angle, forkAng, depth, baseLen, lenDec, baseDiam, diamDec):
		if([x1,y1] not in self.FractalCoords and self.screen == None):
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

	def PoblacionInicial(self, x1, y1, angle, forkAng, depth, baseLen, lenDec, baseDiam, diamDec, rateMut):
		self.rateMutation = rateMut	
		for i in range(10):
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
			arbolDict = {'Coordenadas': coordenadas, 'Parametros':parametros, 'Nota': nota, 'Padres' : None}
			self.FractalDict[i] = arbolDict
			self.FractalCoords = []
		self.topArboles = self.FractalDict
		self.Cruces()

	def showTree(self, x1, y1, angle, forkAngle, depth, baseLen, lenDec, baseDiam, diamDec):
		self.windowSettings()
		self.drawTree(x1, y1, angle, forkAngle, depth,
					  baseLen, lenDec, baseDiam, diamDec)
		pygame.display.flip()
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					running = False

