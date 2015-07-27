#math

class Point:
	def __init__(self,x,y):
		self.x=x
		self.y=y

class Rect:
	
	def __init__(self, x,y,width,height):
		self.x=x
		self.y=y
		self.width=width
		self.height=height

	def topLeft(self):
		return Point(self.x,self.y)
	
	def bottomRight(self):
		return Point(self.x+self.width,self.y+self.height)
	