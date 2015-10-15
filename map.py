import libtcodpy as ltc

import tileStyles
import actor
import util

class Map:
	#general map object
	
	#boundary conditions
	HARD_BOUNDARY=0
	PERIODIC_BOUNDARY=1
	
	#Field of View
	FOV_ALGO = 0
	FOV_LIGHT_WALLS = True
	TORCH_RADIUS=10
	
	
	def __init__(self, width,height):
		self.fov_recompute=True
		self.bc=Map.PERIODIC_BOUNDARY
	
		self.width=width
		self.height=height
		self.tiles=[[ Floor()
			for y in range(self.height)]
				for x in range(self.width)]
		
		self.objects=[[[] 
			for y in range(self.height)]
				for x in range(self.width)]
		
		self.positions={}
		
		#FOV
		self.initializeFOV()
		self.visibility=[[ False
			for y in range(self.height)]
				for x in range(self.width)]
	
	def initializeFOV(self):
		self.fov_map=ltc.map_new(self.width,self.height)
		for x in range(self.width):
			for y in range(self.height):
				ltc.map_set_properties(self.fov_map,x,y, not self.tile(x,y).block_sight, not self.tile(x,y).blocked)
		
	def tile(self, x,y):
		return self.tiles[x][y]
	
	def setTile(self,x,y,tile):
		self.tiles[x][y]=tile
	
	def draw(self,PARTY, screen, mapWindow):
		yi=mapWindow.topLeft().y if mapWindow.topLeft().y < self.height else self.height
		yf=mapWindow.bottomRight().y if mapWindow.bottomRight().y < self.height else self.height
		
		xi=mapWindow.topLeft().x if mapWindow.topLeft().x < self.width else self.width
		xf=mapWindow.bottomRight().x if mapWindow.bottomRight().x < self.width else self.width

	
		if self.fov_recompute:
			#recompute FOV if needed (the player moved or something)
			self.fov_recompute=False
			for y in range(yi if yi>=0 else 0,yf):
					for x in range(xi if xi>=0 else 0,xf):
						self.visibility[x][y]=False
			for member in PARTY.members:
				fov=ltc.map_new(self.width,self.height)
				ltc.map_copy(self.fov_map,fov)
				ltc.map_compute_fov(fov,self.positionOf(member)[0],self.positionOf(member)[1], self.TORCH_RADIUS, self.FOV_LIGHT_WALLS, self.FOV_ALGO)
				for y in range(yi,yf):
					for x in range(xi,xf):
						if ltc.map_is_in_fov(fov,x,y):
							self.visibility[x][y]=True
			
			#ltc.map_compute_fov(self.fov_map,self.positionOf(PARTY.getFocus())[0],self.positionOf(PARTY.getFocus())[1], self.TORCH_RADIUS, self.FOV_LIGHT_WALLS, self.FOV_ALGO)
		
		for y in range(yi if yi>=0 else 0,yf):
			for x in range(xi if xi>=0 else 0,xf):
				screen_x=x-xi
				screen_y=y-yi
				visible=ltc.map_is_in_fov(self.fov_map,x,y)
				self.tile(x,y).draw(screen_x,screen_y, self.visibility[x][y] ,screen)
				for o in self.objects[x][y]:
					o.draw(self.visibility[x][y],screen_x,screen_y,screen)

	def inFieldOfView_private(self,xi,yi,xf,yf,radius):
		#this could probably be sped up with a bresenham line alrogithm?
		fov=ltc.map_new(self.width,self.height)
		ltc.map_copy(self.fov_map,fov)
		ltc.map_compute_fov(fov,xi,yi, self.TORCH_RADIUS, self.FOV_LIGHT_WALLS, self.FOV_ALGO)
		return ltc.map_is_in_fov(fov,xf,yf)
		
	def inFieldOfView(self, obj1, obj2, radius):
		if(self.hasObject(obj1) and self.hasObject(obj2)):
			(xi,yi)=self.positionOf(obj1)
			(xf,yf)=self.positionOf(obj2)
			return self.inFieldOfView_private(xi,yi,xf,yf,radius)
		else:
			return False
					
	def withinBoundaries(self, endPosx, endPosy):
		return not (endPosx<0 or endPosx>=self.width or endPosy<0 or endPosy>=self.height)				
	
	def checkBoundaries(self, startPosx, startPosy, endPosx, endPosy):
		if not self.withinBoundaries(endPosx, endPosy):
			if(self.bc==self.PERIODIC_BOUNDARY):
				return (endPosx%self.width, endPosy%self.height)
			else:
				print("hard boundary")
				return (startPosx,startPosy)
		else:
			return (endPosx,endPosy)
	
	def hasObject(self, object):
		return self.positions.get(object) is not None
	
	def allObjects(self):
		return util.collapse(util.collapse(self.objects))

	def objectsAt(self,x,y):
		#TODO: check boundaries and ensure immutability
		return self.objects[x][y]
	
	def actorAt(self, x,y):
		for o in self.objects[x][y]:
			if o.actor:
				return True
		return False
	
	def getActorAt(self,x,y):
		for o in self.objects[x][y]:
			if o.actor:
				return o
		return None
	
	def actors(self):
		c=[]
		obj=self.allObjects()
		for o in obj:
			if o.actor:
				c.append(o)
		return c
	
	def npcs(self, party):
		c=[]
		obj=self.allObjects()
		for o in obj:
			if o.actor and o.actor.NPC:
				c.append(o)
		return c
		
	def items(self):
		items=[]
		for o in self.objects[x][y]:
			if o.item:
				items.append(o)
		return items
	
	def getItemsAt(self,x,y):
		items=[]
		for o in self.objects[x][y]:
			if o.item:
				items.append(o)
		return items
		
	def getTypeAt(self,x,y,type):
		objects=[]
		for o in self.objects[x][y]:
			if getattr(o,type):
				objects.append(o)
		return objects
		
	def getActivateableTilesAround(self,x,y):
		activateables=[]
		directions=[]
		if(self.tile(x,y).activateable):
			directions.append("here")
			activateables.append(self.tile(x,y))
		
		if(self.tile(x+1,y).activateable):
			directions.append("East")
			activateables.append(self.tile(x+1,y))
			
		if(self.tile(x-1,y).activateable):
			directions.append("West")
			activateables.append(self.tile(x-1,y))

		if(self.tile(x,y+1).activateable):
			directions.append("South")
			activateables.append(self.tile(x,y+1))
			
		if(self.tile(x,y-1).activateable):
			directions.append("North")
			activateables.append(self.tile(x,y-1))
			
		return (activateables,directions)
		
		
	def isBlocked(self,x,y):
		return self.tile(x,y).blocked or self.actorAt(x,y)
	
	def pathCost(self,xFrom,yFrom,xTo,yTo):
		#must return the walk cost from and to coordinates
		#the cost must be >0.0f if the cell xTo,yTo is walkable
		#it must be equal to 0.0f if it is not
		#do not worry about diagonal movements
		if(self.isBlocked(xTo,yTo)):
			return 0
		else:
			return 1
	
	def pathThrough(self,x, y, dx, dy):
		ltc.line_init(x,y,x+dx,y+dy)
		pathx=x
		pathy=y
		prevpathx=x
		prevpathy=y
		pathx, pathy=ltc.line_step ()
		while(pathx is not None):
			#iterate through the path
			#if you are beyond the world
			if not self.withinBoundaries(pathx, pathy):
				if(self.bc==self.PERIODIC_BOUNDARY):
					pathx=pathx%self.width
					pathy=pathy%self.height
				else:
					#hard boundary
					return prevpathx,prevpathy,True
			#if you move into a blocked space, or there is a actor there
			if(self.isBlocked(pathx,pathy)):
				return prevpathx, prevpathy, True
			prevpathx=pathx
			prevpathy=pathy
			pathx, pathy=ltc.line_step ()
		return prevpathx, prevpathy,False
		
	def moveObject(self, object, dx,dy, moveOnFailure=False):
		#the move on failure term ensure that for instance a projectile travelling to a point can hit a wall and stop at the wall, if moveOnFailure is true, then the moving object will stop when it reaches an obstacle. If it is false it will never depart.
		if(not self.hasObject(object)):
			print('no such object')
			return False
		else:
			oldPos=self.positions[object]
			#check that the path isn't blocked
			newPosx, newPosy, blocked=self.pathThrough(oldPos[0],oldPos[1],dx,dy)
			#if it failed to reach its goal, and we dont move on a failure, then we do nothing
			if(blocked and not moveOnFailure):
				return False
			#otherwise we move to the new location
			#remove the object
			self.objects[oldPos[0]][oldPos[1]].remove(object)
			#add it again at its new position
			self.positions[object]=(newPosx,newPosy)
			self.objects[newPosx][newPosy].append(object)
			return True
			
	def canMoveObject(self,object,dx,dy,moveOnFailure=False):
		if(not self.hasObject(object)):
			print('no such object')
			return False
		else:
			oldPos=self.positions[object]
			#check that the path isn't blocked
			newPosx, newPosy, blocked=self.pathThrough(oldPos[0],oldPos[1],dx,dy)
			#if it failed to reach its goal, and we dont move on a failure, then we do nothing
			if(blocked and not moveOnFailure):
				return False
			else:
				return True
				
			
	def addObject(self, object,x,y):
		#make sure this object doesn't exist here already
		if(self.hasObject(object)):
			return False
		#check if you're putting the object within bounds
		if(not self.withinBoundaries(x,y)):
			return False
		
		added=False
		
		if object.item:
			#if your object is an item and that item is stackable, check if the same stackable type is at this location, and add it to the stack instead:
			if(object.item.stackable):
				for o in self.objects[x][y]:
					if o.item and o.item.stackable:
						if o.item.stackable.joinWith(object):
							added=True
							break
		if(not added):
			self.positions[object]=(x,y)
			self.objects[x][y].append(object)
			added=True
			
		if added:
			object.map=self
		return added
	
	
	def removeObject(self, object):
		removed=False
	
		if(self.hasObject(object)):
			(x,y)=self.positions[object]
			del self.positions[object]
			self.objects[x][y].remove(object)
			removed=True
		
		if removed:
			object.map=None
		
		return removed
	
	def positionOf(self,object):
		if self.hasObject(object):
			return self.positions[object]
		else:
			return (-1,-1)
			
	def x(self,object):
		return self.positionOf(object)[0]
		
	def y(self,object):
		return self.positionOf(object)[1]
	
class Tile:
	#a tile of the map
	def __init__(self, blocked, drawCB, block_sight=None, name="Tile",activateable=None):
		#draw callback contract:
		#	draw(x,y,visible,screen)
		self.blocked = blocked
		self.name=name
		self.drawCB=drawCB
		#by default, if a tile is blocked, it also blocks sight
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight
		
		self.activateable=activateable
		if(self.activateable):
			self.activateable.owner=self

		
	def draw(self, x,y,visible,screen):
		wall=self.block_sight
		if self.activateable and self.activateable.activated:
			self.activateable.draw(x,y,visible,screen)
		else:
			self.drawCB.__call__(x,y,visible,screen)
			

class Activateable:
	def __init__(self, onActivateCB, activatedDrawCB):
		self.activated=False
		self.onActivateCB=onActivateCB
		self.activatedDrawCB=activatedDrawCB
		self.owner=None
		#onActivate callback contract:
		#	onActivate(tile (Tile), activator (Object))
		
	def activate(self,activator):
		self.activated= not self.activated
		self.onActivateCB.__call__(self.owner, activator)
		
	def draw(self,x,y,visible,screen):
		self.activatedDrawCB.__call__(x,y,visible,screen)
	
def bgDrawStyle(visibleColor,notVisibleColor):
	#this gives you draw callbacks which draw the given color
	def drawCallback(x,y,visible,screen):
		if(visible):
			ltc.console_set_char_background(screen,x,y,visibleColor,ltc.BKGND_SET)
		else:
			ltc.console_set_char_background(screen,x,y,notVisibleColor,ltc.BKGND_SET)
	return drawCallback
	
def Wall():
	return Tile(True,bgDrawStyle(tileStyles.color_light_wall,tileStyles.color_dark_wall),block_sight=True,name="Wall")
	
def Floor():
	return Tile(False,bgDrawStyle(tileStyles.color_light_ground,tileStyles.color_dark_ground),block_sight=False,name="Floor")
	
def Door():
	def onActivateCB(tile, activator):
		tile.blocked=not tile.blocked
	def activatedDrawCB(x,y,visible,screen):
		if visible:
			ltc.console_set_char_background(screen, x, y, tileStyles.color_light_ground,ltc.BKGND_SET)
			ltc.console_set_default_foreground(screen ,tileStyles.color_light_wall)
		else:
			ltc.console_set_char_background(screen,x,y,tileStyles.color_dark_ground,ltc.BKGND_SET)
			ltc.console_set_default_foreground(screen ,tileStyles.color_dark_wall)
		ltc.console_put_char(screen, x, y, ltc.CHAR_CHECKBOX_UNSET, ltc.BKGND_NONE)
	def normalDrawCB(x,y,visible,screen):
		if visible:
			ltc.console_set_char_background(screen, x, y, tileStyles.color_light_ground,ltc.BKGND_SET)
			ltc.console_set_default_foreground(screen ,tileStyles.color_light_wall)
		else:
			ltc.console_set_char_background(screen,x,y,tileStyles.color_dark_ground,ltc.BKGND_SET)
			ltc.console_set_default_foreground(screen ,tileStyles.color_dark_wall)
		ltc.console_put_char(screen, x, y, ltc.CHAR_CROSS, ltc.BKGND_NONE)
	
	a=Activateable(onActivateCB,activatedDrawCB)
	
	return Tile(True,normalDrawCB,block_sight=False,name="Door", activateable=a)

def ComputerTerminal():
	def onActivateCB(tile, activator):
		tile.blocked=not tile.blocked
	def activatedDrawCB(x,y,visible,screen):
		if visible:
			ltc.console_set_char_background(screen, x, y, tileStyles.color_light_ground,ltc.BKGND_SET)
			ltc.console_set_default_foreground(screen ,tileStyles.color_light_wall)
		else:
			ltc.console_set_char_background(screen,x,y,tileStyles.color_dark_ground,ltc.BKGND_SET)
			ltc.console_set_default_foreground(screen ,tileStyles.color_dark_wall)
		ltc.console_put_char(screen, x, y, 167, ltc.BKGND_NONE)
	def normalDrawCB(x,y,visible,screen):
		if visible:
			ltc.console_set_char_background(screen, x, y, tileStyles.color_light_ground,ltc.BKGND_SET)
			ltc.console_set_default_foreground(screen ,tileStyles.color_light_wall)
		else:
			ltc.console_set_char_background(screen,x,y,tileStyles.color_dark_ground,ltc.BKGND_SET)
			ltc.console_set_default_foreground(screen ,tileStyles.color_dark_wall)
		ltc.console_put_char(screen, x, y, 167, ltc.BKGND_NONE)
	
	a=Activateable(onActivateCB,activatedDrawCB)
	
	return Tile(False,normalDrawCB,block_sight=False,name="Door", activateable=a)

def exitTo(map,x,y):
	def onActivateCB(tile,activator):
		activator.removeFromMap()
		map.addObject(activator,x,y)
	def normalDrawCB(x,y,visible,screen):
		if visible:
			ltc.console_set_char_background(screen, x, y, tileStyles.color_light_exit,ltc.BKGND_SET)
		else:
			ltc.console_set_char_background(screen,x,y,tileStyles.color_dark_exit,ltc.BKGND_SET)
	a=Activateable(onActivateCB,normalDrawCB)
	return Tile(True,normalDrawCB,block_sight=False, name="exit",activateable=a)
	
		

# map factory
def test_plaza():
	plaza=Map(101,101)
	for i in range(20):
		for j in range(20):
			plaza.setTile(i,j,Wall())
			plaza.setTile(plaza.width-i-1,j, Wall())
			plaza.setTile(i,plaza.height-j-1,Wall())
			plaza.setTile(plaza.width-i-1, plaza.height-j-1, Wall())
	for i in range(plaza.width):
		plaza.setTile(i,0,Wall())
		plaza.setTile(i,plaza.height-1,Wall())
	for i in range(plaza.height):
		plaza.setTile(0,i,Wall())
		plaza.setTile(plaza.width-1,i,Wall())
	
	for i in range(20):
		for j in range(20):
			plaza.setTile(i-plaza.width/2-10, j-plaza.height/4-10, Wall())
	
	return plaza
	
def test_shuttle():
	shuttle=Map(51,51)
	for i in range(shuttle.width):
		shuttle.setTile(i,0,Wall())
		shuttle.setTile(i,shuttle.height-1,Wall())
	for i in range(shuttle.height):
		shuttle.setTile(0,i,Wall())
		shuttle.setTile(shuttle.width-1,i,Wall())
	return shuttle

		
		
#test
#m=Map(20,20)
#m.tile(5,10).blocked=True
#m.bc=0
#x=10
#y=10
#pos=m.pathThrough(x,y,20,0)
#print(str(x))
#print(str(y))
#print(pos)