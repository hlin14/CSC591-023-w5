from testEngine import O
import math

class sym:
	def __init__(self):
		self.counts = {}
		self.mode = None
		self.most = 0
		self.n = 0
		self.ent = None

	def syms(self, list_char):
		s = sym()
		for c in list_char:
			#print(self.counts)
			s.symInc(c)
		return s

	def symInc(self, c):
		if c is None:
			return c
		self.ent = None
		self.n += 1
		old = self.counts.get(c, 0)
		new = old and old + 1 or 1#??
		self.counts[c] = new
		#print(self.counts[c], new)
		#print(self.counts)
		if new > self.most:
			self.most, self.mode = new, c
		return self

	def symDec(self, c):
		self.ent = None
		if self.n > 0:
			self.n -= 1
			self.counts[x] = self.counts[x] -1
		return c


	def symEnt(self):
		#print(self.counts)
		if not self.ent:
			self.ent = 0
		for c, val in self.counts.items():
			p = val / self.n
			self.ent = self.ent - p * math.log(p, 2)
		return self.ent


@O.k
def testing():
	s = sym() 
	s = s.syms(['y','y','y','y','y','y','y','y','y','n','n','n','n','n'])
	assert round(s.symEnt(), 4)== 0.9403 

if __name__== "__main__":
  O.report()

