import libtcodpy as ltc
import actor


class Party:
	MENU_WIDTH=20
	MENU_HEIGHT=20
	MAX_MEMBERS=4
	focus=0
	turn_ended=False
	
	
	def __init__(self):
		self.menu=ltc.console_new(self.MENU_WIDTH,self.MENU_HEIGHT)
		#ltc.console_set_background_color(self.menu, ltc.red)
		self.members=[]
		
	
	def setFocus(self, number):
		if(len(self.members)==0):
			return
		if(number>=len(self.members)):
			number=len(self.members)-1
		if(number<0):
			number=0
		self.focus=number
	
	def getFocus(self):
		return self.getMember(self.focus)
	
	def hasMember(self, obj):
		return obj in self.members
	
	def getMember(self, number):
		if(len(self.members)==0):
			return None
		if(number>=len(self.members)):
			number=len(self.members)-1
		if(number<0):
			number=0
		return self.members[number]
	
	def getCurrentMaps(self):
		maps=[]
		for member in self.members:
			if(member.map and member.map not in maps):
				maps.append(member.map)
		return maps
	
	def inBounds(self, number):
		if(number>=len(self.members)):
			return False
		if(number<0):
			return False
		return True
	
	def addMember(self, obj):
		if(obj.actor is None):
			return False
		if(len(self.members)==self.MAX_MEMBERS):
			return False
		else:
			self.members.append(obj)
			obj.actor.party=self
			obj.NPC=False
			return True
	
	def removeMember(self, obj):
		if self.hasMember(obj): 
			self.members.remove(obj)
			obj.actor.party=None
			obj.actor.NPC=True
	
	def size(self):
		return len(self.members)
	
	def swapPositions(self, pos1, pos2):
		if(len(self.members)==0):
			return
		if(pos1>=len(self.members)):
			pos1=len(self.members)-1
		if(pos1<0):
			pos1=0
		if(pos2>=len(self.members)):
			pos2=len(self.members)-1
		if(pos2<0):
			pos2=0
		member1=self.members[pos1]
		member2=self.members[pos2]
		self.members[pos1]=member2
		self.members[pos2]=member1
	
	def draw_menu(self, screen):
		verticalSpacing=4
		menu=self.menu
		ltc.console_clear(menu)
		ltc.console_print(menu,0,0,"Party Member")
		ltc.console_print(menu,self.MENU_WIDTH-4, 0, 'APs')
		ltc.console_print(menu,0,1,"--------------------")
		for i in range(len(self.members)):
			ltc.console_print(menu,1,3+verticalSpacing*i,str(i+1))
			ltc.console_print(menu,3,3+verticalSpacing*i,self.getMember(i).getName())
			ltc.console_print(menu,self.MENU_WIDTH-2, 3+verticalSpacing*i, str(self.getMember(i).actor.ap))
			if(self.getMember(i).mortal):
				ltc.console_print(menu,1, 3+verticalSpacing*i+2, "Health: ("+str(self.getMember(i).mortal.hp)+")")
			#1 Joel (1)
			ltc.console_print(menu, 1, 3+verticalSpacing*i+1, self.getMember(i).actor.order.title())
			# following Marty

		ltc.console_print(menu,0,3+verticalSpacing*self.focus,'>')
		
		ltc.console_blit(menu,-ltc.console_get_width(screen)+self.MENU_WIDTH,0,self.MENU_WIDTH+ltc.console_get_width(screen),self.MENU_HEIGHT,0,0,0)

