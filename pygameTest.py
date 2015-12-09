import sys, pygame
pygame.init()
black = 0, 0, 0
size = width, height = 640, 640
screen = pygame.display.set_mode(size)

w=64

greenMan=pygame.transform.scale(pygame.image.load('sprites/fatGreenMan.png'),(w,w))
hairBrain=pygame.transform.scale(pygame.image.load('sprites/hairBrain.png'),(w,w))
glimmer=pygame.transform.scale(pygame.image.load('sprites/glimmer.png'),(w,w))
jelly=pygame.transform.scale(pygame.image.load('sprites/Jelly.png'),(w,w))
turtle=pygame.transform.scale(pygame.image.load('sprites/turtle.png'),(w,w))
shroomo=pygame.transform.scale(pygame.image.load('sprites/shroomo.png'),(w,w))

tile=pygame.image.load('sprites/floorTile2.png')
tile=pygame.transform.scale(tile,(w,w))

terminal=pygame.transform.scale(pygame.image.load('sprites/Terminal2.png'),(w,w))

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		screen.fill(black)
		for i in range(10):
			for j in range(10):
				screen.blit(tile,(w*i,w*j))
		screen.blit(greenMan,(w*3,w*2-w/4))
		screen.blit(hairBrain,(w*3,w*3-w/4))
		screen.blit(glimmer,(w*5,w*3-w/4))
		screen.blit(jelly,(w*5,w*5-w/4))
		screen.blit(turtle,(w*1,w*2-w/4))
		screen.blit(shroomo,(w*1,w*3-w/4))

		screen.blit(terminal,(w*1,w*3))

		pygame.display.flip()