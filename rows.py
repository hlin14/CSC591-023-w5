from num import num
from sym import sym
import re
import random
from testEngine import O

class data:
	def __init__(self):
		self.w = {}
		self.syms = {}
		self.nums = {}
		self._class = None
		self.rows = {}
		self.name = {}
		self._use = {}
		self.indeps = []

	#???
	#def indep(self, c): return not self.w[c] and self._class is not c
	#def dep(self, c): return not self.indep(c) 

	def header(self, cells):#cells just one row
		for idx, x in enumerate(cells):
			#print(idx, x)
			if not re.match('\?', x):
				c = len(self._use) + 1
				self._use[c] = idx
				self.name[c] = x
				if re.match('[<>$]', x):
					self.nums[c] = num()
				else:
					self.syms[c] = sym()
				if re.match('<', x):
					self.w[c] = -1
				elif re.match('>', x):
					self.w[c] = 1
				elif re.match('!', x):
					self._class = c
				else:
					self.indeps.append(c)

	#add a row
	def row(self, cells):
		r = len(self.rows) + 1
		self.rows[r] = {}
		for c, col in self._use.items():#col will collect the col that is in used
			x = cells[col]  #get the col obj in the cell
			if x != '?':
				if self.nums.get(c, '') != '':
					x = float(x)
					self.nums[c].numInc(x)
				else:
					self.syms[c].symInc(x)
			self.rows[r][c] = x
		#print(self.rows[r])


	def rows1(self,fname):
		with open(fname) as stream:
			first = True
			lines = stream.readlines()
			for line in lines:
				re.sub("[\t\r]*","",line)
				re.sub("#.*","",line)
				cells = line.split(',')
				for i in range(len(cells)):
					cells[i] = cells[i].strip()
				if len(cells) > 0:
					if first:
						#print(cells)
						self.header(cells)
					else:
						#print(cells)
						self.row(cells)
				first = False
				#print(line)
		return self

	def doms(self, obj):
		#print(obj.name)
		n = 100 #(should sample?)
		c = len(obj.name) + 1
		result = []
		print(" ".join(list(obj.name.values())) + "    >dom")
		#print(len(obj.rows))
		#print(obj.rows)
		for r1 in range(1, len(obj.rows) + 1):
			#print(obj.rows[r1])
			row1 = obj.rows[r1]
			obj.rows[r1][c] = 0
			for s in range(1, n + 1):
				row2 = self.another(r1, obj.rows)#to implement
				s = 1 / n if self.dom(obj, row1, row2) else 0
				obj.rows[r1][c] = round(obj.rows[r1][c] + s, 2)
			#print(list(obj.rows[r1].values()))
			result.append(list(obj.rows[r1].values()))
		return result

	def another(self, r1, rows):
		r2 = r1
		while r1 == r2:
			r2 = random.randrange(1, len(rows) + 1)
		return rows[r2]

	def dom(self, obj, row1, row2):
		s1 = 0
		s2 = 0
		n = 0
		for _ in range(len(obj.w)): #count how many w in obj
			n += 1
		for col, w in obj.w.items():#for every weighted col
			a0 = row1[col]#get weighted number from the row
			b0 = row2[col]
			a = obj.nums[col].numNorm(a0) #do the normalization
			b = obj.nums[col]. numNorm(b0)
			s1 = s1 - 10 ** (w * (a - b) / n) #cumulate the score
			s2 = s2 - 10 ** (w * (b - a) / n)
		return s1 / n < s2 / n  #return 1 if row1 dominate


	def readRows(self, fname):
		return self.rows1(fname)

	def showDom(self, fname):
		return self.doms(self.readRows(fname))

@O.k
def testing():
	n2 = data()
	result2 = n2.showDom("weatherLong.csv")

	result2.sort(key=lambda x: x[5])

	for item in result2:
		print(item)

	#check the row with the biggest dom is the smallest humid
	assert result2[-1][2] == 65.0


	n3 = data()
	result3 = n3.showDom("auto.csv")

	result3.sort(key=lambda x: x[8])


	aveWeigh1 = 0
	aveWeigh2 = 0

	aveAcce1 = 0
	aveAcce2 = 0

	aveMpg1 = 0
	aveMpg2= 0

	for item in result3[:10]:
		aveWeigh1 += item[3]
		aveAcce1 += item[4]
		aveMpg1 += item[7]
		print(item)

	aveWeigh1 /= 10
	aveAcce1 /= 10
	aveMpg1 /= 10

	for item in result3[-10:]:
		aveWeigh2 += item[3]
		aveAcce2 += item[4]
		aveMpg2 += item[7]
		print(item)

	aveWeigh2 /= 10
	aveAcce2 /= 10
	aveMpg2 /= 10
	
	assert aveWeigh1 > aveWeigh2 and aveAcce1 < aveAcce2 and aveMpg1 < aveMpg2


if __name__== "__main__":
  O.report()

