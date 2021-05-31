import pygame
import math
import random as r
import numpy as np
from PIL import Image


class fractalTree:
	def __init__(self):
		self.SilhouetteMatrix = []
		self.FractalMatrix = []
		self.screen = None

	def windowSettings(self):
		pygame.init()
		self.window = pygame.display.set_mode((600, 600))
		pygame.display.set_caption("Fractal Tree")
		self.screen = pygame.display.get_surface()

	def getScore(self, silhouetteArr, fractalArr):
		fractalNpArr = np.array(fractalArr)
		notEqual = 0
		for i in range(len(fractalNpArr)):
			if(silhouetteArr[i] not in fractalNpArr):
				notEqual += 1
		return notEqual/len(silhouetteArr)

	def getDataFromSilhouette(self, path):
		img = Image.open(path)
		rgbImage = img.convert("RGB")
		im = np.array(rgbImage)
		black = [0, 0, 0]
		X, Y = np.where(np.all(im == black, axis=2))
		self.SilhouetteMatrix = np.column_stack((X, Y))
		return self.SilhouetteMatrix

	def drawTree(self, x1, y1, angle, forkAng, depth, baseLen, lenDec, baseDiam, diamDec):
		self.FractalMatrix.append([x1, y1])
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


a = fractalTree()
m = a.getDataFromSilhouette("silueta.gif")
a.drawTree(300, 599, -90, 10, 9, 10, 1, 2, 0)
print(a.getScore(m, a.FractalMatrix))
