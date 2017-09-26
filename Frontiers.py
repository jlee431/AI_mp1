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
			self.explored[s.toString()] = True
			return s
		else:
			return None

	def addState(self, state):
		if(not self.isStateRepeated(state)):
			self.f.append(state)

	def isStateRepeated(self, state):
		if(state.toString() in self.explored):
			return True
		try:
			self.f.index(s)
			return True
		except ValueError:
			return False
		#for s in self.f:
		#	if(s.toString() == state.toString()):
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
			self.explored[s.toString()] = True
			return s
		else:
			return None

	def addState(self, state):
		if(not self.isStateRepeated(state)):
			self.f.append(state)

	def isStateRepeated(self, state):
		if(state.toString() in self.explored):
			return True
		for s in self.f:
			if(s.toString() == state.toString()):
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
			self.explored[s.toString()] = True
			return s
		else:
			return None

	def addState(self, state):
		if(not self.isStateRepeated(state)):
			heapq.heappush(self.f, state)

	def isStateRepeated(self, state):
		if(state.toString() in self.explored):
			return True
		for s in self.f:
			if(s.toString() == state.toString()):
				return True
		return False

	def isEmpty(self):
		return not self.f

# A*
class FrontierAStar:
	def __init__(self):
		self.f = []
		self.explored = {}

	def getState(self):
		if(self.f):
			s = heapq.heappop(self.f)
			self.explored[s.toString()] = True
			return s
		else:
			return None

	def addState(self, state):

		# Check for repeats
		if(state.toString() in self.explored):
			return
		try:
			i = self.f.index(state)
			if self.f[i].path_cost > state.path_cost:
				self.f[i] = state
				heapq.heapify(self.f)
				return
		except ValueError:
			pass

		# Add state to frontier
		heapq.heappush(self.f, state)

	def isStateRepeated(self, state):
		if(state.toString() in self.explored):
			return True
		try:
			i = self.f.index(state)
			if self.f[i].path_cost > state.path_cost:
				self.f[i] = state
				heapq.heapify(self.f)
				return True

		except ValueError:
			return False

		return False
		#for i, s in enumerate(self.f):
		#	if(s.toString() == state.toString()):
		#		if(s.path_cost > state.path_cost):
		#			self.f[i] = state
		#			heapq.heapify(self.f)
		#		return True
		#return False

	def isEmpty(self):
		return not self.f