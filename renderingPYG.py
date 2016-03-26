from MyMath import *
import pygame
import sys



class Renderer:
	size=width,height=1280,640
	tileWidth=32
	#the world panel is where the ship is displayed
	worldPanelRect=pygame.Rect(0,0,width/2,height)
	#the activity panel is where the interfaces are displayed
	activityPanelRect=pygame.Rect(width/2,0,width/2,height)


	def __init__(self):
		self.zoom=1

		pygame.init()
		self.screen=pygame.display.set_mode(self.size)
		self.worldPanel=self.screen.subsurface(self.worldPanelRect)
		self.activityPanel=self.screen.subsurface(self.activityPanelRect)

		self.mapOffset=Vec(0,0)
		self.mapSurface=pygame.Surface((self.tileWidth*200,self.tileWidth*200))

	#map rendering
	#we have a map already loaded, with all the tiles blitted to a surface, and then blit that surface onto the worldPanel. When anything changes in the map, you pass the change to the renderer, and then the renderer will re render the tile on the map surface
	def tileAt(self,pixelPos):
		#this tells you which tile is at a screens absolute pixel coordinates, should return none if out of bounds of the display region associated with displaying the map

		#first check if the pixel is in the display region of the world panel:
		inWorldPanel=self.worldPanel.get_rect(topleft=self.worldPanel.get_abs_offset()).collidepoint(pixelPos)

		if not inWorldPanel:
			return None

		mapPixel=Vec(pixelPos)-Vec(self.worldPanel.get_abs_offset())-self.mapOffset
		#and then we take the map pixel and divide by the tile width
		tilePos=mapPixel/self.tileWidth
		return tilePos


	def setMapFocus(self,pos,pixel=False):
		if(not pixel):
			pixPos=Vec(pos)*self.tileWidth-self.tileWidth/2
		else:
			pixPos=Vec(pos)
		self.mapOffset= -pixPos+Vec(self.mapSurface.Rect.center)

	def setMapDimensions(self,width,height):
		temp=self.mapSurface.copy()
		self.mapSurface=pygame.Surface(self.tileWidth*width,self.tileWidth*height)
		self.mapSurface.blit(temp,(0,0))

	def drawTile(self, sprite, index):
		pos=self.tileWidth*Vec(index)
		scale=(self.tileWidth, self.tileWidth)
		self.mapSurface.blit(sprite,pos)

	def drawObject(self,sprite,index):
		#figure out actual pixel position
		pos=self.tileWidth*Vec(index)+self.mapOffset
		#figue out if its in the render frame
		frame=self.worldPanel.get_rect().inflate(self.tileWidth*2,self.tileWidth*2)
		if(frame.collidepoint(pos)):
			#if it is, draw it at the position:
			self.worldPanel.blit(sprite,pos)
		else:
			pass

	def render(self, mapTileChanges, mapObjects):
		#inputs are dictionaries with map positions (tuples) as keys
		#update the map tiles
		for mapPos in mapTileChanges.keys():
			print mapPos
			handle=mapTileChanges[mapPos]
			sprite=renderStyles[handle]
			self.drawTile(sprite,mapPos)
		#draw the mapSurface
		self.worldPanel.blit(self.mapSurface,self.mapOffset)
		#draw the mapObjects
		for mapPos in mapObjects.keys():
			handle=mapObjects[mapPos]
			sprite=renderStyles[handle]
			self.drawObject(sprite,mapPos)
		
		pygame.display.flip()



#### sprites ######
def load(path):
	return pygame.image.load(path)#.convert()


hairBrain=load('sprites/hairBrain.png')
greenMan=load('sprites/fatGreenMan.png')
hairBrain=load('sprites/hairBrain.png')
glimmer=load('sprites/glimmer.png')
jelly=load('sprites/Jelly.png')
turtle=load('sprites/turtle.png')
shroomo=load('sprites/shroomo.png')
floor=load('sprites/floorTile2.png')

### Draw Callbacks ###
# the draw callbacks give a callback function to be executed when the renderer iterates through the objects
def spriteCallback(img):
	def drawCallback(x,y,screen):
		screen.blit(img,(x,y))
	return drawCallback

def square(color):
	pygame.Surface((Renderer.tileWidth,Renderer.tileWidth)).fill(color)


### render handles:styles ###

renderStyles={
	"floor":load('sprites/floorTile2.png'),
	"hairBrain":load('sprites/hairBrain.png'),
	"greenMan":load('sprites/fatGreenMan.png'),
	"wall":square((0,100,255)),
	"active_terminal":square((0,255,0)),
	"inactive_terminal":square((255,0,0)),
	"open_door":square((100,100,0)),
	"closed_door":square(100,100,255),
}


### test ###

r=Renderer()

tiles={}
for i in range(20):
	for j in range(20):
		index=(i,j)
		tiles[index]="floor"

objects={(0,0):"hairBrain", (5,5):"greenMan"}

r.render(tiles,objects)

while 1:
	for event in pygame.event.get():
		if event.type==pygame.QUIT: sys.exit()
	r.render({},objects)