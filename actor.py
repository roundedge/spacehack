import libtcodpy as ltc
import object
import orders


class Actor():
	
	def __init__(self):
		self.ap=1
		self.order=orders.noOrder()
		self.NPC=True
		self.party=None
		
	def renew_action_points(self):
		self.ap=1
		
	def giveOrder(self, order):
		self.order=order
	
	def takeOrder(self):
		if(self.order is not None):
			self.order.resolve(self.owner)
			return True
		else:
			return False
			
