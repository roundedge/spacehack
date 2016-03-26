import sys, pygame
from types import MethodType
from MyMath import Vec

## I'm gonna add a helpful function to rect ##
## see here: https://www.ianlewis.org/en/dynamically-adding-method-classes-or-class-instanc ##

#def get_abs_rect(self):
#	return self.get_rect(topleft=self.get_abs_offset())

#pygame.Rect.get_abs_rect=MethodType(get_abs_rect, None, pygame.Rect)


pygame.init()
black = 0, 0, 0
size = width, height = 640, 640
screen = pygame.display.set_mode(size)

w=32

subscreen=screen.subsurface(pygame.Rect(320,320,160,160))

greenMan=pygame.transform.scale(pygame.image.load('sprites/fatGreenMan.png'),(w,w))
hairBrain=pygame.transform.scale(pygame.image.load('sprites/hairBrain.png'),(w,w))
glimmer=pygame.transform.scale(pygame.image.load('sprites/glimmer.png'),(w,w))
jelly=pygame.transform.scale(pygame.image.load('sprites/Jelly.png'),(w,w))
turtle=pygame.transform.scale(pygame.image.load('sprites/turtle.png'),(w,w))
shroomo=pygame.transform.scale(pygame.image.load('sprites/shroomo.png'),(w,w))

tile=pygame.image.load('sprites/floorTile2.png')
tile=pygame.transform.scale(tile,(w,w))

terminal=pygame.transform.scale(pygame.image.load('sprites/Terminal2.png'),(w,w))


def tileAt(pixelPos):
		pix=Vec(pixelPos[0],pixelPos[1])

		inWorldPanel=subscreen.get_rect(topleft=subscreen.get_abs_offset()).collidepoint(pixelPos)

		if not inWorldPanel:
			return None


		middleOfPanel=Vec(subscreen.get_width()/2,subscreen.get_height()/2)

		focus=Vec(80,80)

		mapPixel=pix-Vec(subscreen.get_abs_offset())-middleOfPanel+focus

		tilePos=mapPixel/w
		return tilePos


while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		screen.fill(black)
		for i in range(10):
			for j in range(10):
				subscreen.blit(tile,(w*i,w*j))
		subscreen.blit(greenMan,(w*3,w*2-w/4))
		subscreen.blit(hairBrain,(w*3,w*3-w/4))
		subscreen.blit(glimmer,(w*5,w*3-w/4))
		subscreen.blit(jelly,(w*5,w*5-w/4))
		subscreen.blit(turtle,(w*1,w*2-w/4))
		subscreen.blit(shroomo,(w*1,w*3-w/4))

		if(subscreen.get_rect(topleft=subscreen.get_abs_offset()).collidepoint(pygame.mouse.get_pos())):
			screen.blit(terminal,(w*1,w*3))

		print(tileAt(pygame.mouse.get_pos()))

		pygame.display.flip()