import pygame
import math

class fractalTree:
	def __init__(self):
		# super().__init__(master)
		# self.master = master
		self.windowSettings()

	def windowSettings(self):
		pygame.init()
		self.window = pygame.display.set_mode((600, 600))
		pygame.display.set_caption("Fractal Tree")
		self.screen = pygame.display.get_surface() 

	def drawTree(self,x1, y1, angle, forkAngle, depth, baseLen, lenDecRatio):
		if depth > 0:
			x2 = x1 + int(math.cos(math.radians(angle)) * depth * baseLen)
			y2 = y1 + int(math.sin(math.radians(angle)) * depth * baseLen)
			pygame.draw.line(self.screen, (255, 255, 255), (x1, y1), (x2, y2), 2)
			self.drawTree(x2, y2, angle - forkAngle, forkAngle,depth - 1, baseLen-lenDecRatio, lenDecRatio)
			self.drawTree(x2, y2, angle + forkAngle, forkAngle,depth - 1, baseLen-lenDecRatio, lenDecRatio)        

	def createTree(self,x1, y1, angle, forkAngle, depth, baseLen, lenDecRatio):	
		self.drawTree(x1,y1,angle,forkAngle,depth,baseLen,lenDecRatio)
		pygame.display.flip()
		while True:
			self.input(pygame.event.wait())
	
	def input(self,event):
		if event.type == pygame.QUIT:
			quit()

# test = fractalTree()
# test.createTree(300, 550, -90, 20, 9 , 10,1)