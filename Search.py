import sys
import string
from Frontiers import *

class State:
	compareFunc = 0
	heuristic = 0
	num_dots = 0

	def __init__(self, x, y, d, el, pc = 0, p = None):
		self.x_pos = x
		self.y_pos = y
		self.dots_left = d
		self.eaten_list = el
		self.path_cost = pc
		self.parent = p

		self.calcHeuristic()
		self.id = str(x) + ' ' + str(y) + ' ' + str.join('', map(lambda x: str(x[0]), el))

	def calcHeuristic(self):
		if(State.heuristic == 0):
			x_dist = abs(self.eaten_list[0][1][0] - self.x_pos)
			y_dist = abs(self.eaten_list[1][1][1] - self.y_pos)
			self.heuristic =  x_dist + y_dist
		elif(State.heuristic == 1):
			min_dist = len(maze) + len(maze[0])
			for pair in self.eaten_list:
				if(pair[0]):
					x_dist = abs(pair[1][0] - self.x_pos)
					y_dist = abs(pair[1][1] - self.y_pos)
					if(x_dist + y_dist < min_dist):
						min_dist = x_dist + y_dist
			self.heuristic =  min_dist
		elif(State.heuristic == 2):
			self.heuristic =  self.dots_left
		elif(State.heuristic == 3):
			min_dist = len(maze) + len(maze[0])
			for pair in self.eaten_list:
				if(pair[0]):
					x_dist = abs(pair[1][0] - self.x_pos)
					y_dist = abs(dot[1][1] - self.y_pos)
					if(x_dist + y_dist < min_dist):
						min_dist = x_dist + y_dist
			self.heuristic =  self.dots_left + min_dist - 1
		else:
			min_dist = len(maze) + len(maze[0])
			for pair in self.eaten_list:
				if(pair[0]):
					x_dist = abs(pair[1][0] - self.x_pos)
					y_dist = abs(pair[1][1] - self.y_pos)
					if(x_dist + y_dist < min_dist):
						min_dist = x_dist + y_dist
			self.heuristic =  (self.dots_left * min_dist) / State.num_dots

	def calcEvalFunc(self):
		return self.heuristic + self.path_cost

	def isGoal(self):
		if(self.dots_left):
			return False
		return True;

	def __lt__(self, other):
		if State.compareFunc:
			return self.calcEvalFunc() < other.calcEvalFunc()
		else:
			return self.heuristic < other.heuristic

	def __gt__(self, other):
		if State.compareFunc:
			return self.calcEvalFunc() > other.calcEvalFunc()
		else:
			return self.heuristic > other.heuristic

	def __eq__(self, other):
		return self.id == other.id

actions = [(-1,0),(0,-1),(1,0),(0,1)]

def DoActions(state, actionList):
	stateList = []
	
	for action in actionList:
		new_x = state.x_pos + action[0]
		new_y = state.y_pos + action[1]

		char = maze[new_y][new_x]
		if(char == ' ' or char == 'P'):
			stateList.append(State(new_x, new_y, state.dots_left, state.eaten_list.copy(), state.path_cost + 1, state))
		elif(char == '.'):
			elist = state.eaten_list.copy()
			dots_left = state.dots_left
			for i in range(num_dots):
				if(elist[i][1][0] == new_x and elist[i][1][1] == new_y):
					elist[i] = (0, (new_x, new_y))
					break
			stateList.append(State(new_x,new_y, dots_left, elist, state.path_cost + 1, state))
	
	return stateList

if(len(sys.argv) !=3):
	print("USAGE: Search.py mazefile search")
	sys.exit()

maze_file = open(sys.argv[1], 'r')

maze = []
for line in maze_file:
	maze.append(list(line)[:len(line)-1])

option = sys.argv[2].lower()

if(option == 'dfs'):
	frontier = FrontierDFS()
elif(option == 'bfs'):
	frontier = FrontierBFS()
elif(option == 'greedy'):
	frontier = FrontierGreedy()
	State.compareFunc = 0
elif(option == 'a*'):
	frontier = FrontierAStar()
	State.compareFunc = 1
else:
	print("Unrecognized search: " + option)
	sys.exit()

write = sys.stdout.write
for line in maze:
	for c in line:
		write(c)
	print('')

ans = string.digits + string.ascii_letters 

num_dots = 0
dots = []
y_pos = 0
x_pos = 0
for row in range(len(maze)):
	for col in range(len(maze[row])):
		if(maze[row][col] == '.'):
			dots.append((1, (col, row)))
			num_dots = num_dots + 1
		elif(maze[row][col] == 'P'):
			y_pos = row
			x_pos = col

start_state = State(x_pos, y_pos, num_dots, dots)

# Set heuristic
if(start_state.dots_left > 1):
	State.heuristic = 1
	State.num_dots = num_dots

# Add initial state
frontier.addState(start_state)
nodes_expanded = 0
path_cost = 0

# Common functions:
getState = frontier.getState
isEmpty = frontier.isEmpty
addState = frontier.addState

# Start Search
while not isEmpty():
	# Get the next state
	current_state = getState()

	# Check if current state is goal state
	if(current_state.isGoal()):
		path_cost = current_state.path_cost
		target = start_state.dots_left - 1

		while current_state:
			if(start_state.dots_left == 1):
				maze[current_state.y_pos][current_state.x_pos] = '.'
			elif(maze[current_state.y_pos][current_state.x_pos] == '.'):
				maze[current_state.y_pos][current_state.x_pos] = ans[target]
				target = target - 1

			current_state = current_state.parent
		break

	# Update expanded state counter
	nodes_expanded = nodes_expanded + 1

	# Check all four directions:
	new_states = DoActions(current_state, actions)
	for state in new_states:
		addState(state)

for line in maze:
	for c in line:
		write(c)
	print('')

print('Path cost: ' + str(path_cost))
print('Nodes expanded: ' + str(nodes_expanded))