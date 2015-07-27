import object

class Inventory:
	
	def __init__(self):
		self.items=[]
	
	def removeItem(self, obj):
		if self.hasObject(obj): self.items.remove(obj)
	
	def addItem(self, obj):
		added=False
		if(obj.item.stackable):
			for o in self.items:
				if o.item.stackable:
					if o.item.stackable.joinWith(obj):
						added=True
						break
		if(not added):
			self.items.append(obj)
			added=True
		return added
		
	def hasObject(self,o):
		return o in self.items
				
#perhaps we need to employ composition for our items. Some compositions are:
	#stackable, weildable, etc. in fact, let's do the composition thing with our objects as well 

class Item:
	def __init__(self, useFunction=None, stackable=None):
		self.useFunction=useFunction
		self.stackable=stackable
		
		if self.stackable:
			self.stackable.owner=self
		
	def use():
		if(self.useFunction is None):
			pass
		else:
			self.useFunction.__call__(self.owner)
		
class Stackable():

	def __init__(self, uniqueID):
		self.amount=1;
		self.uniqueID=uniqueID
	
	def canJoinWith(self, obj):
		if obj.item and obj.item.stackable:
			return obj.item.stackable.uniqueID==self.uniqueID
		else:
			return False
	
	def joinWith(self, obj):
		if(self.canJoinWith(obj)):
			self.amount=self.amount+obj.item.stackable.amount
			return True
		else:
			return False