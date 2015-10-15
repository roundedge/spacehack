import libtcodpy as libtcod

class Object:

	#so the Object class has its own namespace, and it is there that we can put default instances of all the components,
	# so we don't have to constantly be asking wether the object has an instance of it. 
	#This means making default objects.. is this wise? We do not want to be misleading about the functionality of an object

	#this is a generic object: the player, a monster, an item, the stairs..
	#its always represented by a character on screen.
	def __init__(self,char,color,name="no name",description="a featureless object",actor=None, item=None, inventory=None, weildable=None, wearable=None, mortal=None, combatant=None):
		self.char=char
		self.color=color
		self.name=name
		self.actor=actor
		self.item=item
		self.inventory=inventory
		self.weildable=weildable
		self.wearable=wearable
		self.mortal=mortal
		self.combatant=combatant
		self.map=None
		
		if self.actor:
			self.actor.owner=self
		
		if self.item:
			self.item.owner=self
	
		if self.inventory:
			self.inventory.owner=self
			
		if self.weildable:
			self.weildable.owner=self
			
		if self.wearable:
			self.wearable.owner=self
			
		if self.mortal:
			self.mortal.owner=self
		
		if self.combatant:
			self.combatant.owner=self
		
		
	def getName(self):
		nameToGive=self.name
		if self.item and self.item.stackable:
			nameToGive=nameToGive+ " ("+str(self.item.stackable.amount)+")"
		
		return nameToGive
	
	def setName(self, name):
		self.name=name
	
	def move(self,dx,dy):
		#the object should just tell the map it wants to move, the map should decide if the object can move,
		if(self.map):
			self.map.moveObject(self,dx,dy)
			return True
		else:
			return False
		
	def position(self):
		if(self.map):
			return self.map.positionOf(self)
		else:
			return None
			
	def inView(self, object, radius):
		if(self.map):
			(xi,yi)=self.map.positionOf(self)
			(xf,yf)=self.map.positionOf(object)
			return map.inFieldOfView(xi,yi,xf,yf,radius)
		
	def removeFromMap(self):
		if(self.map):
			return self.map.removeObject(self)
		else:
			return False
	
	def kill(self):
		self.removeFromMap()
		if(self.actor and self.actor.party):
			self.actor.party.removeMember(self)
	
	
	def draw(self,isVisible,x,y,screen):
		if isVisible:
			#set the color and then draw the character that represents this object at its position
			libtcod.console_set_default_foreground(screen ,self.color)
			libtcod.console_put_char(screen, x, y, self.char, libtcod.BKGND_NONE)
	

		
	def clear(self,x,y,screen):
		#erase the character that represents this object
		libtcod.console_put_char(screen, x, y, ' ', libtcod.BKGND_NONE)