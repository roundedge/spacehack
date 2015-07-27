#combat
import math
import MyMath
import libtcodpy as ltc
import items
import object


#everything that is a combatant should be mortal, but not everything that is mortal is a combatant
class Mortal:
	#owner type: object
	def standardOnDeath(object):
		object.kill()
	
	def __init__(self, maxhp, onDeath=standardOnDeath):
		self.maxhp=maxhp
		self.hp=maxhp
		self.onDeath=onDeath
		
		self.damageResistance=Buffable({"default":0})
		self.damageReduction=Buffable({"default":0})
		
	def takeDamage(self, damage, sourceObject=None):
		#TODO: handle dodging
		amount=damage.amount
		
		reductions=self.damageReduction.get()
		reduction=reductions["default"]
		if damage.type in reductions.keys():
			reduction=reductions[damage.type]
			
		amount-=reduction
		
		resistances=self.damageResistance.get()
		resistance=resistances["default"]
		print(resistances)
		if damage.type in resistances.keys():
			resistance=resistances[damage.type]
		amount=amount*(1-resistance/100)
		
		if amount<0:
			amount=0
		self.hp = self.hp-amount
		if(self.hp<=0):
			self.die()
	
	def die(self):
		self.onDeath.__call__(self.owner)


class Damage:
	def __init__(self,amount,type):
		self.amount=amount
		self.type=type
		#self.source=source

#TODO: Buffs
#I want to describe a buffable object
#it takes some data, and makes each element of that data modifiable
#need a composition operator
#needs a base piece of data
class Buffable:
    def __init__(self, baseStat):
        self.baseStat=baseStat
        self.buffs=[]
        
    def __repr__(self):
        return str(self.get())
        
    def get(self):
        out=self.baseStat
        for buff in self.buffs:
            out=buff.apply(out)
        return out
        
    def buff(self, buff):
        self.buffs.append(buff)
        
    def debuff(self, buff):
        if(buff in self.buffs):
            self.buffs.remove(buff)
		
class damageResistanceBuff:
	def __init__(self, amount, types):
		self.amount=amount
		self.types=types
	
	def apply(self,stat):
		out=stat
		# #for each type in the base stat
		# for type in stat.keys():
			# #check if it is in the buff
			# if type in self.types.keys():
				# #if it is, check if it is true
				# if self.types[type]:
					# out[type]+=self.amount
					# if(out[type]>100):
						# out[type]=100
			# else:
				# #if it is not in the buff
				# if self.types["default"]:
					# #then only apply it if it is applied by default
					# out[type]+=self.amount
					# if(out[type]>100):
						# out[type]=100
						
		
		#it should work like this
		relevantTypes=self.types.keys()+stat.keys()
		for type in relevantTypes:
			#three cases
			if type in self.types.keys():
				if type in stat.keys():
					#its in the buff and in the base stat
					if self.types[type]:
						#if its true for this type
						out[type]+=self.amount
						if(out[type]>100):
							out[type]=100
				else:
					#its in the buff only
					if self.types[type]:
						out[type]=self.amount
						if(out[type]>100):
							out[type]=100
					else:
						out[type]=0
			elif type in stat.keys():
				#its in the base stat only
				if self.types["default"]:
					out[type]+=self.amount
					if(out[type]>100):
						out[type]=100	
		return out
	
class damageReductionBuff:
	def __init__(self,amount,types):
		self.amount=amount
		self.types=types
		
	def apply(self,stat):
		out=stat
		for type in stat.keys():
			#check if it is in the buff
			if type in self.types.keys():
				#if it is, check if it is true
				if self.types[type]:
					out[type]+=self.amount
			else:
				#if it is not in the buff
				if self.types["default"]:
					#then only apply it if it is applied by default
					out[type]+=self.amount
		return out

#TODO: Body Schema? Aliens have different body types, should this be taken into account? Maybe, but consider that for the purposes of gameplay it bogs things down quite a bit. 

	
class Combatant:
	#owner type: object	
	def __init__(self, hands=2, NaturalWeapon=None):
		self.hands=hands
		self.weilding=[]
		self.NaturalWeapon=NaturalWeapon
		self.NaturalWeapon.combatant=self
		
	def weild(self, obj):
		#if your hands are not full
		if len(self.weilding) >= self.hands:
			return False
		#and you aren't already weilding this
		if obj in self.weilding:
			return False
		#and it can be weilded
		if obj.weildable==None :
			return False
			
		self.weilding.append(obj)
		obj.weildable.onWeild(self.owner)
		
	def drop(self, obj):
		#if you are weilding the object
		if obj not in self.weilding:
			return False
		#and you live in a world
		if self.owner.map == None:
			return False
		
		self.weilding.remove(obj)
		self.obj.weildable.unWeild(self.owner)
		(x,y)=self.owner.position()
		self.owner.map.addObject(obj,x,y)
		return True
		
	def putAway(self, obj):
		#if you are weilding the object
		if obj not in self.weilding:
			return False
		#and you have an inventory
		if self.owner.inventory == None:
			return False
		#and the object is an item
		if obj.item==None:
			return False
		
		self.weilding.remove(obj)
		self.obj.weildable.unWeild(self.owner)
		self.owner.inventory.addItem(obj)
		
		return True
		
	def inRangeOf(self,target):
		for w in self.weilding:
			if w.weildable.inRange(target):
				return True
		if self.NaturalWeapon.inRange(target):
			return True
		return False
		
	def attack(self, target):
		#need to handle both ranged and melee attacks. I guess melee is simply an instance of ranged with range=1
		for w in self.weilding:
			print(w.name)
			w.weildable.onAttack(target)	
		freeHands=self.hands-len(self.weilding)
		for i in range(freeHands):
			self.NaturalWeapon.onAttack(target)

	
	
class NaturalWeapon:
	#owner type: combatant
	
	def __init__(self, attackRange=1, attackFunction=None):
		self.attackFunction=attackFunction
		self.attackRange=attackRange
		self.combatant=None
	
	def inRange(self, target):
		if self.combatant and self.combatant.owner and self.combatant.owner.map.hasObject(target):
			#kludgy stuff here
			(xi,yi)=self.combatant.owner.position()
			(xf,yf)=target.position()
			p1=MyMath.Point(xi,yi)
			p2=MyMath.Point(xf,yf)
			#we floor our distance so that immediate diagonals are 1 away. Hope that works.
			return math.floor(MyMath.distance(p1,p2))<=1
		else:
			return False
		
	def onAttack(self,target):
		if self.inRange(target):
			if(self.attackFunction != None):
				#the attack function handles hit probabilities etc.
				self.attackFunction.__call__(self,self.combatant.owner,target)
	
class Weildable:
	#owner type: object
	def __init__(self, attackRange=1, attackFunction=None, onWeildFunction=None, onUnWeildFunction=None, ignoreObstacles=False):
		self.onWeildFunction=onWeildFunction
		self.attackFunction=attackFunction
		self.onUnWeildFunction=onUnWeildFunction
		self.weildedBy=None
		self.attackRange=attackRange
		self.ignoreObstacles=ignoreObstacles
	
	def onWeild(self,weildedBy):
		self.weildedBy=weildedBy
		if(self.onWeildFunction != None):
			self.onWeildFunction.__call__(self,self.weildedBy)
		
	def unWeild(self):
		if(self.onUnWeildFunction != None):
			self.onUnWeildFunction.__call__(self,self.weildedBy)
		self.weildedBy=None
		
	def inRange(self, target):
		if self.weildedBy :
			(xi,yi)=self.weildedBy.position()
			(xf,yf)=target.position()
			p1=MyMath.Point(xi,yi)
			p2=MyMath.Point(xf,yf)
			#we floor our distance so that immediate diagonals are 1 away. Hope that works.
			return math.floor(MyMath.distance(p1,p2))<=self.attackRange
			
	#we have to consider line of sight as well, there are some weapons which might be range weapons, but there are also some that might require line of sight, ie projectile weapons vs ...magic weapons?
	
	def inSight(self, target):
		if(self.weildedBy):
			if(self.weildedBy.map):
				return self.weildedBy.map.inFieldOfView(self.weildedBy, target, self.attackRange)
		return False
					
					
		
	def onAttack(self,target):
		if(self.ignoreObstacles):
			if self.inRange(target):
				if(self.attackFunction != None):
					#the attack function handles hit probabilities etc.
					self.attackFunction.__call__(self,self.weildedBy,target)
		else:
			if self.inSight(target):
				if(self.attackFunction != None):
					self.attackFunction.__call__(self,self.weildedBy,target)
		

		
		
class Wearable:
	#owner type: object?
	def __init__(self, onWearFunction=None, onTakeOffFunction=None):
		self.onWearFunction=onWearFunction
		self.onTakeOffFunction=onTakeOffFunction
		self.wornBy=None
	
	def onWear(self,weildedBy):
		self.weildedBy=weildedBy
		if(self.onWeildFunction != None):
			self.onWeildFunction.__call__(self,self.wornBy)
		
	def onTakeOff(self):
		if(self.onTakeOffFunction != None):
			self.onTakeOffFunction.__call__(self,self.wornBy)
		self.weildedBy=None
			

#I need to think a bit about how combat works. Namely, how to organize succesfully dealing damage. 

#The simplest thing is that there should be a chance to hit, and then there should be armour which reduces the chance to hit. I figure this can be calculated in two seperate places? First, the attacker tries to hit, if they succeed, then the defender attempts to dodge/deflect




####---------- Instances -------------####

###----------- attack funtion callback generators -------------###
# attackFunction.__call__(weapon instance ,weilder ,target) #
def simpleDamage(damage):
	def attackFunction(weapon,weilder,target):
		if target.mortal:
			target.mortal.takeDamage(damage,weapon)
	return attackFunction
###----------- Natural Weapon Factories ----------###
def Fist(strength): return NaturalWeapon(attackFunction=simpleDamage(Damage(strength, "blunt")))
def Claw(strength): return NaturalWeapon(attackFunction=simpleDamage(Damage(strength, "cutting")))

###----------- Weilded Weapon Factories ----------###

def LaserGun(power, range):
	w=Weildable( attackRange=range, attackFunction=simpleDamage(Damage(power, "beam"))) 
	return object.Object('/',ltc.fuchsia, name="laser gun", description="a standard beam weapon",item=items.Item(),weildable=w)
	
### we can see here the makings of a markup language ###

##okay, here is my test, I want to make an orb that when weilded buffs you against all damage except for beam damage. It also has a charge, so after a certain amount of damage buffed it will stop working #### we dont have the infrastructure for this yet. still need a buff system

#let's try now
def StasisOrb():
	buff=damageResistanceBuff(100, {"default":True, "beam":False})
	def onWeild(weapon, weilder):
		if weilder.mortal:
			weilder.mortal.damageResistance.buff(buff)
			
	def onUnWeild(weapon,weilder):
		if weilder.mortal:
			weilder.mortal.damageResistance.debuff(buff)

	w=Weildable(onWeildFunction=onWeild, onUnWeildFunction=onUnWeild)
	
	return object.Object('/', ltc.blue, name="Stasis Orb", description="This sphere produces a shield which is impermeable to all but the most energetic weapons", item=items.Item(), weildable=w)