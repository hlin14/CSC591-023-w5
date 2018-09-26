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
		print("   ".join(list(obj.name.values())) + "    >dom")
		#print(len(obj.rows))
		#print(obj.rows)
		for r1 in range(1, len(obj.rows) + 1):
			#print(obj.rows[r1])
			row1 = obj.rows[r1]
			obj.rows[r1][c] = 0
			for s in range(1, n + 1):
				row2 = self.another(r1, obj.rows)#to implement
				s = 1 / n if self.dom(obj, row1, row2) else 0
				obj.rows[r1][c] = obj.rows[r1][c] + s
			print(obj.rows[r1])
		return

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
	#n2.showDom("weatherLong.csv")
	n2.showDom("weatherLong.csv")
	
	#print(n2.nums[2].same.max)???


	# print("           "+ "n"+ "  " +"mode" + " " + "frequency")
	# for sym_idx in n2.syms:
	# 	print(sym_idx, n2.name[sym_idx],n2.syms[sym_idx].n, n2.syms[sym_idx].mode, n2.syms[sym_idx].most)
	
	# assert n2.syms[1].n == 28 and n2.syms[1].mode == 'sunny' and n2.syms[1].most == 10

	# print("         "+ "n"+ "  " +"mu" + "    " + "sd")
	# for num_idx in n2.nums:	
	# 	print(num_idx, n2.name[num_idx], n2.nums[num_idx].n ,round(n2.nums[num_idx].mu, 2),round(n2.nums[num_idx].sd, 2))
	
	# assert n2.nums[2].n == 28 and round(n2.nums[2].mu, 2) == 73.57 and round(n2.nums[2].sd, 2) == 6.45

	# print('\n')

	# n3 = data()
	# n3.readRows("auto.csv")
	# print("              "+ "n"+ "  " +"mode" + " " + "frequency")
	# for sym_idx in n3.syms:
	# 	print(sym_idx, n3.name[sym_idx],n3.syms[sym_idx].n, n3.syms[sym_idx].mode, n3.syms[sym_idx].most)
	# #print(n3.syms[1].n,n3.syms[1].mode,n3.syms[1].most)
	# assert n3.syms[1].n == 398 and n3.syms[1].most == 204

	# print("                 "+ "n"+ "   " +"mu" + "      " + "sd")
	# for num_idx in n3.nums:	
	# 	print(num_idx, n3.name[num_idx], n3.nums[num_idx].n ,round(n3.nums[num_idx].mu, 2),round(n3.nums[num_idx].sd, 2))

	# assert n3.nums[2].n == 398 and round(n3.nums[2].mu, 2) == 193.43 and round(n3.nums[2].sd, 2) == 104.27
	
if __name__== "__main__":
  O.report()

