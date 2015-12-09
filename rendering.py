import libtcodpy as ltc
import MyMath
import pygame


class Screen:
	#modes
	libtcod=0
	pygame=1

	def __init__(self, game, renderMode=libtcod):
		self.renderMode=renderMode
		self.game=game
		#screen stuff
		self.width=125
		self.height=75
		self.LIMIT_FPS=10

		if self.renderMode is self.libtcod:
			self.libtcod_init()

	def render(self):
		if self.renderMode is self.libtcod:
			self.libtcod_render()
		
	#helper functions

	def mapTopLeftX(self):
		focus_pos=self.game.PARTY.getFocus().position()
		if(focus_pos):
			return focus_pos[0]-self.width/2
		else:
			return -self.width/2 

	def mapTopLeftY(self):
		focus_pos=self.game.PARTY.getFocus().position()
		if(focus_pos):
			return focus_pos[1]-self.height/2
		else:
			return -self.height/2


	#libtcod rendering
			
	def libtcod_init(self):
		#initialize the screens
		ltc.console_set_custom_font('terminal8x8_gs_as.png', ltc.FONT_TYPE_GREYSCALE | ltc.FONT_LAYOUT_ASCII_INCOL)
		ltc.console_init_root(self.width, self.height, 'spacehack', False)
		ltc.sys_set_fps(self.LIMIT_FPS)

		self.ltcScreen=ltc.console_new(self.width,self.height)


	def libtcod_render(self):
		ltc.console_clear(self.ltcScreen)
		
		#these are the coordinates on the map that conform to the dimensions of the 
		#screen, centered on where we would like them to be centered
		mapWindow=MyMath.Rect(self.mapTopLeftX(),self.mapTopLeftY(),self.width,self.height)
		
		focused_map=self.game.PARTY.getFocus().map
		if(focused_map):
			focused_map.draw(self.game.PARTY, self.ltcScreen, mapWindow)
		else:
			#TODO: draw the current party member floating in a vacuum
			print("player out of bounds")
		ltc.console_blit(self.ltcScreen,0,0,self.width,self.height,0,0,0)
		
		self.game.PARTY.draw_menu(self.ltcScreen)
		
		self.game.interface.draw(self.ltcScreen)
		
		ltc.console_flush()


#okay, so I want to revamp rendering... 
#I want to be able to switch between rendering modes, libtcod or pygame
#render grabs the map, and renders it by iterating through all the relevant 
#squares of the map and rendering the tile, then rendering all the objects

class basic_libtcod_object_renderer():

	def __init__(self, char, color):
		self.char=char
		self.color=color

	def render(self,object,isVisible,x,y,screen):
		if isVisible:
			#set the color and then draw the character that represents this object at its position
			libtcod.console_set_default_foreground(screen ,self.color)
			libtcod.console_put_char(screen, x, y, self.char, libtcod.BKGND_NONE)

class basic_libtcod_tile_renderer():

	def __init__(visibleColor, notVisibleColor):
		self.visibleColor=visibleColor
		self.notVisibleColor=notVisibleColor

	def render(self, tile, isVisible, x, y, screen):
		if isVisible:
			ltc.console_set_char_background(screen,x,y,visibleColor,ltc.BKGND_SET)
		else:
			ltc.console_set_char_background(screen,x,y,notVisibleColor,ltc.BKGND_SET)

def bgDrawStyle(visibleColor,notVisibleColor):
	#this gives you draw callbacks which draw the given color
	def drawCallback(x,y,visible,screen):
		if(visible):
			ltc.console_set_char_background(screen,x,y,visibleColor,ltc.BKGND_SET)
		else:
			ltc.console_set_char_background(screen,x,y,notVisibleColor,ltc.BKGND_SET)
	return drawCallback


#### rendering stylesheet ######
from collections import namedtuple
ORS = namedtuple('ObjectRenderingStyle', ('color', 'char', 'img'))

HairBrain=ORS('ltc.pink','@',pygame.image.load('sprites/hairBrain.png'))

TRS = namedtuple('TileRenderingStyle', ('visibleColor','notVisibleColor',  'img'))

Floor=TRS()
