import pygame
import math

pygame.init()
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.get_surface()


def drawTree(x1, y1, angle, depth):
	fork_angle = 20
	base_len = 10.0
	if depth > 0:
		x2 = x1 + int(math.cos(math.radians(angle)) * depth * base_len)
		y2 = y1 + int(math.sin(math.radians(angle)) * depth * base_len)
		pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 2)
		drawTree(x2, y2, angle - fork_angle, depth - 1)
		drawTree(x2, y2, angle + fork_angle, depth - 1)


def input(event):
	if event.type == pygame.QUIT:
		quit()

drawTree(300, 550, -90, 9)
pygame.display.flip()
while True:
	input(pygame.event.wait())
