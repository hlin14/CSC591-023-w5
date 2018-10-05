from num import num
from sym import sym
import re
import random
import operator
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



	def unsuper(self, obj):
		rows = obj.rows
		enough = len(rows) ** 0.5 #0.5 is magic number
		#print(enough)
		def band(c, lo, hi):
			if lo == 1:
				return ".." + str(rows[hi][c])
			elif hi == most:   #most!?!!!!!!!
				return str(rows[lo][c]) + ".."
			else:
				return str(rows[lo][c]) + ".." + str(rows[hi][c])

		def argmin(c, lo, hi):
			cut = None
			if (hi - lo > 2 * enough):
				l, r = num(), num()
				for i in range(lo, hi + 1):
					r.numInc(rows[i][c])
				#get the total sd first
				best = r.sd

				#now, decreseInc from r and increase from left, to find the best sd
				for i in range(lo, hi + 1):
					x = rows[i][c]
					l.numInc(x)
					r.numDec(x)
					if l.n >= enough and r.n >= enough:
						tmp = num.numXpect(l, r) * 1.05  #1.05 is margin which is magic number
						if tmp < best:
							cut, best = i, tmp
			return cut



		def cuts(c, lo, hi, pre):
			#?
			#txt = pre + str(obj.rows[lo][c]) + '..' + str(obj.rows[hi][c])
			#print("cut!!!!!!!!")
			cut = argmin(c, lo, hi)
			if cut:
				#? fyi
				cuts(c, lo, cut, pre + "|..")
				cuts(c, cut + 1, hi, pre + "|..")
			else:#stop cut
				b = band(c, lo, hi)
				#modify the row into b
				for r in range(lo, hi + 1):
					rows[r][c] = b

		#to find the largest number not '?' from the right
		def stop(c, t): #t is rows, c is col
			for i in range(len(t) - 1, -1, -1):
				if t[i][c] != '?':
					return i + 1
				else:
					return 0

		def sortRow(c, rows):
			dic = {}

			rows = sorted(rows.items(), key = lambda x:x[1][c])
			
			i = 1
			for item in rows:
				key, val = item
				#print(key, val)
				dic[i] = val
				i += 1

			# for key, val in dic.items():
			# 	print(key, val)
			return dic


		for c in obj.indeps:
			if obj.nums.get(c, "") != "":


				# for key, val in obj.rows.items():
				# 	print(key, val)
				# print("====")

				rows = sortRow(c, rows)  #ksort(c, rows)

				most = stop(c, rows)
				#print("most:", most)
				cuts(c, 1, most, "|..")


				for key, val in rows.items():
					print(key, val)


		return self

@O.k
def testing():

	# #part1
	# n2 = data()
	# result2 = n2.showDom("weatherLong.csv")

	# result2.sort(key=lambda x: x[5])

	# for item in result2:
	# 	print(item)

	# #check the row with the biggest dom is the smallest humid
	# assert result2[-1][2] == 65.0


	# n3 = data()
	# result3 = n3.showDom("auto.csv")

	# result3.sort(key=lambda x: x[8])


	# aveWeigh1 = 0
	# aveWeigh2 = 0

	# aveAcce1 = 0
	# aveAcce2 = 0

	# aveMpg1 = 0
	# aveMpg2= 0

	# for item in result3[:10]:
	# 	aveWeigh1 += item[3]
	# 	aveAcce1 += item[4]
	# 	aveMpg1 += item[7]
	# 	print(item)

	# aveWeigh1 /= 10
	# aveAcce1 /= 10
	# aveMpg1 /= 10

	# for item in result3[-10:]:
	# 	aveWeigh2 += item[3]
	# 	aveAcce2 += item[4]
	# 	aveMpg2 += item[7]
	# 	print(item)

	# aveWeigh2 /= 10
	# aveAcce2 /= 10
	# aveMpg2 /= 10
	
	# assert aveWeigh1 > aveWeigh2 and aveAcce1 < aveAcce2 and aveMpg1 < aveMpg2

	#part2
	n4 = data()
	obj = n4.unsuper(n4.readRows("weatherLong.csv"))
	#print(obj.indeps) [1, 2, 4]

if __name__== "__main__":
  O.report()

