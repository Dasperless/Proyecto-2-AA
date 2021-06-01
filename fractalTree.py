import pygame
import math
import random as r
import numpy as np
from PIL import Image
import numpy_indexed as npi


class fractalTree:
	def __init__(self):
		self.SilhouetteMatrix = []
		self.FractalCoords = []
		self.FractalMatrix = []
		self.InitialParameters = []
		self.screen = None

	def windowSettings(self):
		pygame.init()
		self.window = pygame.display.set_mode((600, 600))
		pygame.display.set_caption("Fractal Tree")
		self.screen = pygame.display.get_surface()

	def getScore(self, silhouetteArr, fractalArr):
		fractalNpArr = np.array(fractalArr)
		score = len(npi.intersection(fractalNpArr,silhouetteArr))
		return score/len(fractalArr)*100

	def getScore1(self, silhouetteArr, fractalArr):
		fractalNpArr = np.array(fractalArr)
		score  = 0
		for i in range(len(fractalNpArr)):
			if(fractalNpArr[i] in silhouetteArr):
				score += 1
		print(score)
		return score/len(silhouetteArr)*100	

	def getDataFromSilhouette(self, path):
		img = Image.open(path)
		rgbImage = img.convert("RGB")
		im = np.array(rgbImage)
		black = [0, 0, 0]
		X, Y = np.where(np.all(im == black, axis=2))
		self.SilhouetteMatrix = np.column_stack((X, Y))
		return self.SilhouetteMatrix

	def drawTree(self, x1, y1, angle, forkAng, depth, baseLen, lenDec, baseDiam, diamDec):
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

	def test(self, x1, y1, angle, forkAng, depth, baseLen, lenDec, baseDiam, diamDec):
		# for i in range(1):
		# 	rAngle = r.randint(80,angle*-1)*-1
		# 	rforkAng = r.randint(0,forkAng)
		# 	rDepth = r.randint(4,20)
		# 	rBaseLen = r.randint(4,baseLen)
		# 	rLenDec =  r.randint(0,lenDec)
		# 	rBaseDiam = r.randint(1,baseDiam)
		# 	rDiamDec = r.randint(0,diamDec)
		# 	self.InitialParameters.append([x1,y1,rAngle,rforkAng,rDepth,rBaseLen,rLenDec,rBaseDiam,rDiamDec])
		# 	self.FractalMatrix.append(self.drawTree(x1, y1, rAngle, rforkAng, rDepth, rBaseLen, rLenDec, rBaseDiam, rDiamDec))
		# 	self.FractalCoords = []

		self.FractalMatrix.append(self.drawTree(
			x1, y1, angle, forkAng, depth, baseLen, lenDec, baseDiam, diamDec))
		# print(len( self.FractalMatrix[0]), len(self.SilhouetteMatrix))
		# print(self.getScore(m, self.FractalMatrix[0]))
		# a = self.InitialParameters[0]
		# print(a)
		# self.showTree(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8])
		# print(len(self.FractalMatrix))

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


f = fractalTree()
m = f.getDataFromSilhouette("silueta.gif")
# f.showTree(300, 599, -90, 13, 15, 2, 1, 6, 0)
f.test(300, 599, -90, 13, 15, 9, 1, 6, 1)
# print(f.FractalMatrix)


print(f.getScore(f.SilhouetteMatrix,f.FractalMatrix[0]))
# print(f.getScore1(f.SilhouetteMatrix,f.FractalMatrix[0]))