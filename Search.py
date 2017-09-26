import sys
import string
from Frontiers import *

class State:
	compareFunc = 0
	heuristic = 0

	def __init__(self, x = 0, y = 0, d = 0, el = {}, pc = 0, p = None):
		self.x_pos = x
		self.y_pos = y
		self.dots_left = d
		self.eaten_list = el
		self.path_cost = pc
		self.parent = p

	def toString(self):
		s = str(self.x_pos) + ' ' + str(self.y_pos) + ' '
		for key, value in self.eaten_list:
			if(value == True):
				s = s + '1'
			else:
				s = s + '0'
		return s

	def calcHeuristic(self):
		if(State.heuristic == 0):
			x_dist = abs(eaten_list.keys()[0][0] - self.x_pos)
			y_dist = abs(eaten_list.keys()[0][1] - self.y_pos)
			return x_dist + y_dist
		elif(State.heuristic == 1):
			min_dist = len(maze) + len(maze[0])
			for dot in eaten_list.keys():
				x_dist = abs(dot[0] - self.x_pos)
				y_dist = abs(dot[1] - self.y_pos)
				if(x_dist + y_dist < min_dist):
					min_dist = x_dist + y_dist
			return min_dist
		else:
			return self.dots_left

	def calcEvalFunc(self):
		return self.calcHeuristic() + self.path_cost

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
			return self.calcHeuristic() > other.calcHeuristic()

	def __eq__(self, other):
		if State.compareFunc:
			return self.calcEvalFunc() == other.calcEvalFunc()
		else:
			return self.calcHeuristic() == other.calcHeuristic()

actions = [(-1,0),(0,-1),(1,0),(0,1)]

def DoAction(state,action):
	new_x = state.x_pos + action[0]
	new_y = state.y_pos + action[1]

	char = maze[new_y][new_x]
	if(char == ' ' or char == 'P'):
		return State(new_x, new_y, state.dots_left, state.eaten_list.copy(), state.path_cost + 1, state)
	elif(char == '.'):
		dic = state.eaten_list.copy()
		dots_left = state.dots_left
		if(not dic[(new_x, new_y)]):
			dots_left = dots_left - 1
			dic[(new_x, new_y)] = True
		return State(new_x,new_y, dots_left, dic, state.path_cost + 1, state)
	return None

if(len(sys.argv) !=3):
	print("USAGE: Search.py mazefile search")
	sys.exit()

maze_file = open(sys.argv[1], 'r')

maze = []
for line in maze_file:
	maze.append(list(line)[:len(line)-1])

if(sys.argv[2].lower() == 'dfs'):
	frontier = FrontierDFS()
elif(sys.argv[2].lower() == 'bfs'):
	frontier = FrontierBFS()
elif(sys.argv[2].lower() == 'greedy'):
	frontier = FrontierGreedy()
	State.compareFunc = 0
elif(sys.argv[2].lower() == 'a*'):
	frontier = FrontierAStar()
	State.compareFunc = 1
else:
	print("Unrecognized search: " + sys.argv[2])
	sys.exit()

for line in maze:
	for c in line:
		sys.stdout.write(c)
	print('')

ans = string.digits + string.ascii_letters 

start_state = State()

for row in range(len(maze)):
	for col in range(len(maze[row])):
		if(maze[row][col] == '.'):
			start_state.eaten_list[(col, row)] = False
			start_state.dots_left = start_state.dots_left + 1
		elif(maze[row][col] == 'P'):
			start_state.y_pos = row
			start_state.x_pos = col

print("Dots left: " + str(start_state.dots_left))
for d in start_state.eaten_list.keys():
	print("Dot: " + str(d))
print("Start state: " + start_state.toString())

# Set heuristic
if(start_state.dots_left > 1):
	State.heuristic = 2

# Add initial state
frontier.addState(start_state)
nodes_expanded = 0
path_cost = 0

# Start Search
while not frontier.isEmpty():
	# Get the next state
	current_state = frontier.getState()

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

	# Check all four directions
	for a in actions:
		new_state = DoAction(current_state, a)
		if(new_state is not None):
			frontier.addState(new_state)

for line in maze:
	for c in line:
		sys.stdout.write(c)
	print('')

print('Path cost: ' + str(path_cost))
print('Nodes expanded: ' + str(nodes_expanded))