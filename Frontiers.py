import heapq

# Search Frontiers

# DFS
class FrontierDFS:
	def __init__(self):
		self.f = []
		self.explored = {}

	def getState(self):
		if(self.f):
			s = self.f.pop()
			self.explored[s.id] = True
			return s
		else:
			return None

	def addState(self, state):
		if(not self.isStateRepeated(state)):
			self.f.append(state)

	def isStateRepeated(self, state):
		if(state.id in self.explored):
			return True
		try:
			self.f.index(s)
			return True
		except ValueError:
			return False
		#for s in self.f:
		#	if(s.id == state.id):
		#		return True
		#return False

	def isEmpty(self):
		return not self.f

# BFS
class FrontierBFS:
	def __init__(self):
		self.f = []
		self.explored = {}

	def getState(self):
		if(self.f):
			s = self.f.pop(0)
			self.explored[s.id] = True
			return s
		else:
			return None

	def addState(self, state):
		if(not self.isStateRepeated(state)):
			self.f.append(state)

	def isStateRepeated(self, state):
		if(state.id in self.explored):
			return True
		for s in self.f:
			if(s.id == state.id):
				return True
		return False

	def isEmpty(self):
		return not self.f

# Greedy
class FrontierGreedy:
	def __init__(self):
		self.f = []
		self.explored = {}

	def getState(self):
		if(self.f):
			s = heapq.heappop(self.f)
			self.explored[s.id] = True
			return s
		else:
			return None

	def addState(self, state):
		if(not self.isStateRepeated(state)):
			heapq.heappush(self.f, state)

	def isStateRepeated(self, state):
		if(state.id in self.explored):
			return True
		for s in self.f:
			if(s.id == state.id):
				return True
		return False

	def isEmpty(self):
		return not self.f

# A*
class FrontierAStar:

	heappush = heapq.heappush
	heappop = heapq.heappop
	heapify = heapq.heapify

	def __init__(self):
		self.f = []
		self.explored = {}

	def getState(self):
		if(self.f):
			s = self.f.pop(0)
			self.explored[s.id] = True
			return s
		else:
			return None

	def addState(self, state):

		# Check for repeats
		if(state.id in self.explored):
			return

		f = self.f

		start = 0
		end = len(f)-1
		index = end//2
		if(start <= end):
			while start < end and not state == f[index]:
				if(state < f[index]):
					end = index-1
				else:
					start = index+1
				index = (start + end)//2

			if(state == f[index]):
				if(f[index].path_cost > state.path_cost):
					f[index] = state
					f.sort()
					return
				
		f.insert(index, state)

	def isStateRepeated(self, state):
		if(state.id in self.explored):
			return True
		try:
			i = self.f.index(state)
			if self.f[i].path_cost > state.path_cost:
				self.f[i] = state
				FrontierAStar.heapify(self.f)
				return True

		except ValueError:
			return False

		return False

	def isEmpty(self):
		return not self.f