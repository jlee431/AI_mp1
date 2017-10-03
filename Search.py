import sys
import string
import heapq
from imageio import *
from Frontiers import *
import numpy as np

# Stores distances between two points in the maze
distDictionary = {}

# Calculates the distance between two points in the maze
def calcDist(maze, start_x, start_y, goal_x, goal_y):

	# No need to calculate distance from a point to itself
	if(start_x == goal_x and start_y == goal_y):
		return 0

	# Check if this distance has already been calculated
	tup = ((start_x,start_y),(goal_x, goal_y))
	if(tup in distDictionary):
		return distDictionary[tup]

	# Set the goal in the maze and create the empty frontier
	maze[goal_y][goal_x] = '.'
	f = FrontierAStar()

	# Save state values
	h = State.heuristic
	n = State.num_dots
	c = State.compareFunc

	# Perform the A* search
	retval = search(maze, f, 1, [(0, (goal_x, goal_y))], start_x, start_y, False)

	# Reset state values
	State.heuristic = h
	State.num_dots = n
	State.compareFunc = c

	# Reset maze to initial layout
	maze[goal_y][goal_x] = ' '

	# Save this distance in dictionary
	distDictionary[tup] = retval[0]
	distDictionary[((goal_x, goal_y),(start_x,start_y))] = retval[0]
	
	return retval[0]

# Finds the root of node x in disjoint set representation
def root(sets, x):
	while sets[x] != x:
		sets[x] = sets[sets[x]]
		x = sets[x]
	return x

# Unites the set containing x with the set containing y
def union1(sets, x, y):
	p = root(sets, x)
	q = root(sets, y)
	sets[p] = sets[q]

# The state representation class for the search algorithm
class State:
	# Distinguishes between Greedy and A*
	compareFunc = 0

	# Determines which heuristic to use
	heuristic = None

	# The initial number of dots in the maze
	num_dots = 0

	def __init__(self, x, y, d, el, pc = 0, p = None):
		self.x_pos = x
		self.y_pos = y
		self.dots_left = d
		self.eaten_list = el
		self.path_cost = pc
		self.parent = p

		self.heuristic = None

		# Creates id unique to this state based on x position, y position, and which dots remain
		self.id = str(x) + ' ' + str(y) + ' ' + str.join('', map(lambda x: str(x[0]), el))

	def minSpanTree(self):
		# Construct list of nodes
		node_list = []
		for pair in self.eaten_list:
			# If dot exists, add it as a node
			if pair[0] == 0:
				node_list.append((pair[1][0], pair[1][1]))

		# Add the current position as a node
		node_list.append((self.x_pos, self.y_pos))
		num_nodes = len(node_list)

		# Create priority queue of edges
		edge_heap = [None] * ((num_nodes * (num_nodes-1)) // 2)
		edge_index = 0
		for node1_index in range(num_nodes):
			for node2_index in range(node1_index+1, num_nodes):
				# Calculate the distance between the two points in the maze
				dist = calcDist(blank_maze, node_list[node1_index][0], node_list[node1_index][1], node_list[node2_index][0], node_list[node2_index][1])
				edge_heap[edge_index] = ((dist, (node1_index, node2_index)))
				edge_index = edge_index + 1

		# Sort edges by weight
		edge_heap.sort()

		# Create disjoint set representation
		sets = [i for i in range(num_nodes)]
		edges_in_tree = 0
		edge_index = 0
		tree_weight = 0

		# Add edges to tree from smallest to largest
		while edges_in_tree < num_nodes - 1:
			edge = edge_heap[edge_index]
			edge_index = edge_index + 1

			edge_weight = edge[0]
			node1 = edge[1][0]
			node2 = edge[1][1]

			# Check if node1 and node2 are already connected
			if(root(sets, node1) != root(sets, node2)):
				# Connect add edge node1=>node2 to tree
				edges_in_tree = edges_in_tree + 1
				tree_weight = tree_weight + edge_weight
				union1(sets, node1, node2)

		# Return the total weight of edges in the tree
		return tree_weight

	# Calculates the heuristic for this state
	def calcHeuristic(self):
		# Check if the calculation has already been done
		if(self.heuristic is None):
			if(State.heuristic == 0):
				# Heuristic 1: Manhattan Distance to the first dot
				x_dist = abs(self.eaten_list[0][1][0] - self.x_pos)
				y_dist = abs(self.eaten_list[0][1][1] - self.y_pos)
				self.heuristic =  x_dist + y_dist
			else:
				# Heuristic 2: Total weight of minimum spanning tree
				self.heuristic = self.minSpanTree()
		return self.heuristic

	# Calculates the evaluation function for A* Search
	def calcEvalFunc(self):
		self.calcHeuristic()
		return self.heuristic + self.path_cost

	# Determines whether this state is a goal state
	def isGoal(self):
		if(self.dots_left):
			return False
		return True;

	# Uses evaluation function/heuristic for state comparision
	def __lt__(self, other):
		if State.compareFunc:
			return self.calcEvalFunc() < other.calcEvalFunc()
		else:
			return self.calcHeuristic() < other.calcHeuristic()

	# Uses evaluation function/heuristic for state comparision
	def __gt__(self, other):
		if State.compareFunc:
			return self.calcEvalFunc() > other.calcEvalFunc()
		else:
			return self.calcHeuristic() < other.calcHeuristic()

	# Uses state id to check for equality
	def __eq__(self, other):
		return self.id == other.id

# List of actions that the agent can perform (Only movement)
actions = [(-1,0),(0,-1),(1,0),(0,1)]

# Attemps to perform all actions on state; adds children to frontier
def DoActions(maze, frontier, dot_map, state, actionList):

	for action in actionList:
		# Determine the new position
		new_x = state.x_pos + action[0]
		new_y = state.y_pos + action[1]

		char = maze[new_y][new_x]

		# Check if action is valid
		if(char == ' ' or char == 'P'):
			frontier.addState(State(new_x, new_y, state.dots_left, state.eaten_list[:], state.path_cost + 1, state))
		elif(char == '.'):
			# Update the list of dots
			elist = state.eaten_list[:]
			dots_left = state.dots_left
			i = dot_map[(new_x, new_y)]

			# Only update if this dot has not been collected before
			if(elist[i][0] == 0 and elist[i][1][0] == new_x and elist[i][1][1] == new_y):
				elist[i] = (1, (new_x, new_y))
				dots_left = dots_left - 1

			frontier.addState(State(new_x,new_y, dots_left, elist, state.path_cost + 1, state))

def addFrame(frame_list, maze, dot_map, state):
	square_size = 10
	frame = np.zeros((maze_height*square_size, maze_width*square_size, 3), dtype=np.uint8)

	y = 0
	x = 0
	for y in range(maze_height):
		for x in range(maze_width):
			if(x == state.x_pos and y == state.y_pos):
				center = square_size//2
				for i in range(square_size):
					for j in range(square_size):
							i_dist = abs(i - center)
							j_dist = abs(j - center)
							if(i_dist + j_dist < 3):
								frame[square_size*y+i][square_size*x+j] = [0,255,0]
							else:
								frame[square_size*y+i][square_size*x+j] = [0,200,0]
			elif(maze[y][x] == '.' or maze[y][x] in ans):
				try:
					dot_index = dot_map[(x, y)]
					if(state.eaten_list[dot_index][0] == 0):
						for i in range(square_size):
							for j in range(square_size):
								frame[square_size*y+i][square_size*x+j] = [255,255,255]
				except KeyError:
						pass
			elif(maze[y][x] == '%'):
				for i in range(square_size):
					for j in range(square_size):
						frame[square_size*y+i][square_size*x+j] = [255,0,0]

	frame_list.insert(0, frame)

# Performs the search over maze starting from x_pos, y_pos
def search(maze, frontier, num_dots, dots, x_pos, y_pos, alter_maze = True):

	# Set heuristic
	if(num_dots > 1):
		State.heuristic = 2
		State.num_dots = num_dots
	else:
		State.heuristic = 0
		State.num_dots = 1

	# Initialize mapping from dot coordinates to dot index
	dot_map = {}
	for i in range(num_dots):
		dot_map[(dots[i][1][0],dots[i][1][1])] = i

	# Add initial state
	frontier.addState(State(x_pos, y_pos, num_dots, dots))
	nodes_expanded = 0
	path_cost = 0

	# Start Search
	while not frontier.isEmpty():
		# Get the next state
		current_state = frontier.getState()

		# Check if current state is a goal state
		if(current_state.isGoal()):
			path_cost = current_state.path_cost
			target = num_dots - 1

			parent = current_state.parent
			child = current_state

			frames = []

			# Update the maze with the path
			if(alter_maze):
				while parent:
					# Add frame
					addFrame(frames, maze, dot_map, child)

					if(num_dots == 1):
						# Trace the path taken with '.'
						maze[child.y_pos][child.x_pos] = '.'

					elif(maze[child.y_pos][child.x_pos] == '.'):
						# Number the dots in the order they were collected
						for i in range(num_dots):
							# Only mark this dot if child was the state that collected it 
							if(parent.eaten_list[i][0] == 0 and child.eaten_list[i][0] == 1):
								maze[child.y_pos][child.x_pos] = ans[target]
								target = target - 1
								break

					child = parent
					parent = parent.parent
				addFrame(frames, maze, dot_map, child)
				mimwrite(animation_name, frames)
			break

		# Update expanded state counter
		nodes_expanded = nodes_expanded + 1

		# Check all four directions:
		DoActions(maze, frontier, dot_map, current_state, actions)

	return (path_cost, nodes_expanded)
	

if(len(sys.argv) !=3):
	print("USAGE: Search.py mazefile search")
	sys.exit()

maze_file = open(sys.argv[1], 'r')

# Load maze
maze = []
blank_maze = []
for line in maze_file:
	line_list = list(line)
	if(line_list[-1] == '\n'):
		line_list.pop()
	maze.append(line_list)
	blank_maze.append(line_list[:])

maze_height = len(maze)
maze_width = len(maze[0])

option = sys.argv[2].lower()

# Set main search type
if(option == 'dfs'):
	frontier = FrontierDFS()
elif(option == 'bfs'):
	frontier = FrontierBFS()
elif(option == 'greedy'):
	frontier = FrontierGreedy()
	State.compareFunc = 0
elif(option == 'astar'):
	frontier = FrontierAStar()
	State.compareFunc = 1
else:
	print("Unrecognized search: " + option)
	sys.exit()

# Open output file
filename = "soln_" + sys.argv[1][:-4] + "_" + option + ".txt"
animation_name = "animations\soln_" + sys.argv[1][:-4] + "_" + option + ".gif"
file = open(filename, "w+")
write = file.write

# List of characters for multiple dot searches
ans = string.digits + string.ascii_letters 

# Initialize starting values
num_dots = 0
dots = []
y_pos = 0
x_pos = 0
for row in range(len(maze)):
	for col in range(len(maze[row])):
		if(maze[row][col] == '.'):
			blank_maze[row][col] = ' '
			dots.append((0, (col, row)))
			num_dots = num_dots + 1
		elif(maze[row][col] == 'P'):
			y_pos = row
			x_pos = col

# Perform search
retval = search(maze, frontier, num_dots, dots, x_pos, y_pos)

# Write maze solution, path cost, and nodes expanded 
for line in maze:
	for c in line:
		write(c)
	write('\n')

write('Path cost: ' + str(retval[0]) + '\n')
write('Nodes expanded: ' + str(retval[1]))
file.close()