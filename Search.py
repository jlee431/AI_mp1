import sys
import string
import heapq
from Frontiers import *

maxsize = 10000
distDictionary = {}

def calcDist(maze, start_x, start_y, goal_x, goal_y):

	if(start_x == goal_x and start_y == goal_y):
		return 0

	tup = ((start_x,start_y),(goal_x, goal_y))
	if(tup in distDictionary):
		return distDictionary[tup]

	maze[goal_y][goal_x] = '.'
	f = FrontierAStar()

	#print('Startx ' + str(start_x))
	#print('Starty ' + str(start_y))
	#print('Goalx ' + str(goal_x))
	#print('Goaly ' + str(goal_y))

	retval = search(maze, f, 1, [(0, (goal_x, goal_y))], start_x, start_y, False)

	maze[goal_y][goal_x] = ' '
	distDictionary[tup] = retval[0]
	distDictionary[((goal_x, goal_y),(start_x,start_y))] = retval[0]
	return retval[0]

def root(sets, x):
	while sets[x] != x:
		sets[x] = sets[sets[x]]
		x = sets[x]
	return x

def union1(sets, x, y):
	p = root(sets, x)
	q = root(sets, y)
	sets[p] = sets[q]

class State:
	compareFunc = 0
	heuristic = None
	num_dots = 0

	def __init__(self, x, y, d, el, pc = 0, p = None):
		self.x_pos = x
		self.y_pos = y
		self.dots_left = d
		self.eaten_list = el
		self.path_cost = pc
		self.parent = p

		self.heuristic = None
		self.id = str(x) + ' ' + str(y) + ' ' + str.join('', map(lambda x: str(x[0]), el))

	'''def testFunc(self):
		distances = [None]*num_dots
		closest = [None]*num_dots

		h = State.heuristic
		n = State.num_dots

		closest_to_player = maxsize

		for d in range(n):
			pair = self.eaten_list[d]
			if(pair[0] == 0):
					distances[d] = calcDist(blank_maze, self.x_pos, self.y_pos, pair[1][0], pair[1][1])
					if(distances[d] < closest_to_player):
						closest_to_player = distances[d]
					closest[d] = -1
					for i in range(n):
						neigh = self.eaten_list[i]
						if(neigh[0] == 0 and neigh != pair):
							dist = calcDist(blank_maze, neigh[1][0], neigh[1][1], pair[1][0], pair[1][1])
							if(dist < distances[d]):
								distances[d] = dist
								closest[d] = i

		State.heuristic = h
		State.num_dots = n

		player_nearest = 0
		for i in range(num_dots):
			if(closest[i] == -1):
				player_nearest = player_nearest + distances[i]

		if(player_nearest == 0):
			return closest_to_player
		else:
			return player_nearest'''


	def dijkstra(self):
		num_nodes = State.num_dots + 1
		Q = []
		dist = [maxsize]*num_nodes
		prev = [-1]*num_nodes
		layers_from_player = [0]*num_nodes
		dist[0] = 0
		eaten_list = self.eaten_list

		# Save state values
		h = State.heuristic
		n = State.num_dots

		Q.append((0, 0))

		i = 0
		for i in range(len(eaten_list)):
			if(eaten_list[i][0] == 0):
				Q.append((maxsize, i+1))

		while Q:
			u = Q.pop(0)
			u_in = u[1]
			u_dist = u[0]
			i = 0
			while i < num_nodes:
				if(i != u_in):
					if(i != 0 and eaten_list[i-1][0] == 0):
						if(u_in == 0):
							alt = calcDist(blank_maze, self.x_pos, self.y_pos, eaten_list[i-1][1][0], eaten_list[i-1][1][1])
							#alt = abs(self.x_pos - eaten_list[i-1][1][0]) + abs(self.y_pos - eaten_list[i-1][1][1]) 
						else:
							if(prev[u_in] != i and prev[i] != u_in):
								alt = calcDist(blank_maze, eaten_list[u_in-1][1][0], eaten_list[u_in-1][1][1], eaten_list[i-1][1][0], eaten_list[i-1][1][1])
								#alt = abs(eaten_list[u_in-1][1][0] - eaten_list[i-1][1][0]) + abs(eaten_list[u_in-1][1][1] - eaten_list[i-1][1][1])
							else:
								alt = maxsize
						if(alt < dist[i]):
							dist[i] = alt
							prev[i] = u_in
							layers_from_player[i] = layers_from_player[u_in] + 1
				i = i + 1

			for i in range(len(Q)):
				index = Q[i][1]
				Q[i] = (dist[index], index)

		State.heuristic = h
		State.num_dots = n

		summation = 0
		for i in range(num_nodes):
			if(prev[i] != -1):
				summation = summation + dist[i]
		return summation

	def calcHeuristic(self):
		if(self.heuristic is None):
			if(State.heuristic == 0):
				x_dist = abs(self.eaten_list[0][1][0] - self.x_pos)
				y_dist = abs(self.eaten_list[0][1][1] - self.y_pos)
				self.heuristic =  x_dist + y_dist
			else:
				self.heuristic = self.dijkstra()
		return self.heuristic

	def calcEvalFunc(self):
		self.calcHeuristic()
		return self.heuristic + self.path_cost

	def isGoal(self):
		if(self.dots_left):
			return False
		return True;

	def __lt__(self, other):
		if State.compareFunc:
			return self.calcEvalFunc() < other.calcEvalFunc()
		else:
			return self.calcHeuristic() < other.calcHeuristic()

	def __gt__(self, other):
		if State.compareFunc:
			return self.calcEvalFunc() > other.calcEvalFunc()
		else:
			return self.calcHeuristic() < other.calcHeuristic()

	def __eq__(self, other):
		return self.id == other.id

actions = [(-1,0),(0,-1),(1,0),(0,1)]

def DoActions(maze, frontier, dot_map, state, actionList):

	for action in actionList:
		new_x = state.x_pos + action[0]
		new_y = state.y_pos + action[1]

		char = maze[new_y][new_x]
		if(char == ' ' or char == 'P'):
			frontier.addState(State(new_x, new_y, state.dots_left, state.eaten_list.copy(), state.path_cost + 1, state))
		elif(char == '.'):
			elist = state.eaten_list.copy()
			dots_left = state.dots_left
			i = dot_map[(new_x, new_y)]
			if(elist[i][0] == 0 and elist[i][1][0] == new_x and elist[i][1][1] == new_y):
				elist[i] = (1, (new_x, new_y))
				dots_left = dots_left - 1
			frontier.addState(State(new_x,new_y, dots_left, elist, state.path_cost + 1, state))

def search(maze, frontier, num_dots, dots, x_pos, y_pos, alter_maze = True):

	# Set heuristic
	if(num_dots > 1):
		State.heuristic = 2
		State.num_dots = num_dots
	else:
		State.heuristic = 0
		State.num_dots = 1

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

		'''if(alter_maze == True):
			for y in range(len(maze)):
				for x in range(len(maze[row])):
					if(y == current_state.y_pos and x == current_state.x_pos):
						write('X')
					else:
						write(maze[y][x])
				print('')
			input()'''

		# Check if current state is goal state
		if(current_state.isGoal()):
			path_cost = current_state.path_cost
			target = num_dots - 1

			parent = current_state.parent
			child = current_state

			if(alter_maze):
				while parent:
					if(num_dots == 1):
						maze[child.y_pos][child.x_pos] = '.'
					elif(maze[child.y_pos][child.x_pos] == '.'):
						for i in range(num_dots):
							if(parent.eaten_list[i][0] == 0 and child.eaten_list[i][0] == 1):
								maze[child.y_pos][child.x_pos] = ans[target]
								target = target - 1
								break

					child = parent
					parent = parent.parent
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

maze = []
blank_maze = []
for line in maze_file:
	line_list = list(line)
	if(line_list[-1] == '\n'):
		line_list.pop()
	maze.append(line_list)
	blank_maze.append(line_list[:])

option = sys.argv[2].lower()

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

filename = "soln_" + sys.argv[1][:-4] + "_" + option + ".txt"
#file = open(filename, "w+")
#write = file.write
write = sys.stdout.write

ans = string.digits + string.ascii_letters 

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

for line in blank_maze:
	for c in line:
		write(c)
	write('\n')

retval = search(maze, frontier, num_dots, dots, x_pos, y_pos)

for line in maze:
	for c in line:
		write(c)
	write('\n')

write('Path cost: ' + str(retval[0]) + '\n')
write('Nodes expanded: ' + str(retval[1]))
#file.close()