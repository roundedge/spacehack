#utilities

class Delayed:
	#wrapper which provides a delayed function call
	def __init__(self, function,*args):
		self.function=function
		self.args=args
	
	def call(self, *args):
		allArgs=self.args+args
		self.function(*allArgs)
		
class delay:
	#possible alternative
    def __init__(self,f, *args):
        self.f=f
        self.args=args
   
    def __call__(self, *more):
        a=self.args+more
        return self.f(*a)
	
class ChainedDelay:
	def __init__(self, *delayed):
		self.delayed=delayed
		print("chained delay created")
	
	def call(self, *args):
		print("chained delay called")
		for d in self.delayed:
			d.call();

def trueForAll(list,eval):
	#tells wether every element of a list evaluates to true
	check=True
	for e in list:
		check=eval(e) and check
	return check

def collapse(list):
 return [item for sublist in list for item in sublist]


import new

class Compose(object):
    def __init__(self, *parts):
        self.parts = parts
    def __call__(self, cls):
        conflicts = dict()
        parts = self.parts + (cls,)
        for i, part1 in enumerate(parts):
            for partn in parts[i+1:]:
                for attr in dir(part1):
                    if attr[:2] == attr[-2:] == '__':
                        continue
                    if getattr(partn, attr, None):
                        if attr not in conflicts:
                            conflicts[attr] = [part1]
                        conflicts[attr].append(partn)
        if conflicts:
            text = []
            for key, lst in conflicts.items():
                text.append('    %s:' % key)
                for c in lst:
                    text.append('        %s' % c)
            text = '\n'.join(text)
            raise TypeError("Conflicts while composing:\n%s" % text)
        for part in self.parts:
            for attr in dir(part):
                if attr[:2] == attr[-2:] == '__':
                    continue
                thing = getattr(part, attr)
                thing = getattr(thing, '__func__', None) or thing
                if callable(thing):
                    setattr(cls, attr, new.instancemethod(thing, None, cls))
                else:
                    setattr(cls, attr, thing)
        return cls

		
class a:
	def test1(self):
		print "a"
		
class b:
	def test2(self):
		print "b"
