import libtcodpy as ltc
from party import Party
import object
import map
import species
import actor
import actions
import orders
import MyMath
import interface3
import rendering
import renderingPYG

class Game:
	#game loop finite state machine
	ANNOUNCEMENTS=0
	PLAYERS_TURN=1
	FINISHING_PLAYERS_TURN=2
	NPCS_TURN=3
	PASSIVE_ACTIONS=4
	
	stateMachine={}


	def __init__(self):

	
		#initialize input
		ltc.console_set_keyboard_repeat(500, 20)
		#ltc.console_set_keyboard_repeat(0, 0)
	
		#construct world
		self.PARTY=Party()
		#self.currentMap=map.test_plaza()#map.Map(60,60)
	
		self.interface=interface3.PartyInterface(self.PARTY,self)
	
		#main loop
		self.turn_ended=False
		self.waiting_for_input=False
		self.show_scheduled_actions=False
		self.state=Game.PLAYERS_TURN

	
	
	def handle_keys(self):
		mouse= ltc.Mouse()
		key = ltc.Key()
		ltc.sys_check_for_event(ltc.EVENT_KEY|ltc.EVENT_MOUSE,key,mouse)
		#ltc.sys_wait_for_event(ltc.EVENT_KEY_PRESS|ltc.EVENT_MOUSE,key,mouse,True)
		#ltc.sys_wait_for_event(ltc.EVENT_KEY|ltc.EVENT_MOUSE,key,mouse,True)
		if(key.vk is not 0):
			None
			#print(key.vk)
		if(key.c is not 0):
			None
			#print(key.c)
		exitKey=self.interface.onKeyEvent(key)
		exitMouse=self.interface.onMouseEvent(mouse)
		
		#ltc.sys_wait_for_event(ltc.EVENT_KEY_RELEASE, key,mouse,True)
		
	
		#f key.vk == ltc.KEY_ESCAPE:
		#	return True #exit game
		if(exitKey or exitMouse):
			return True
	
	def renew_action_points(self):
		currentMaps=self.PARTY.getCurrentMaps()
		for map in currentMaps:
			objects=map.actors()
			for c in objects:
				c.actor.renew_action_points()

	
	def makeAnnouncements(self):
		#print("make announcement")
		#make announcement
		#if its the last announcement to have been made
		self.state=self.PLAYERS_TURN
		self.PARTY.turn_ended=False
		#print("players turn")
		#renew all action points
		self.renew_action_points()
		#after interrupt messages, focus on your primary party member (leader)
		self.PARTY.setFocus(0)
	
	def doPlayersTurn(self):
		#wait for input from player
		print("check for input")
		exit=self.handle_keys()

		turnBased=1
		realtime=2
		gameStyle=realtime

		if gameStyle is turnBased:
			#once the leader performs their action the players turn is over, 
			if(self.PARTY.getMember(0).actor.ap==0):
				#all those party members which have not yet performed actions will perform their scheduled passive actions until they have run out of action points.
				if(self.show_scheduled_actions==False):
					for i in range(self.PARTY.size()):
						#go through the party members until you find one with action points
						while(self.PARTY.getMember(i).actor.ap!=0):
							#TODO: spend all their action points
							#PARTY.getMember(i).takeScheduledAction()
							self.PARTY.getMember(i).actor.takeOrder()
							self.PARTY.getMember(i).actor.ap=0
							#TODO: figure out how you want to make sure that taking an order which spends zero action points doesn't cause an infinite loop, the above fix is a kludge (SEE ALSO, DO NPCS TURN)
							pass
					self.state=self.NPCS_TURN
				else:
					self.state=self.FINISHING_PLAYERS_TURN
					#print('finishing players turn')
			return exit

		if gameStyle is realtime:
			for i in range(self.PARTY.size()):
				#go through the party members until you find one with action points
				while(self.PARTY.getMember(i).actor.ap!=0):
					#TODO: spend all their action points
					self.PARTY.getMember(i).actor.takeOrder()
					self.PARTY.getMember(i).actor.ap=0
					#TODO: figure out how you want to make sure that taking an order which spends zero action points doesn't cause an infinite loop, the above fix is a kludge (SEE ALSO, DO NPCS TURN)
					pass
				self.state=self.NPCS_TURN
			return exit

	
	def finishPlayersTurn(self):
		#all those party members which have not yet performed actions will perform their scheduled passive actions until they have run out of action points.
		foundActiveMember=False
		#if we are showing schedules actions actions
		for i in range(self.PARTY.size()):
			#go through the party members until you find one with action points
			if(self.PARTY.getMember(i).actor.ap!=0):
				foundActiveMember=True
				#let the player
				#if we aren't focusing on this party member, set the focus and let rendering occur
				if(self.PARTY.getFocus()!=self.PARTY.getMember(i)):
					self.PARTY.setFocus(i)
					break
				else:
					#ltc.sys_sleep_milli(2)
					self.PARTY.getMember(i).actor.takeScheduledAction()
					break
		if(foundActiveMember!=True):
			self.state=self.NPCS_TURN
			
	def doNPCsTurn(self):
		#ltc.sys_sleep_milli(2)
		#print("NPC turns")
		#handle AI actions
		currentMaps=self.PARTY.getCurrentMaps()
		npcs=[]
		for m in currentMaps:
			npcs=npcs+m.npcs(self.PARTY)
		for npc in npcs:
			while npc.actor.ap!=0:
				npc.actor.takeOrder()
				npc.actor.ap=0
				#TODO: figure out how you want to make sure that taking an order which spends zero action points doesn't cause an infinite loop, the above fix is a kludge
		self.state=self.PASSIVE_ACTIONS
	
	def doPassiveActions(self):
		#TODO
		#print("passive actions")
		self.state=self.ANNOUNCEMENTS
	
	def render(self):
		#TODO
	
	stateMachine={ANNOUNCEMENTS:makeAnnouncements,
	PLAYERS_TURN:doPlayersTurn,
	FINISHING_PLAYERS_TURN:finishPlayersTurn,
	NPCS_TURN:doNPCsTurn,
	PASSIVE_ACTIONS:doPassiveActions}
	
	def loop(self):
		#Render Scene
		if self.state==self.PLAYERS_TURN: self.render()
		return self.stateMachine[self.state](self)

#the game structure is kind of tricky, what I want to do is have the rendering engine be a bit more agnostic so that I can call it without having the structure of the game known, but I want to delegate the specific details of rendering out of the game class and into a seperate mediating agent,

class Rendering_Agent:
	
	def __init__(self):
		self.currentMap=None
		self.mapChanged=False

	def setMap(self,map):
		if self.currentMap!=map:
			self.mapChanged=True
			self.currentMap=map
		else:
			self.mapChanged=False

	def render(self):
		#check if the last map rendered has changed
		if self.mapChanged:
			#TODO
		#if so, construct new tile changes

		#get the tile changes
		self.
		#clear the tile changes

		#get the objects

		#draw the scene
		self.screen.