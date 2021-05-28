import pygame
import math

class fractalTree:
	def __init__(self):
		self.windowSettings()

	def windowSettings(self):
		pygame.init()
		self.window = pygame.display.set_mode((600, 600))
		pygame.display.set_caption("Fractal Tree")
		self.screen = pygame.display.get_surface()

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



