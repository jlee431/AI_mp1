import heapq

# Search Frontiers

# DFS
class FrontierDFS:
	def __init__(self):
		self.f = []

	def getState(self):
		if(self.f):
			return self.f.pop()
		else:
			return None

	def addState(self, state):
		if(not self.isStateRepeated(state)):
			self.f.append(state)

	def isStateRepeated(self, state):
		for s in self.f:
			if(s.toString() == state.toString()):
				return True
		return False

	def isEmpty(self):
		return not self.f

# BFS
class FrontierBFS:
	def __init__(self):
		self.f = []

	def getState(self):
		if(self.f):
			return self.f.pop(0)
		else:
			return None

	def addState(self, state):
		if(not self.isStateRepeated(state)):
			self.f.append(state)

	def isStateRepeated(self, state):
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

	def getState(self):
		if(self.f):
			return heapq.heappop(self.f)
		else:
			return None

	def addState(self, state):
		if(not self.isStateRepeated(state)):
			heapq.heappush(self.f, state)

	def isStateRepeated(self, state):
		for s in self.f:
			if(s.toString() == state.toString()):
				return True
		return False

	def isEmpty(self):
		return not self.f