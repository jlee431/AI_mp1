import heapq

# Search Frontiers

# DFS
class FrontierDFS:
	def __init__(self):
		self.f = []
		self.explored = {}

	# Returns the next state from the frontier
	def getState(self):
		if(self.f):
			# Pop state off of stack
			s = self.f.pop()
			self.explored[s.id] = True
			return s
		else:
			return None

	# Attempts to add state to frontier
	def addState(self, state):
		# Check for repeated state
		if(not self.isStateRepeated(state)):
			# Push state to top of stack
			self.f.append(state)

	# Checks if state has been repeated
	def isStateRepeated(self, state):
		# Check if state has been explored
		if(state.id in self.explored):
			return True

		# Check if state is in the frontier
		for s in self.f:
			if(s.id == state.id):
				return True

	def isEmpty(self):
		return not self.f

# BFS
class FrontierBFS:
	def __init__(self):
		self.f = []
		self.explored = {}

	# Returns the next state from the frontier
	def getState(self):
		if(self.f):
			# Pops state from front of queue
			s = self.f.pop(0)
			self.explored[s.id] = True
			return s
		else:
			return None

	# Attempts to add state to frontier
	def addState(self, state):
		if(not self.isStateRepeated(state)):
			# Pushes state to back of queue
			self.f.append(state)

	# Checks if state has been repeated
	def isStateRepeated(self, state):
		# Check if state has been explored
		if(state.id in self.explored):
			return True

		# Check if state is in the frontier
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

	# Returns the next state from the frontier
	def getState(self):
		if(self.f):
			# Pop state from priority queue
			s = heapq.heappop(self.f)
			self.explored[s.id] = True
			return s
		else:
			return None

	# Attempts to add state to frontier
	def addState(self, state):
		# Check if state has been explored
		if(state.id in self.explored):
			return

		# Check if state is in frontier
		try:
			i = self.f.index(state)
			return
		except ValueError:
			pass

		# Add state to priority queue
		FrontierAStar.heappush(self.f, state)

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

	# Returns the next state from the frontier
	def getState(self):
		if(self.f):
			# Pop state from priority queue
			s = FrontierAStar.heappop(self.f)
			self.explored[s.id] = True
			return s
		else:
			return None

	# Attempts to add state to frontier
	def addState(self, state):

		# Check if state has been explored
		if(state.id in self.explored):
			return

		# Check if state is in frontier
		try:
			i = self.f.index(state)
			if self.f[i].path_cost > state.path_cost:
				self.f[i] = state
				FrontierAStar.heapify(self.f)
			return
		except ValueError:
			pass

		# Add state to priority queue
		FrontierAStar.heappush(self.f, state)

	def isEmpty(self):
		return not self.f