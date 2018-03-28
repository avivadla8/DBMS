import sys
from math import *

class BPtree:
	def __init__(self,n):
		self.n = n
		self.root = None


	def insert(self,key):
		if self.root == None:
			self.root = Node(self.n,True)
			self.root.keys[0] = key
			self.root.count_keys +=1
		else:
			self.root.insert(key)
			if self.root.overflow:
				new_root = Node(self.n,False)
				new_root.pointers[0] = self.root
				self.root = new_root
				self.root.split_child(0)

	def traverse(self):
		if self.root == None:
			print("No record Inserted")
		else:
			self.root.traverse()

	def find(self,val):
		if self.root == None:
			print("NO")
		else:
			self.root.find(val)

	def count(self,val):
		if self.root == None:
			print("0")
		else:
			value = self.root.count(val)
			print(value)

	def range_count(self,val1,val2):
		if self.root == None:
			print("0")
		else:
			value = self.root.range_count(val1,val2)
			print(value)


class Node:
	def __init__(self,n,flag):
		self.n = n
		self.leaf = flag
		self.count_keys = 0
		self.keys = [None]*n
		self.extra = None
		self.extra_pointer = None
		self.overflow = False
		self.pointers = [None]*(n+1)

	def insert(self,value):
		if self.leaf == False:
			ptr = None
			ptr_flag = 0
			for i in range(0,self.count_keys):
				if value<self.keys[i]:
					ptr = self.pointers[i]
					ptr_flag = 1
					break
			if value>=self.keys[self.count_keys-1]:
				ptr = self.pointers[self.count_keys]
				ptr_flag = 1
			ptr.insert(value)
			for i in range(0,self.count_keys+1):
				if self.pointers[i].overflow:
					self.split_child(i)
					i+=1
					break

		elif self.leaf == True:
			if self.count_keys<self.n:
				poi = self.count_keys-1
				while(poi>=0 and self.keys[poi]>value):
					self.keys[poi+1] = self.keys[poi]
					poi-=1
				self.keys[poi+1] = value
				self.count_keys +=1
			else:
				self.extra = value
				self.overflow = True

	def traverse(self):
		if self.leaf:
			for i in range(0,self.count_keys):
				print(self.keys[i])
			if self.pointers[self.n] != None:
				self.pointers[self.n].traverse()
		else:
			print(self.keys)
			self.pointers[0].traverse()

	def count(self,val):
		if self.leaf:
			count_val = 0
			over_flag =0
			for i in range(0,self.count_keys):
				if self.keys[i]<val:
					continue
				elif self.keys[i] == val:
					count_val +=1
				else:
					over_flag =1
					break
			if over_flag:
				return count_val
			else:
				if self.pointers[self.n] != None:
					count_val += self.pointers[self.n].count(val)
				return count_val
		else:
			ptr = None
			ptr_flag = 0
			for i in range(0,self.count_keys):
				if val-1<self.keys[i]:
					ptr = self.pointers[i]
					ptr_flag = 1
					break
			if val-1>=self.keys[self.count_keys-1]:
				ptr = self.pointers[self.count_keys]
				ptr_flag = 1
			return ptr.count(val)

	def range_count(self,val1,val2):
		if self.leaf:
			count_val = 0
			over_flag =0
			for i in range(0,self.count_keys):
				if self.keys[i]<val1:
					continue
				elif self.keys[i] >= val1 and self.keys[i] <=val2:
					count_val +=1
				else:
					over_flag =1
					break
			if over_flag:
				return count_val
			else:
				if self.pointers[self.n] != None:
					count_val += self.pointers[self.n].range_count(val1,val2)
				return count_val
		else:
			ptr = None
			ptr_flag = 0
			for i in range(0,self.count_keys):
				if val1-1<self.keys[i]:
					ptr = self.pointers[i]
					ptr_flag = 1
					break
			if val1-1>=self.keys[self.count_keys-1]:
				ptr = self.pointers[self.count_keys]
				ptr_flag = 1
			return ptr.range_count(val1,val2)


	def find(self,val):
		if self.leaf:
			temp_flag = 0
			for i in range(0,self.count_keys):
				if self.keys[i] == val:
					temp_flag=1
					break
			if temp_flag==1:
				print("YES")
			else:
				print("NO")
		else:
			ptr = None
			ptr_flag = 0
			for i in range(0,self.count_keys):
				if val<self.keys[i]:
					ptr = self.pointers[i]
					ptr_flag = 1
					break
			if val>=self.keys[self.count_keys-1]:
				ptr = self.pointers[self.count_keys]
				ptr_flag = 1
			ptr.find(val)


	def split_child(self,index):
		new_node = Node(self.n,self.pointers[index].leaf)
		main_node = self.pointers[index]
		temp1 = int(ceil((self.n+1)/2)-1)
		if self.pointers[index].leaf:
			temp1 = int(floor((self.n+1)/2))



		val_node = None
		poi_node = None

		if main_node.leaf:
			if main_node.extra < main_node.keys[temp1-1]:
				i = temp1-1
				while(i<=main_node.n-1):
					new_node.keys[i-(temp1-1)] = main_node.keys[i]
					main_node.keys[i] = None
					i+=1

				i = temp1-2
				while(i>=0 and main_node.keys[i]>main_node.extra):
					main_node.keys[i+1] = main_node.keys[i]
					i-=1
				main_node.keys[i+1] = main_node.extra
				main_node.extra = None
				main_node.overflow = False
			else:
				i = temp1
				poi = 0
				while(i<=main_node.n-1):
					if main_node.overflow and (main_node.extra < main_node.keys[i]):
						new_node.keys[poi] = main_node.extra
						main_node.extra = None
						main_node.overflow = False
						poi +=1
					else:
						new_node.keys[poi] = main_node.keys[i]
						main_node.keys[i] = None
						poi +=1
						i +=1
				if main_node.overflow:
					new_node.keys[poi] = main_node.extra
					main_node.extra = None
					main_node.overflow = False

			val_node = new_node.keys[0]
			poi_node = new_node
		else:
			if main_node.extra < main_node.keys[temp1-1]:
				i = temp1-1
				poi= 0
				val_node = main_node.keys[i]
				main_node.keys[i] = None
				poi_node = new_node
				i +=1
				while(i<=main_node.n-1):
					new_node.pointers[poi] = main_node.pointers[i]
					new_node.keys[poi] = main_node.keys[i]
					main_node.pointers[i] = None
					main_node.keys[i] = None
					poi +=1
					i +=1
				new_node.pointers[poi] = main_node.pointers[i]
				main_node.pointers[i] = None

				i = temp1-2
				while(i>=0 and main_node.keys[i] > main_node.extra):
					main_node.keys[i+1] = main_node.keys[i]
					main_node.pointers[i+2] = main_node.pointers[i+1]
					i -=1
				main_node.keys[i+1] = main_node.extra
				main_node.pointers[i+2] = main_node.extra_pointer
				main_node.extra = None
				main_node.extra_pointer = None
				main_node.overflow = False

			else:
				i = temp1
				poi = 0
				if main_node.extra < main_node.keys[i]:
					val_node = main_node.extra
					poi_node = new_node
					new_node.pointers[0] = main_node.extra_pointer
					main_node.extra  = None
					main_node.extra_pointer = None
					main_node.overflow = False
					while(i<=main_node.n-1):
						new_node.keys[poi] = main_node.keys[i]
						new_node.pointers[poi+1] = main_node.pointers[i+1]
						main_node.keys[i] = None
						main_node.pointers[i+1] = None
						i+=1
						poi +=1

				else:
					val_node = main_node.keys[temp1]
					main_node.keys[temp1] = None
					poi_node = new_node
					new_node.pointers[0] = main_node.pointers[i+1]
					main_node.pointers[i+1] = None
					i+=1
					while(i<=main_node.n-1):
						if main_node.overflow and (main_node.extra < main_node.keys[i]):
							new_node.keys[poi] = main_node.extra
							new_node.pointers[poi+1] = main_node.extra_pointer
							main_node.extra = None
							main_node.extra_pointer = None
							main_node.overflow = False
							poi +=1
						else:
							new_node.keys[poi] = main_node.keys[i]
							new_node.pointers[poi+1] = main_node.pointers[i+1]
							main_node.keys[i] = None
							main_node.pointers[i+1] = None
							poi +=1
							i +=1
					if main_node.overflow:
						new_node.keys[poi] = main_node.extra
						new_node.pointers[poi+1] = main_node.extra_pointer
						main_node.extra = None
						main_node.extra_pointer = None
						main_node.overflow = False


		if main_node.leaf:
			new_node.count_keys = self.n-(temp1)+1
		else:
			new_node.count_keys = self.n-(temp1)
		main_node.count_keys = temp1



		if self.count_keys < self.n:
			poi = self.count_keys-1

			while(poi>=0 and self.keys[poi]>val_node):
				self.keys[poi+1] = self.keys[poi]
				self.pointers[poi+2] = self.pointers[poi+1]
				poi-=1
			self.keys[poi+1] = val_node
			self.pointers[poi+2] = poi_node
			self.count_keys +=1
		else:
			self.extra = val_node
			self.extra_pointer = poi_node
			self.overflow = True

		if main_node.leaf:
			new_node.pointers[self.n] = main_node.pointers[self.n]
			main_node.pointers[self.n] = new_node



if __name__ == "__main__":
	filename = sys.argv[1]
	M = sys.argv[2]
	B = sys.argv[3]
	n = int(floor((int(B)-8)/12.0))
	root = BPtree(n)
	f = open(filename,'r')
	lines = f.readlines()
	for line in lines:
		word = line.split(' ')
		if word[0]=="INSERT":
			root.insert(int(word[1]))
		elif word[0] == "FIND":
			root.find(int(word[1]))
		elif word[0] == "COUNT":
			root.count(int(word[1]))
		elif word[0] == "RANGE":
			root.range_count(int(word[1]),int(word[2]))

