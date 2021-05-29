import PIL
import pygame 
import math
import random as r
from PIL import Image

class fractalTree:
	def __init__(self):
		# self.windowSettings()
		self.SilhouetteMatrix = []

	def windowSettings(self):
		pygame.init()
		self.window = pygame.display.set_mode((600, 600))
		pygame.display.set_caption("Fractal Tree")
		self.screen = pygame.display.get_surface()

	def getDataFromSilhouette(self, path):	
		img = Image.open(path)
		rgbImage = img.convert("RGB")
		for i in range(1000):
			x = r.randint(0,499)
			y = r.randint(0,499)
			print(x,y)
			if(rgbImage.getpixel((x,y)) != (255,255,255)):
				self.SilhouetteMatrix.append([x,y])
		print(self.SilhouetteMatrix)

	def drawTree(self, x1, y1, angle, forkAng, depth, baseLen, lenDec, baseDiam, diamDec):
		if depth > 0:
			x2 = x1 + int(math.cos(math.radians(angle)) * depth * baseLen)
			y2 = y1 + int(math.sin(math.radians(angle)) * depth * baseLen)
			pygame.draw.line(self.screen, (255, 255, 255),
                            (x1, y1), (x2, y2), baseDiam)
			self.drawTree(x2, y2, angle - forkAng, forkAng, depth - 1, baseLen -
                            lenDec, lenDec, baseDiam-diamDec, diamDec)
			self.drawTree(x2, y2, angle + forkAng, forkAng, depth - 1, baseLen -
                            lenDec, lenDec, baseDiam-diamDec, diamDec)

	def createTree(self, x1, y1, angle, forkAngle, depth, baseLen, lenDec, baseDiam, diamDec):
		self.drawTree(x1, y1, angle, forkAngle, depth, baseLen,lenDec, baseDiam, diamDec)
		pygame.display.flip()
		while True:
			self.input(pygame.event.wait())

	def input(self, event):
		if event.type == pygame.QUIT:
			quit()
