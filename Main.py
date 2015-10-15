#based on this tutorial http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod,_part_1

import libtcodpy as ltc
from party import Party
import object
import map
import species
import actions
import orders
import MyMath
import interface
import game
import items
import combat

spacehack=game.Game()
shuttle=map.test_shuttle()
plaza=map.test_plaza()
currentMap=shuttle

shuttle.setTile(1,1, map.exitTo(plaza,plaza.width/2,plaza.height/2))


#load test bed
#game objects
player1=species.creature_Factory(species.HUMAN)
player1.setName("Joel")
player2=species.creature_Factory(species.HUMAN)
player2.setName("Doc")
player3=species.creature_Factory(species.HUMAN)
player3.setName("Marty")
currentMap.addObject(player1, currentMap.width/2, currentMap.height/2)
currentMap.addObject(player2, currentMap.width/2+5, currentMap.height/2+3)
currentMap.addObject(player3, currentMap.width/2+5, currentMap.height/2+4)

spacehack.PARTY.addMember(player1)
spacehack.PARTY.addMember(player2)
spacehack.PARTY.addMember(player3)

player2.actor.giveOrder(orders.followOrder(currentMap, player1))
player3.actor.giveOrder(orders.followOrder(currentMap, player2))

currentMap.setTile(30,22,map.Wall())
currentMap.setTile(50,22,map.Wall())
currentMap.setTile(50,21,map.Door())
currentMap.tile(50,21).activateable.activate(None)

for i in range(14):
	keycard=object.Object(',', ltc.lighter_sea, name="keycard", item=items.Item(stackable=items.Stackable(4)))
	currentMap.addObject(keycard,spacehack.SCREEN_WIDTH/2, spacehack.SCREEN_HEIGHT/2)
	
gun=combat.LaserGun(4, 6)
player1.combatant.weild(gun)

orb=combat.StasisOrb()
player2.combatant.weild(orb)

########################

while not ltc.console_is_window_closed():
	exit=spacehack.loop()
	if exit:
			break