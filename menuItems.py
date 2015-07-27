#menu pieces
import libtcodpy as ltc
import MyMath

class SelectionMenu(ConsoleBuffer):
	
	def __init__(self,width,height,x, y,title,selection,names):
		#selection must be a delayed function
		ltc.ConsoleBuffer.__init__(width,height)
		self.title=title
		self.selection=selection
		self.names=names
		self.rect=MyMath.Rect(x,y,width,height)
	
	def draw(self):
		ltc.console_print(self,0,0, self.title)
		ltc.console_print(self,0,1,"------------")
		for i in range(length(names)):
			ltc.console_print(self,0,i+2,names[i])
		
		ltc.console_blit(self,self.rect.x,self.rect.y,self.rect.width,self.rect.height,0,0,0)
	
	def contains(self,x,y):
		return self.rect.contains(x,y)
	
	def onClick(self,x,y):
		if(self.contains(x,y)):
			i=y-self.y-2
			if(selection[i] is not None):
				selection[i].call()
	