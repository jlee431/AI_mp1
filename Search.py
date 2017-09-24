import sys
from Frontiers import *
from State import *

class State:

	def __init__(self, x = 0, y = 0, d = 0, el = [], p = None):
		self.x_pos = x
		self.y_pos = y
		self.dots_left = d
		self.eaten_list = el
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

	def __lt__(self, other):
		return self.calcHeuristic() < other.calcHeuristic()

	def __gt__(self, other):
		return self.calcHeuristic() > other.calcHeuristic()

	def __eq__(self, other):
		return self.calcHeuristic() == other.calcHeuristic()

actions = [(-1,0),(0,-1),(1,0),(0,1)]

def DoAction(state,action):
	new_x = state.x_pos + action[0]
	new_y = state.y_pos + action[1]

	char = maze[new_y][new_x]
	if(char == ' '):
		return State(new_x, new_y, state.dots_left, list(state.eaten_list), state)
	elif(char == '.'):
		l = list(state.eaten_list)
		i = dots.index((new_x, new_y))
		l[i] = True
		return State(new_x,new_y, state.dots_left - 1, l, state)
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

print('Player pos: ' + str(player_start_x) + ', ' + str(player_start_y))
print('Dot pos: ' + str(dots[0][0]) + ', ' + str(dots[0][1]))

prev_states = {}

# Add initial state
start_state = State(player_start_x, player_start_y, len(dots), [False]*len(dots))
frontier.addState(start_state)

# Start Search
while not frontier.isEmpty():
	# Get the next state
	current_state = frontier.getState()

	# Check if current state is goal state
	if(not current_state.dots_left):
		while current_state:
			maze[current_state.y_pos][current_state.x_pos] = '.'
			current_state = current_state.parent
		break

	# Check for repeated state
	if(current_state.toString() in prev_states):
		continue

	# Expand current state
	prev_states[current_state.toString()] = True

	# Check all four directions
	for a in actions:
		new_state = DoAction(current_state, a)
		if(new_state is not None):
			frontier.addState(new_state)

for line in maze:
	for c in line:
		sys.stdout.write(c)
	print('')

