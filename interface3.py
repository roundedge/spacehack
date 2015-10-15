

#keycode structure

#vk	An arbitrary value representing the physical key on the keyboard. Possible values are stored in the TCOD_keycode_t enum. If no key was pressed, the value is TCODK_NONE
#c	If the key correspond to a printable character, the character is stored in this field. Else, this field contains 0.
#pressed	true if the event is a key pressed, or false for a key released.
#lalt	This field represents the status of the left Alt key : true => pressed, false => released.
#lctrl	This field represents the status of the left Control key : true => pressed, false => released.
#ralt	This field represents the status of the right Alt key : true => pressed, false => released.
#rctrl	This field represents the status of the right Control key : true => pressed, false => released.
#shift	This field represents the status of the shift key : true => pressed, false => released.
		

		
#interface3
import libtcodpy as ltc
import actions
import util
import orders
import object

menu_width=40
menu_height=40


class Interface:
	#this caries over to other interfaces, so we can swap between them without having to keep track
	keyState={}
	UP=0
	DOWN=1
	JUST_PRESSED=2
	JUST_RELEASED=3
	
	def __init__(self):
		self.keyBinding=({},{},{},{})
		self.mouseBinding=None
		self.options=[]
		

	def setKeyBindings(self,keyBindings, state=JUST_PRESSED):
		self.keyBinding[state].update(keyBindings)
	
	def setKeyBinding(self, key, binding, state=JUST_PRESSED):
		self.keyBinding[state][key]=binding
		
	def setMouseBinding(self, mouseBinding):
		self.mouseBinding=mouseBinding
		
	def onKeyEvent(self,key):
		UP=0
		DOWN=1
		JUST_PRESSED=2
		JUST_RELEASED=3
		#get the key:
		keyType=key.vk	
		keyDown=key.pressed
		
		if(keyType==ltc.KEY_CHAR):
			keyType=chr(key.c)
		
		registered=self.keyState.has_key(keyType)
		if(not registered):
			self.keyState[keyType]=(JUST_PRESSED if keyDown else JUST_RELEASED)
			print "on key event"
			print "key just pressed: "+ str(keyType)
		else:
			state=self.keyState[keyType]
			if(state==UP and keyDown):
				self.keyState[keyType]=JUST_PRESSED
				print "on key event"
				print "key just pressed: "+ str(keyType) 
			if(state==DOWN and not keyDown):
				self.keyState[keyType]=JUST_RELEASED
				print "on key event"
				print "key just released: "+ str(keyType) 
		
		#for k in self.keyState.keys():
		#	if self.keyState[k]==DOWN and not (k==keyType):
		#		self.keyState[k]=JUST_RELEASED
		#		print "key just released: "+ str(k) 
		
		#iterate through the keybindings and check if the conditions are satisfied
		quitGame=False
		for i in range(JUST_RELEASED+1):
			for k in self.keyBinding[i].keys():
				if self.keyState.has_key(k) and self.keyState[k]==i:
					#activates the delayed function in that keybinding
					out=self.call(self.keyBinding[i][k])
					quitGame=(out or quitGame)
		
		#now that we have just pressed or released, we can switch to up or down
		for k in self.keyState.keys():
			if self.keyState[k]==JUST_PRESSED:
				self.keyState[k]=DOWN
			if self.keyState[k]==JUST_RELEASED:
				self.keyState[k]=UP
		
		return quitGame
	
	@staticmethod		
	def call(list):
		quitGame=False
		for command in list:
			out=command[0](*command[1:])
			quitGame=(out or quitGame)
		return quitGame
			
	def onMouseEvent(self, mouse):
		if(self.mouseBinding is not None):
			return self.mouseBinding.call(mouse)
			
	def draw(self, screen):
		menu=ltc.console_new(menu_width,menu_height)
		ltc.console_print(menu,0,0,"--------------------")
		for i in range(len(self.options)):
			ltc.console_print(menu,0,i+1,self.options[i])
		
		ltc.console_blit(menu,-ltc.console_get_width(screen)+menu_width,-20,menu_width+ltc.console_get_width(screen),menu_height,0,0,0)
		ltc.console_delete(menu)

#interface commands
def setFocus(PARTY,value):
	PARTY.setFocus(value)
	for m in PARTY.getCurrentMaps():
		m.fov_recompute=True

def move(PARTY,dx,dy):
	if(dx is not 0 or dy is not 0):
		toMove=PARTY.getFocus()
		#check if one of your party members is in the way
		if(toMove.map):
			x,y=toMove.position()
			map=toMove.map
			for dude in PARTY.members:
				if(dude in map.objectsAt(x+dx,y+dy)):
					actions.SwapPlacesAction(toMove, dude).act()
					return

		actions.MoveAction(toMove,dx,dy).act()
		#currentMap.fov_recompute=True

def pickup(PARTY,toPickup):
	map=PARTY.getFocus().map
	if(map):
		actions.PickupAction(PARTY.getFocus(),map,toPickup).act()

def rest(PARTY):
	actions.NoAction(PARTY.getFocus()).act()	


def exit():
	return True
	
#interface templates
		
class PartyInterface(Interface):
	def __init__(self,PARTY,game):
		Interface.__init__(self)
		
		def switchToPickup():
			(x,y)=PARTY.getFocus().position()
			game.interface=PickupItemInterface(PARTY,x,y,game)
			
		def switchToDrop():
			game.interface=DropItemInterface(PARTY,game)
			
		def switchToActivate():
			(x,y)=PARTY.getFocus().position()
			game.interface=ActivateInterface(PARTY,x,y,game)

			
		kb={
		ltc.KEY_1: [(setFocus,PARTY,0)],
		ltc.KEY_2: [(setFocus,PARTY,1)],
		ltc.KEY_3: [(setFocus,PARTY,2)],
		ltc.KEY_4: [(setFocus,PARTY,3)],
		ltc.KEY_KP1 :[(move, PARTY, -1,1)],
		ltc.KEY_KP2 :[(move, PARTY, 0,1)],
		ltc.KEY_KP3 :[(move, PARTY, 1,1)],
		ltc.KEY_KP4 :[(move, PARTY, -1,0)],
		ltc.KEY_KP5 :[(rest, PARTY)],
		ltc.KEY_KP6 :[(move, PARTY, 1,0)],
		ltc.KEY_KP7 :[(move, PARTY, -1,-1)],
		ltc.KEY_KP8 :[(move, PARTY, 0,-1)],
		ltc.KEY_KP9 :[(move, PARTY, 1,-1)],
		ltc.KEY_ESCAPE:[(exit,)],
		's' :[(move, PARTY, 0,1)],
		'a' :[(move, PARTY, -1,0)],
		'd' :[(move, PARTY, 1,0)],
		'w' :[(move, PARTY, 0,-1)],
		',' :[(switchToPickup,)],
		'<' :[(switchToDrop,)],
		ltc.KEY_ENTER:[(switchToActivate,)],
		}
		self.setKeyBindings(kb) 
		self.options=["#: select party member", "awsd or numpad: move","right click: take action at location","Enter: Activate"]	
		self.mouseBinding=util.Delayed(self.onMouse,PARTY,game)
		
		#held button key bindings
		kb={
		ltc.KEY_KP1 :[(move, PARTY, -1,1)],
		ltc.KEY_KP2 :[(move, PARTY, 0,1)],
		ltc.KEY_KP3 :[(move, PARTY, 1,1)],
		ltc.KEY_KP4 :[(move, PARTY, -1,0)],
		ltc.KEY_KP5 :[(rest, PARTY)],
		ltc.KEY_KP6 :[(move, PARTY, 1,0)],
		ltc.KEY_KP7 :[(move, PARTY, -1,-1)],
		ltc.KEY_KP8 :[(move, PARTY, 0,-1)],
		ltc.KEY_KP9 :[(move, PARTY, 1,-1)],
		's' :[(move, PARTY, 0,1)],
		'a' :[(move, PARTY, -1,0)],
		'd' :[(move, PARTY, 1,0)],
		'w' :[(move, PARTY, 0,-1)],
		}
		
		self.setKeyBindings(kb,state=self.DOWN) 
		
		
	def onMouse(self,PARTY,game,mouse):
		if(mouse.rbutton):
			tilex=mouse.cx+game.mapTopLeftX()
			tiley=mouse.cy+game.mapTopLeftY()
			game.interface=ActionSelectInterface(PARTY.getFocus(),tilex,tiley,game)
		


class SelectionInterface(Interface):
	#TODO: improvements
	#indicate when there are more pages
	#include a select all, and a deselect all
	
	
	def __init__(self, selections, selectionNames, selectionCallback, singleSelection=False):
		Interface.__init__(self)
		self.page=0
		self.number=len(selections)
		self.selections=selections
		self.selectionNames=selectionNames
		self.maxPage=self.number/10+1
		self.selectionCallback=selectionCallback
		self.selection=[False for x in range(self.number)]
		
		self.setKeyBinding('>',[(self.deltaPage,1)])
		self.options.append(">: next page")
		self.setKeyBinding('<',[(self.deltaPage,-1)])
		self.options.append("<: previous page")
		#thanks libtcod for making this tedious :)
		self.setKeyBinding(ltc.KEY_0,[(self.toggleSelection,0)])
		self.setKeyBinding(ltc.KEY_1,[(self.toggleSelection,1)])
		self.setKeyBinding(ltc.KEY_2,[(self.toggleSelection,2)])
		self.setKeyBinding(ltc.KEY_3,[(self.toggleSelection,3)])
		self.setKeyBinding(ltc.KEY_4,[(self.toggleSelection,4)])
		self.setKeyBinding(ltc.KEY_5,[(self.toggleSelection,5)])
		self.setKeyBinding(ltc.KEY_6,[(self.toggleSelection,6)])
		self.setKeyBinding(ltc.KEY_7,[(self.toggleSelection,7)])
		self.setKeyBinding(ltc.KEY_8,[(self.toggleSelection,8)])
		self.setKeyBinding(ltc.KEY_9,[(self.toggleSelection,9)])
		self.options.append("0-9: selection")
		self.setKeyBinding(ltc.KEY_ENTER,[(self.passSelection,)])
		
		self.singleSelection=singleSelection
		if(singleSelection):
			#if it's a single selection, always mark the first one
			if(self.number>0):
				self.selection[0]=True
		
	def deltaPage(self,i):
		#print("delta page")
		self.page=self.page+i
		self.page=self.page%self.maxPage
		
	def toggleSelection(self,i):
		i=i+10*self.page
		if(0<=i and i<self.number):
			if(self.singleSelection):
				#if we only ever select a single one
				for k in range(self.number):
					#turn off all the selections
					self.selection[k]=False
				self.selection[i]=True
			else:
				self.selection[i]=not self.selection[i]
			
	def passSelection(self):
		toPass=[]
		for i in range(self.number):
			if(self.selection[i]):
				toPass.append(self.selections[i])
		self.selectionCallback(toPass)
	
	selectionTitle="Select what?"
	
	def draw(self, screen):
		menu=ltc.console_new(menu_width,menu_height)
		ltc.console_print(menu,0,0,self.selectionTitle)
		ltc.console_print(menu,0,1,"--------------------")
		for i in range(self.page*10,self.page*10+10 if len(self.selectionNames)>self.page*10+10 else len(self.selectionNames)):
			ltc.console_print(menu,0,i+2-self.page*10,str(i)+":"+self.selectionNames[i]+" "+('[O]' if self.selection[i] else '[ ]'))
		
		ltc.console_blit(menu,-ltc.console_get_width(screen)+menu_width,-20,menu_width+ltc.console_get_width(screen),menu_height,0,0,0)
			
class PickupItemInterface(SelectionInterface):#TODO
	selectionTitle="Pick up what?"

	def __init__(self,PARTY,x,y,game):
		#print("pickup Item Interface")
		map=PARTY.getFocus().map
		items=[]
		if(map):
			items=map.getItemsAt(x,y)
		names=[x.getName() for x in items]
		#define a callback for the selection we make
		def onSelect(toPickup):
			pickup(PARTY,toPickup)
			#print("picked up item")
			PARTY.setFocus(0)
			goBack()
		
		SelectionInterface.__init__(self,items,names,onSelect)
		
		def goBack():
			game.interface=PartyInterface(PARTY, game)	
		
		#you can go back
		self.setKeyBinding(ltc.KEY_ESCAPE,[(goBack,)])
		self.options.append("esc: go back")
		
class DropItemInterface(SelectionInterface):
	
	selectionTitle="Drop what?"

	def __init__(self,PARTY,map,game):
		#print("drop Item Interface")
		items=PARTY.getFocus().inventory.items
		names=[x.getName() for x in items]
		#define a callback for the selection we make
		def onSelect(toPickup):
			actions.DropAction(PARTY.getFocus(),toPickup).act()
			#print("dropped an item")
			PARTY.setFocus(0)
			goBack()
		
		SelectionInterface.__init__(self,items,names,onSelect)
		
		def goBack():
			game.interface=PartyInterface(PARTY, game)
		
		#you can go back
		self.setKeyBinding(ltc.KEY_ESCAPE,[(goBack,)])
		self.options.append("esc: go back")
			
class ActivateInterface(SelectionInterface):
	selectionTitle="Activate what?"
	
	def __init__(self,PARTY,x,y,game):
		map=PARTY.getFocus().map
		activateableTiles=[]
		directions=[]
		if(map):
			(activateableTiles,directions)=map.getActivateableTilesAround(x,y)
		names=[]
		for i in range(len(activateableTiles)):
			names.append(activateableTiles[i].name+" ("+directions[i]+")")
			
		def onSelect(toActivate):
			if(len(toActivate)>0):
				toActivate[0].activateable.activate(PARTY.getFocus())
			PARTY.setFocus(0)
			goBack()
		
		SelectionInterface.__init__(self,activateableTiles,names,onSelect,singleSelection=True)
		
		def goBack():
			game.interface=PartyInterface(PARTY, game)	
		
		#you can go back
		self.setKeyBinding(ltc.KEY_ESCAPE,[(goBack,)])
		self.options.append("esc: go back")
	
class ActionSelectInterface(Interface):
	def __init__(self,obj,x,y,game):
		Interface.__init__(self)
		cursor=object.Object(ltc.CHAR_CHECKBOX_UNSET,ltc.red)
		map=obj.map
		def goBack():
			game.interface=PartyInterface(game.PARTY, game)
			if(map):
				map.removeObject(cursor)
			game.PARTY.setFocus(0)
		

		#you can go back
		self.setKeyBinding(ltc.KEY_ESCAPE,[(goBack,)])
		self.options.append("esc: go back")
		
		if(obj.map==None):
			return
		
		obj.map.addObject(cursor,x,y)
			
		#if the space is not blocked, you can move there, if you can move 
		self.setKeyBinding('m',[(obj.actor.giveOrder,orders.moveOrder(map,x,y)),(goBack,)])
		self.options.append("m: move to")
		
		#if the space has a actor, you can follow it
		if(map.actorAt(x,y)):
			toFollow=map.getActorAt(x,y)
			self.setKeyBinding('f',[(obj.actor.giveOrder,orders.followOrder(map,toFollow)),(goBack,)])
			self.options.append("f: follow")
		
		#if there are activateable things here, you can activate it
		if(map.tile(x,y).activateable):
			self.setKeyBinding('a',[(obj.actor.giveOrder,orders.activateOrder(map,x,y)),(goBack,)])
			self.options.append("a: activate "+map.tile(x,y).name)
			
		#if there is a mortal there, you can attack it
		mortals=map.getTypeAt(x,y,"mortal")
		if(len(mortals)>0 and obj.combatant):
			#todo multiple enemies at the site
			action = actions.AttackAction(obj, mortals[0])
			self.setKeyBinding('k',[(action.act,),(goBack,)])
			self.options.append("k: attack "+mortals[0].name)
		
		#if the space is blocked, you might be able to do something depending on what is there:
			#if it is a door you can try to open it
			
			#if it is a wall you can fire
			#if it is a wall you can fire