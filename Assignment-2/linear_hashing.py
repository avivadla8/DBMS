from math import *
import sys

class linear_hash:
	def __init__(self,n):
		self.n = n
		self.hash_list = [None]*2
		self.max = 1
		self.n_bits = 1
		self.hash_list[0] = Block(self.n,True)
		self.hash_list[1] = Block(self.n,True)

	def insert(self,val):
		hash_value = val % int(pow(2,self.n_bits))
		if hash_value > self.max:
			hash_value = hash_value - int(pow(2,self.n_bits-1))

		if not self.hash_list[hash_value].find(val):
			self.hash_list[hash_value].insert(val)
			print(val)

		self.calc_occupancy()

	def calc_occupancy(self):
		Total = 0
		occupied = 0
		for temp in self.hash_list:
			Total = Total+self.n
			occupied += temp.count

		if (occupied*1.0)/Total >=0.75:
			self.max +=1
			temp = Block(self.n,True)
			self.hash_list.append(temp)
			if self.max > int(pow(2,self.n_bits))-1:
				self.n_bits +=1

			self.re_hash(self.max- int(pow(2,self.n_bits-1)))

	def re_hash(self,index):
		temp = self.hash_list[index]
		temp2 = self.hash_list[self.max]

		for i in range(0,temp.count):
			poi = 0
			val = temp.list[i] % int(pow(2,self.n_bits))
			if val == self.max:
				temp2.insert(temp.list[i])
			else:
				temp.list[poi] = temp.list[i]
				poi+=1

		temp.count = poi

		if overflow_flag == True:
			old_list = temp.overflow
			temp.overflow = []
			temp.overflow_flag = False
			for temp3 in old_list:
				for i in range(0,temp3.count):
					val = temp3.list[i] % int(pow(2,self.n_bits))
					if val == self.max:
						temp2.insert(temp3.list[i])
					else:
						temp.insert(temp3.list[i])



class Block:
	def __init__(self,n,flag):
		self.n = n
		self.count = 0
		self.list = [None]*n
		self.main = flag
		self.overflow = []
		self.overflow_flag = False

	def insert(self,val):
		if self.count < self.n:
			self.list[self.count] = val
			self.count +=1
		else:
			if self.overflow_flag == False:
				self.overflow_flag = True
				temp = Block(self.n,False)
				temp.insert(val)
				self.overflow.append(temp)
			else:
				temp_flag =0
				for temp in self.overflow:
					if temp.count == self.n:
						continue
					else:
						temp.insert(val)
						temp_flag =1
				if temp_flag==0:
					temp = Block(self.n,False)
					temp.insert(val)
					self.overflow.append(temp)

	def find(self,val):
		found = False
		for i in range(0,self.count):
			if self.list[i] == val:
				found = True
				break

		if not found:
			if self.overflow_flag == True:
				for temp in self.overflow:
					for i in range(0,temp.count):
						if temp.list[i]==val:
							found = True
							break
					if found:
						break
		return found


if __name__ == "__main__":
	filename = sys.argv[1]
	M = sys.argv[2]
	B = sys.argv[3]
	n = int(floor(int(B)/4.0))
	table = linear_hash(n)

	f = open(filename,'r')
	lines = f.readlines()
	for line in lines:
		val = int(line)
		table.insert(val)
