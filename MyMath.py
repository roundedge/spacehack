#math
import math
from collections import Sequence

class Vec(Sequence):
	def __init__(self,x=(0,0),y=None):
		if(y is None):
			self.x=x[0]
			self.y=x[1]
		else:
			self.x=x
			self.y=y

		
	def __getitem__(self,i):
		if i==0:
			return self.x
		elif i==1:
			return self.y
		else:
			temp=[]
			return temp[i]

	def __len__(self):
		return 2

	def __add__(self,c):
		return Vec(self.x+c.x, self.y+c.y)


	def __mul__(self,c):
		if isinstance(c,Vec):
			return self.x*c.x+self.y*c.y
		else:
			return Vec(self.x*c,self.y*c)

	def __sub__(self,c):
		return Vec(self.x-c.x,self.y-c.y)
		
	__rmul__=__mul__

	def __div__(self,c):
		return Vec(self.x/c,self.y/c)

	def __neg__(self):
		return Vec(-self.x,-self.y)

	def __abs__(self):
		return math.sqrt(self*self)

	def __str__(self):
		return '('+str(self.x)+','+str(self.y)+')'

	def tuple(self):
		return (self.x,self.y)
		
a=Vec(0,1)
b=Vec(1,1)
c=a+b
c=a-2*b
print(c.x)
print(c.y)
print((3*c).x)
print(abs(a))
print((c/2).x)

class Rect:
	
	def __init__(self, x,y,width,height):
		self.x=x
		self.y=y
		self.width=width
		self.height=height

	def topLeft(self):
		return Vec(self.x,self.y)
	
	def bottomRight(self):
		return Vec(self.x+self.width,self.y+self.height)
	
	def contains(self,x,y):
		return (x>=self.x and y>=self.y and x<=(self.x+self.width) and y<=(self.y+self.height))


def distance(p1,p2):
	return p1.minus(p2).length()