import libtcodpy as ltc
import actor
import items
import object
import combat

class Struct:
    def __init__(self, **entries): self.__dict__.update(entries)
    def __eq__(self, other): return self.__dict__ == other.__dict__
    def __neq__(self, other): return self.__dict__ != other.__dict__

#null defines parameters for species that have none
NULL=Struct(name="null",size=.25,strength=.25,intelligence=.25,breathes="none",canFly=False, eats="none", enjoys={}, description='A creature not worth describing', char = '?', color=ltc.fuchsia)

class Species:
	def __init__(self, **entries):
		self.__dict__=NULL.__dict__.copy()
		self.__dict__.update(entries)
	def __eq__(self, other): return self.__dict__ == other.__dict__
	def __neq__(self, other): return self.__dict__ != other.__dict__
	

HUMAN = Species(name='Human', size=1,strength=1, intelligence=1, breathes="oxygen", canFly=False, eats="organics", enjoys={'socializing','games','beauty'}, description='A bipedal creature, approximately 5 feet tall.', char='@', color=ltc.light_amber)

ANDROID = Species(name='Android',size=1, strength=5, intelligence=2,enjoys={'cleaning', 'calculating'}, description='A humanoid robot.', char='@', color=ltc.lighter_sea)

def creature_Factory(species):
	c=combat.Combatant(NaturalWeapon=combat.Fist(species.strength))
	m=combat.Mortal(10*species.size+species.strength)
	return object.Object(species.char,species.color,description=species.description,actor=actor.Actor(),inventory=items.Inventory(), mortal=m, combatant=c)