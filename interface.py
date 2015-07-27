#interface
import libtcodpy as ltc
import actions
import util
import orders

class Interface:
	#the interface gives the appropriate responses to key and mouse presses through delayed function calls
	#interfaces can be interchangeable, ie context dependent
	def __init__(self):
		self.keyBinding={}
		self.mouseBinding=None
		
	def setKeyBindings(self, keyBindings):
		self.keyBinding.update(keyBindings)
	
	def setKeyBinding(self, key, binding):
		self.keyBinding[key]=binding
		
	def setMouseBinding(self, mouseBinding):
		self.mouseBinding=mouseBinding
	
	def onKeyEvent(self,key):
		if(key.vk==ltc.KEY_CHAR):
			print("character event")
			if self.keyBinding.has_key(key.c):
				self.keyBinding[key.c].call()
		else:
			if self.keyBinding.has_key(key.vk):
				self.keyBinding[key.vk].call()
	
	def onMouseEvent(self, mouse):
		if(self.mouseBinding is not None):
			self.mouseBinding.call(mouse)
			
	
#interface commands
def setFocus(PARTY,value,currentMap):
	PARTY.setFocus(value)
	currentMap.fov_recompute=True

def move(PARTY,dx,dy,currentMap):
	if(dx is not 0 or dy is not 0):
		actions.MoveAction(PARTY.getFocus(),currentMap,dx,dy).act()
		currentMap.fov_recompute=True

def rest(PARTY):
	actions.NoAction(PARTY.getFocus()).act()


#interface templates
		
class PartyInterface(Interface):
	def __init__(self,PARTY,map,game):
		Interface.__init__(self)
		kb={
		ltc.KEY_1: util.Delayed(setFocus,PARTY,0,map),
		ltc.KEY_2: util.Delayed(setFocus,PARTY,1,map),
		ltc.KEY_3: util.Delayed(setFocus,PARTY,2,map),
		ltc.KEY_4: util.Delayed(setFocus,PARTY,3,map),
		ltc.KEY_KP1 :util.Delayed(move, PARTY, -1,1,map),
		ltc.KEY_KP2 :util.Delayed(move, PARTY, 0,1,map),
		ltc.KEY_KP3 :util.Delayed(move, PARTY, 1,1,map),
		ltc.KEY_KP4 :util.Delayed(move, PARTY, -1,0,map),
		ltc.KEY_KP5 :util.Delayed(rest, PARTY),
		ltc.KEY_KP6 :util.Delayed(move, PARTY, 1,0,map),
		ltc.KEY_KP7 :util.Delayed(move, PARTY, -1,-1,map),
		ltc.KEY_KP8 :util.Delayed(move, PARTY, 0,-1,map),
		ltc.KEY_KP9 :util.Delayed(move, PARTY, 1,-1,map),
		}
		self.setKeyBindings(kb) 
		
		#TODO: introduce mousebinding	
		self.mouseBinding=util.Delayed(self.onMouse,PARTY,map,game)
		
		
	def onMouse(self,PARTY,map,game,mouse):
		if(mouse.rbutton):
			tilex=mouse.cx+game.mapTopLeftX()
			tiley=mouse.cy+game.mapTopLeftY()
			game.interface=ActionSelectInterface(PARTY.getFocus(),map,tilex,tiley,game)

class ActionSelectInterface(Interface):
	def __init__(self,creature,map,x,y,game):
		Interface.__init__(self)
		def goBack(game):
			game.interface=PartyInterface(game.PARTY,game.currentMap, game)
		
		#if the space is not blocked, you can move there, if you can move 
		self.setKeyBinding(ord('m'),util.ChainedDelay(util.Delayed(creature.giveOrder,orders.moveOrder(map,x,y)),util.Delayed(goBack,game)))
		
		#if the space has a creature, you can follow it
		if(map.creatureAt(x,y)):
			toFollow=map.getCreatureAt(x,y)
			self.setKeyBinding(ord('f'),util.ChainedDelay(util.Delayed(creature.giveOrder,orders.followOrder(map,toFollow)),util.Delayed(goBack,game)))
		
		#if the space is blocked, you might be able to do something depending on what is there:
			#if it is a door you can try to open it
			
			#if it is a wall you can fire