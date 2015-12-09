import MyMath
import pygame
import sys

class Renderer:
	size=width,height=640,640
	tileWidth=32

	def __init__(self,game):
		self.game=game
		self.zoom=1
		self.focus=fx,fy=0,0

		pygame.init()
		self.screen=pygame.display.set_mode(size)
		self.leftPanel=pygame.Surface(self.width/2,self.height)
		self.rightPanel=pygame.Surface(self.width/2,self.height)


	def render(self):
		#draw the map on the left panel
		#get the number of tiles spanning the width and height of the left panel
		numTilesWide=self.leftPanel.get_width/(self.tileWidth*self.zoom)
		numTilesHigh=self.leftPanel.get_height/(self.tileWidth*self.zoom)

		for i in range(numTilesWide):
			for j in range(numTilesHigh):
				game.map.


#### sprites ######
hairBrain=pygame.image.load('sprites/hairBrain.png')
greenMan=pygame.image.load('sprites/fatGreenMan.png')
hairBrain=pygame.image.load('sprites/hairBrain.png')
glimmer=pygame.image.load('sprites/glimmer.png')
jelly=pygame.image.load('sprites/Jelly.png')
turtle=pygame.image.load('sprites/turtle.png')
shroomo=pygame.image.load('sprites/shroomo.png')
floor=pygame.image.load('sprites/floorTile2.png')

### Draw Callback ###

def spriteCallback(img):
	def drawCallback(x,y,screen):
		screen.blit(img,(x,y))