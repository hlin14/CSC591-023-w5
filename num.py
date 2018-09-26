from testEngine import O
from sample import sample

class num:
	def __init__(self, maxNumber = 1):
		self.n = 0
		self.mu = 0
		self.m2 = 0
		self.lo = 10 ^ 32
		self.hi = -10 ^ 32
		self.sd = 0
		self.same = sample(maxNumber)

	def nums(self, listNumbers):
		n = num(len(listNumbers))
		for x in listNumbers:
			n.numInc(x)			
		return n

	def numInc(self, x):
		if x is None:
			return x
		self.n += 1
		self.same.sampleInc(x)
		d = x - self.mu
		self.mu = self.mu + d / self.n
		self.m2 = self.m2 + d * (x - self.mu)
		if x > self.hi: self.hi = x
		if x < self.lo: self.lo = x
		if self.n >= 2:
			self.sd = (self.m2 / (self.n - 1 + 10 ** -32)) ** 0.5
		return x

	def numDec(self, x):
		if x is None:
			return x
		if self.n == 1:
			return x
		self.n -= 1
		self.mu = self.mu - d / self.n
		self.m2 = self.m2 - d * (x - self.mu)
		if self.n >= 2:
			self.sd = (self.m2 / (self.n - 1 + 10 ** -32)) ** 0.5
		return x

	def numNorm(self, x):
		return 0.5 if x == '?' else (x - self.lo) / (self.hi - self.lo + 10 ** -32)

	def numXpect(i, j):
		n = i.n + j.n + 0.0001
		return i.n / n * i.sd + j.n / n + j.sd
@O.k
def testing():
	num_list = [4,10,15,38,54,57,62,83,100,100,174,190,215,225,233,250,
		260,270,299,300,306,333,350,375,443,475,525,583,780,1000]
	n = num()
	n = n.nums(num_list)
	assert n.mu == 270.3 and round(n.sd, 3) == 231.946 
	
if __name__== "__main__":
  O.report()
