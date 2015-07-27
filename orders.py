import actions
import libtcodpy as ltc

#Orders are behaviours which can be given to actors and the actors will carry them out until the order terminates itself. They are essentially AI Note that more than one actor can be given the same order

#here's the issue with pathing: if your destination tile is blocked, and you try to path there, you're going to stall, and then not path there. It would be nice if even if the destination were blocked it would treat it like it weren't. So we're going to do that by encoding it in the map callback
def pathingCallback(xFrom,yFrom,xTo,yTo,arg):
	map=arg[0]
	xDest=arg[1]
	yDest=arg[2]
	if(xTo==xDest and yTo==yDest):
		return 1
	else:
		return map.pathCost(xFrom,yFrom,xTo,yTo)

def moveTowards(object,map,moveTox,moveToy):
	moved=False
	atDestination=False
	#note that in order for the callback arguments to work, arg must still be loaded when the callback is called
	arg=(map,moveTox,moveToy)
	path=ltc.path_new_using_function(map.width, map.height,pathingCallback,arg)
	ltc.path_compute(path,map.x(object),map.y(object),moveTox,moveToy)
	x,y = ltc.path_walk(path,True)
	if(x==None or y==None):
		atDestination=True
	else:
		motion=actions.MoveAction(object, x-map.x(object),y-map.y(object))
		(valid,reason)=motion.validAction()
		if(valid):
			motion.act()
			moved=True
	ltc.path_delete(path)	
	return (moved, atDestination)

class moveOrder:
	#moves to a specific location
	def __init__(self,map,moveToX,moveToY,untilYouGetThere=True):
		self.map=map
		self.moveToX=moveToX
		self.moveToY=moveToY
		self.untilYouGetThere=untilYouGetThere #don't stop trying until you reach your destination
		
	def resolve(self, object):
		(moved,atDestination)=moveTowards(object, self.map, self.moveToX,self.moveToY)
		if(atDestination):
			object.actor.giveOrder(noOrder())
		if(not moved and not self.untilYouGetThere):
			object.actor.giveOrder(noOrder())
		
		
	def title(self):
		return "moving to "+str(self.moveToX)+", "+str(self.moveToY)
		
		
class moveOrderOld:
	#moves to a specific location
	def __init__(self,map,moveToX,moveToY):
		self.map=map
		self.moveToX=moveToX
		self.moveToY=moveToY
		
	def resolve(self, object):
		#note that in order for the callback arguments to work, arg must still be loaded when the callback is called
		arg=(self.map,self.moveToX,self.moveToY)
		path=ltc.path_new_using_function(self.map.width, self.map.height,pathingCallback,arg)
		ltc.path_compute(path,self.map.x(object),self.map.y(object),self.moveToX,self.moveToY)
		x,y = ltc.path_walk(path,True)
		if(x==None or y==None):
			object.actor.giveOrder(noOrder())
		else:
			actions.MoveAction(object, x-self.map.x(object),y-self.map.y(object)).act()
		ltc.path_delete(path)
		
	def title(self):
		return "moving to "+str(self.moveToX)+", "+str(self.moveToY)
		
class followOrder:
	#figures out where the thing is, and follows it
	
	def __init__(self, map, toFollow):
		self.map=map
		self.toFollow=toFollow
		
	def resolve(self, object):
		xDest=self.map.x(self.toFollow)
		yDest=self.map.y(self.toFollow)
		arg=(self.map,xDest,yDest)
		path=ltc.path_new_using_function(self.map.width, self.map.height,pathingCallback,arg)
		ltc.path_compute(path,self.map.x(object),self.map.y(object),self.map.x(self.toFollow),self.map.y(self.toFollow))
		x,y = ltc.path_walk(path,True)
		if(x==None or y==None):
			actions.NoAction(object).act()
		else:
			actions.MoveAction(object, x-self.map.x(object),y-self.map.y(object)).act()
		ltc.path_delete(path)
	
	def title(self):
		return "following "+self.toFollow.getName()

	
class activateOrder:
	
	def __init__(self,map,tileX,tileY):
		self.map=map
		self.tileX=tileX
		self.tileY=tileY
		
	def resolve(self, object):
		#check if you're near the tile
		(x,y)=self.map.positionOf(object)
		tileX=self.tileX
		tileY=self.tileY
		if( (tileX==x+1 and tileY==y) or (tileX==x-1 and tileY==y) or (tileX==x and tileY==y+1) or (tileX==x and tileY==y-1) or (tileX==x and tileY==y)):
			#if you are, activate it
			if(self.map.tile(tileX,tileY).activateable):
				self.map.tile(tileX,tileY).activateable.activate(object)
			object.actor.giveOrder(noOrder())
		#if you're not near the tile, move towards it
		else:
			moveTowards(object,self.map, self.tileX,self.tileY)
		
	def title(self):
		return "activating "+self.map.tile(self.tileX,self.tileY).name+" at ("+ str(self.tileX)+","+str(self.tileY)+")"
		
class noOrder:

	def __init__(self):
		pass
	
	def resolve(self,object):
		#spend all the action points
		object.actor.ap=0
		
	def title(self):
		return "doing nothing"