#math
import math

class Point:
	def __init__(self,x,y):
		self.x=x
		self.y=y
		
	def length(self):
		x=self.x
		y=self.y
		return math.sqrt(x*x+y*y)
		
	def plus(self,p2):
		return Point(self.x+p2.x, self.y+p2.y)
		
	def minus(self,p2):
		return Point(self.x-p2.x, self.y-p2.y)
		
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
	
	def contains(self,x,y):
		return (x>=self.x and y>=self.y and x<=(self.x+self.width) and y<=(self.y+self.height))


def distance(p1,p2):
	return p1.minus(p2).length()