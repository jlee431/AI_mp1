import sys
from Frontiers import *

class State:
	compareFunc = 0

	def __init__(self, x = 0, y = 0, d = 0, el = [], pc = 0, p = None):
		self.x_pos = x
		self.y_pos = y
		self.dots_left = d
		self.eaten_list = el
		self.path_cost = pc
		self.parent = p

	def toString(self):
		s = str(self.x_pos) + str(self.y_pos)
		for e in self.eaten_list:
			if(e):
				s = s + '1'
			else:
				s = s + '0'
		return s

	def calcHeuristic(self):
		x_dist = abs(dots[0][0] - self.x_pos)
		y_dist = abs(dots[0][1] - self.y_pos)
		return x_dist + y_dist

	def calcEvalFunc(self):
		return self.calcHeuristic() + self.path_cost

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
	if(char == ' '):
		return State(new_x, new_y, state.dots_left, list(state.eaten_list), state.path_cost + 1, state)
	elif(char == '.'):
		l = list(state.eaten_list)
		i = dots.index((new_x, new_y))
		l[i] = True
		return State(new_x,new_y, state.dots_left - 1, l, state.path_cost + 1, state)
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

dots = []
player_start_x = 0
player_start_y = 0

for row in range(len(maze)):
	for col in range(len(maze[row])):
		if(maze[row][col] == '.'):
			dots.append((col, row)) 
		elif(maze[row][col] == 'P'):
			player_start_y = row
			player_start_x = col

print('Dot location: ' + str(dots[0][0]) + ', ' + str(dots[0][1]))

# Add initial state
start_state = State(player_start_x, player_start_y, len(dots), [False]*len(dots))
frontier.addState(start_state)
nodes_expanded = 0

# Start Search
while not frontier.isEmpty():
	# Get the next state
	current_state = frontier.getState()
	if(150 == current_state.path_cost):
		print('X: ' + str(current_state.x_pos) + '  Y: ' + str(current_state.y_pos))

	# Check if current state is goal state
	if(not current_state.dots_left):
		path_cost = current_state.path_cost
		n = 0
		while current_state:
			#if(maze[current_state.y_pos][current_state.x_pos] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
			#	maze[current_state.y_pos][current_state.x_pos] = '.'
			maze[current_state.y_pos][current_state.x_pos] = str(n)
			n = (n + 1) % 10
			current_state = current_state.parent
		break

	ch = maze[current_state.y_pos][current_state.x_pos]
	maze[current_state.y_pos][current_state.x_pos] = 'P'
	for line in maze:
		for c in line:
			sys.stdout.write(c)
		print('')

	input()

	# Update expanded state counter
	nodes_expanded = nodes_expanded + 1

	# Check all four directions
	for a in actions:
		new_state = DoAction(current_state, a)
		if(new_state is not None):
			'''if(new_state.path_cost == 150):
				s = new_state
				for i in range(9):
					maze[s.y_pos][s.x_pos] = str(i)
					s = s.parent'''
			frontier.addState(new_state)

	maze[current_state.y_pos][current_state.x_pos] = ch

for line in maze:
	for c in line:
		sys.stdout.write(c)
	print('')

print('Path cost: ' + str(path_cost))
print('Nodes expanded: ' + str(nodes_expanded))

#frontier.dump()