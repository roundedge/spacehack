import util

#actions are specifc things that can be done in the game world. Everything and anything a PC or NPC can do will be given by an action. They are essentially verbs. Might refactor this to get rid of the "Action" postfix.

class AttackAction:
	apCost=1
	
	def __init__(self, attacker, target):
		self.attacker=attacker
		self.target=target
	
	def validAction(self):
		if (self.attacker.combatant):
			if(self.target.mortal):
				if(self.attacker.combatant.inRangeOf(self.target)):
					return (True, 'valid')
				else:
					return (False, 'target out of range')
			else:
				return (False, 'target cant be attacked')
		else:
			return (False, 'attacker is not a combatant')
		
	def act(self):
		if(self.attacker.actor.ap >= self.apCost):
			(valid,reason)=self.validAction()
			if(valid):
				#spend your action points
				self.attacker.actor.ap=self.attacker.actor.ap-self.apCost
				#perform the action
				self.attacker.combatant.attack(self.target)
			else:
				self.fail(reason)
		else:
			self.fail('no ap on attack')
			
	def fail(self, reason):
		print(reason)

class MoveAction:
	apCost=1
	
	def __init__(self,object, dx, dy):
		self.object=object
		self.dx=dx
		self.dy=dy
		
	def validAction(self):
		if (self.dx is not 0 or self.dy is not 0):
			if (self.object.map.canMoveObject(self.object,self.dx,self.dy)):
				return (True,'valid')
			else:
				return (False,'blocked on move')
		else:
			return (False,'no motion on move')
	
	def act(self):
		if (self.object.actor.ap >= self.apCost):
			if (self.dx is not 0 or self.dy is not 0):
				if (self.object.move(self.dx,self.dy)):
					self.object.actor.ap=self.object.actor.ap-self.apCost
					self.object.map.fov_recompute=True
					#print('actor moved')
				else:
					self.fail('blocked on move')
			else:
				self.fail('no motion on move')
		else:
			self.fail('no ap on move')
	
	def fail(self, reason):
		print(reason)

class DropAction:
	apCost=1
	
	def __init__(self, obj, toDrop):
		self.obj=obj
		self.map=obj.map
		self.toDrop=toDrop

	def validAction(self):
		if(self.map==None):
			return (False, 'nowhere to drop it')
		
		if(self.obj.inventory):
			def isItem(o): return True if o.item else False
			if(util.trueForAll(self.toDrop, isItem)):
				def hasObject(o): return True if self.map.hasObject(o) else False
				if(util.trueForAll(self.toDrop,self.obj.inventory.hasObject)):
					return (True, 'valid')
				else:
					return (False,'item is not in the inventory')
			else:
				return (False, 'not an item')
		else:
			return (False, 'no inventory')
	
	def act(self):
		if(self.obj.actor.ap >= self.apCost):
			(valid,reason)=self.validAction()
			if(valid):
				#spend your action points
				self.obj.actor.ap=self.obj.actor.ap-self.apCost
				(x,y)=self.map.positionOf(self.obj)
				for o in self.toDrop:
					#remove the item from the inventory
					self.obj.inventory.removeItem(o)
					#add the item to the world
					self.map.addObject(o,x,y)
			else:
				self.fail(reason)
		else:
			self.fail('no ap on pickup')
			
	def fail(self, reason):
		print(reason)
		
class PickupAction:
	apCost=1
	
	def __init__(self,obj,map,toPickup):
		self.obj=obj
		self.map=map
		self.toPickup=toPickup
		
	def validAction(self):
		if(self.obj.inventory):
			def isItem(o): return True if o.item else False
			if(util.trueForAll(self.toPickup, isItem)):
				def hasObject(o): return True if self.map.hasObject(o) else False
				if(util.trueForAll(self.toPickup,self.map.hasObject)):
					return (True, 'valid')
				else:
					return (False,'item is not in the world')
			else:
				return (False, 'not an item')
		else:
			return (False, 'nowhere to put object')
		
	def act(self):
		if(self.obj.actor.ap >= self.apCost):
			(valid,reason)=self.validAction()
			if(valid):
				#spend your action points
				self.obj.actor.ap=self.obj.actor.ap-self.apCost
				for o in self.toPickup:
					#remove the item from the world
					self.map.removeObject(o)
					#add the item to the inventory
					self.obj.inventory.addItem(o)
			else:
				self.fail(reason)
		else:
			self.fail('no ap on pickup')
			
	def fail(self, reason):
		print(reason)

class ActivateTileAction:
	apCost=1
	
	def __init__(self,obj,map,tile):
		self.obj=obj
		self.map=map
		self.tile=tile
		
	def validAction(self):
		if(self.tile.activateable):
			return (True, 'valid')
		else:
			return (False, 'cant be activated')
	
	def act(self):
		if(self.obj.actor.ap >= self.apCost):
			(valid,reason)=self.validAction()
			if(valid):
				#spend your action points
				self.obj.actor.ap=self.obj.actor.ap-self.apCost
				#activate the tile
				self.tile.activateable.activate(self.obj)
			else:
				self.fail(reason)
		else:
			self.fail('no ap on pickup')
			
	def fail(self, reason):
		print(reason)
		
class GeneralAction:

	def __init__(self,object,subject,conditionsCB,actCB,apCost=1):
		self.apCost=apCost
		self.contionsCB=conditionsCB
		self.actCB=actCB
		self.object=object
		self.subject=subject
		
	def validAction(self):
		return self.conditionsCB(self.object,self.subject)
		
	def act(self):
		if(self.object.actor.ap >= self.apCost):
			(valid,reason)=self.validAction()
			if(valid):
				#spend your action points
				self.obj.actor.ap=self.obj.actor.ap-self.apCost
				#perform the action
				self.actCB(self.object,self.subject)
			else:
				self.fail(reason)
		else:
			self.fail('no ap on pickup')	
		
class NoAction:
	apCost=1
	
	def __init__(self, object):
		self.object=object
	
	def act(self):
		if (self.object.actor.ap >= self.apCost):
			self.object.actor.ap=self.object.actor.ap-self.apCost