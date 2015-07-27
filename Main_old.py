#based on this tutorial http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod,_part_1

import libtcodpy as ltc
from party import Party
import object
import map
import species
import creature
import actions
import orders
import MyMath
import interface

SCREEN_WIDTH=80
SCREEN_HEIGHT=50
LIMIT_FPS=20

ltc.console_set_custom_font('arial10x10.png', ltc.FONT_TYPE_GREYSCALE | ltc.FONT_LAYOUT_TCOD)

#initialize the screens
ltc.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'spacehack', False)
ltc.sys_set_fps(LIMIT_FPS)
con=ltc.console_new(SCREEN_WIDTH,SCREEN_HEIGHT)

currentMap=map.Map(800,600)
currentMap.tile(30,22).blocked=True
currentMap.tile(30,22).block_sight=True
currentMap.tile(50,22).blocked=True
currentMap.tile(50,22).block_sight=True
currentMap.initializeFOV()

ActionMenu=None

#game objects
player1=creature.Creature(species.HUMAN, 'Joel')
player2=creature.Creature(species.HUMAN, 'Marty')
player3=creature.Creature(species.HUMAN, 'Doc')
currentMap.addObject(player1, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
currentMap.addObject(player2, SCREEN_WIDTH/2+5, SCREEN_HEIGHT/2+3)
currentMap.addObject(player3, SCREEN_WIDTH/2+5, SCREEN_HEIGHT/2+4)

npc=object.Object( '@', ltc.yellow)
currentMap.addObject(npc, SCREEN_WIDTH/2-5, SCREEN_HEIGHT/2)

objects=[npc,player1, player2, player3]
creatures=[player1, player2, player3]


PARTY=Party()
PARTY.addMember(player1)
PARTY.addMember(player2)
PARTY.addMember(player3)
player2.giveOrder(orders.followOrder(currentMap, player1))
player3.giveOrder(orders.followOrder(currentMap, player2))

#initialize input
ltc.console_set_keyboard_repeat(500, 20)

#input handler

def handle_keys():
	inter=interface.PartyInterface(PARTY,currentMap)
	
	mouse= ltc.Mouse()
	key = ltc.Key()
	ltc.sys_check_for_event(ltc.EVENT_KEY_PRESS|ltc.EVENT_MOUSE,key,mouse)
	inter.onKeyEvent(key)
	inter.onMouseEvent(mouse)
	
	if key.vk == ltc.KEY_ESCAPE:
		return True #exit game
	

def old_handle_keys():
	global playerx, playery,fov_recompute, player
	
	mouse= ltc.Mouse()
	key = ltc.Key()
	
	#ltc.sys_wait_for_event(ltc.EVENT_KEY_PRESS|ltc.EVENT_MOUSE,key,mouse,True)
	
	#key = ltc.console_wait_for_keypress(True)
	ltc.sys_check_for_event(ltc.EVENT_KEY_PRESS|ltc.EVENT_MOUSE,key,mouse)
	print("key pressed: "+str(key.vk))
	if(mouse.rbutton):
		#create an action menu
		print(str(mouse.cx)+" "+str(mouse.cy))
		tilex=mouse.cx+mapTopLeftX()
		tiley=mouse.cy+mapTopLeftY()
		print(str(tilex)+" "+str(tiley))
		#get the info you need
		creatures=currentMap.creatures(tilex,tiley)
		#put up a menu item
		i=0
		for c in creatures:
			ltc.console_print(con,tilex,tiley+i,c.title())
			i=i+1
		#ActionMenu=menuItems.SelectionMenu()
	
	if(key.vk==25):
		PARTY.setFocus(0)
		currentMap.fov_recompute=True
	elif(key.vk==26):
		PARTY.setFocus(1)
		currentMap.fov_recompute=True
	elif(key.vk==27):
		PARTY.setFocus(2)
		currentMap.fov_recompute=True
	elif(key.vk==28):
		PARTY.setFocus(3)
		currentMap.fov_recompute=True

	dx=0
	dy=0
	
	if (key.vk==ltc.KEY_UP):
		dy-=1
		currentMap.fov_recompute=True
	elif (key.vk==ltc.KEY_DOWN):
		dy+=1
		currentMap.fov_recompute=True
	elif (key.vk==ltc.KEY_LEFT):
		dx-=1
		currentMap.fov_recompute=True
	elif (key.vk==ltc.KEY_RIGHT):
		dx+=1
		currentMap.fov_recompute=True
	
	#PARTY.getFocus().move(currentMap,dx,dy)
	#currentMap.moveObject(PARTY.getFocus(),dx,dy)
	if(dx is not 0 or dy is not 0):
		actions.MoveAction(PARTY.getFocus(),currentMap,dx,dy).act()
	
	if key.vk == ltc.KEY_ENTER and key.lalt:
		#alt +enter: toggler fullscreen
		ltc.console_set_fullscreen(not ltc.console_is_fullscreen())
	elif key.vk == ltc.KEY_ESCAPE:
		return True #exit game
	
			
#rendering
def mapTopLeftX():return currentMap.positionOf(PARTY.getFocus())[0]-SCREEN_WIDTH/2

def mapTopLeftY():return currentMap.positionOf(PARTY.getFocus())[1]-SCREEN_HEIGHT/2

def render_all():
	mapWindow=MyMath.Rect(mapTopLeftX(),mapTopLeftY(),SCREEN_WIDTH,SCREEN_HEIGHT)
	ltc.console_clear(con)
	currentMap.draw(PARTY,con, mapWindow)
	
	ltc.console_blit(con,mapTopLeftX(),mapTopLeftY(),SCREEN_WIDTH,SCREEN_HEIGHT,0,0,0)
	PARTY.draw_menu(con)
	
	if(ActionMenu is not None):
		ActionMenu.draw()
	
	#for o in objects:
		#o.clear(currentMap.x(o),currentMap.y(o),con)

	ltc.console_flush()

#main loop
turn_ended=False
waiting_for_input=False

#we've got a finite state machine here
ANNOUNCEMENTS=0
PLAYERS_TURN=1
FINISHING_PLAYERS_TURN=2
NPCS_TURN=3


show_scheduled_actions=False

state=1

def renew_action_points():
	global creatures
	for c in creatures:
		c.renew_action_points()

while not ltc.console_is_window_closed():
	
	#Render Scene
	render_all()
	
	if(state==ANNOUNCEMENTS):
		print("make announcement")
		#make announcement
		#if its the last announcement to have been made
		state=PLAYERS_TURN
		PARTY.turn_ended=False
		print("players turn")
		#renew all action points
		renew_action_points()
		#after interrupt messages, focus on your primary party member (leader)
		PARTY.setFocus(0)
	elif(state==PLAYERS_TURN):
		#wait for input from player
		exit=handle_keys()
		#once the leader performs their action the players turn is over, 
		if(PARTY.getMember(0).ap==0):
			#all those party members which have not yet performed actions will perform their scheduled passive actions until they have run out of action points.
			if(show_scheduled_actions==False):
				for i in range(PARTY.size()):
					#go through the party members until you find one with action points
					while(PARTY.getMember(i).ap!=0):
						#TODO: spend all their action points
						#PARTY.getMember(i).takeScheduledAction()
						PARTY.getMember(i).takeOrder()
						PARTY.getMember(i).ap=0
						#TODO: figure out how you want to make sure that taking an order which spends zero action points doesn't cause an infinite loop, the above fix is a kludge
						pass
				state=NPCS_TURN
			else:
				state=FINISHING_PLAYERS_TURN
				print('finishing players turn')
		if exit:
			break
	elif(state==FINISHING_PLAYERS_TURN):
		#all those party members which have not yet performed actions will perform their scheduled passive actions until they have run out of action points.
		foundActiveMember=False
		#if we are showing schedules actions actions
		for i in range(PARTY.size()):
			#go through the party members until you find one with action points
			if(PARTY.getMember(i).ap!=0):
				foundActiveMember=True
				#let the player
				#if we aren't focusing on this party member, set the focus and let rendering occur
				if(PARTY.getFocus()!=PARTY.getMember(i)):
					PARTY.setFocus(i)
					break
				else:
					#ltc.sys_sleep_milli(2)
					PARTY.getMember(i).takeScheduledAction()
					break
		if(foundActiveMember!=True):
			state=NPCS_TURN
	elif(state==NPCS_TURN):
		#ltc.sys_sleep_milli(2)
		print("NPC turns")
		#handle AI actions
		state=ANNOUNCEMENTS
		
		
