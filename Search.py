import sys

if(len(sys.argv) !=2):
	print("USAGE: Search.py mazefile")



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

def IsInFrontier(frontier, state):
	for i in frontier:
		if (state.toString() == i.toString()):
			return True
	return False


maze_file = open(sys.argv[1], 'r')

maze = []
for line in maze_file:
	maze.append(list(line)[:len(line)-1])

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


frontier = []
prev_states = {}

# Add initial state

frontier.append(State(player_start_x, player_start_y, len(dots), [False]*len(dots)))

# Start Search

while frontier:
	# Get the next state
	current_state = frontier.pop()

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
	char = maze[current_state.y_pos-1][current_state.x_pos]
	if(char == ' '):
		new_state = State(current_state.x_pos, current_state.y_pos - 1, current_state.dots_left, list(current_state.eaten_list), current_state)
		if(not(IsInFrontier(frontier, new_state))):
			frontier.append(new_state)
	elif(char == '.'):
		l = list(current_state.eaten_list)
		i = dots.index((current_state.x_pos, current_state.y_pos - 1))
		l[i] = True
		new_state = State(current_state.x_pos, current_state.y_pos - 1, current_state.dots_left - 1, l, current_state)
		if(not IsInFrontier(frontier, new_state)):
			frontier.append(new_state)

	char = maze[current_state.y_pos][current_state.x_pos + 1]
	if(char == ' '):
		new_state = State(current_state.x_pos + 1, current_state.y_pos, current_state.dots_left, list(current_state.eaten_list), current_state)
		if(not IsInFrontier(frontier, new_state)):
			frontier.append(new_state)
	elif(char == '.'):
		l = list(current_state.eaten_list)
		i = dots.index((current_state.x_pos + 1, current_state.y_pos))
		l[i] = True
		new_state = State(current_state.x_pos + 1, current_state.y_pos, current_state.dots_left - 1, l, current_state)
		if(not IsInFrontier(frontier, new_state)):
			frontier.append(new_state)

	char = maze[current_state.y_pos + 1][current_state.x_pos]
	if(char == ' '):
		new_state = State(current_state.x_pos, current_state.y_pos + 1, current_state.dots_left, list(current_state.eaten_list), current_state)
		if(not IsInFrontier(frontier, new_state)):	
			frontier.append(new_state)
	elif(char == '.'):
		l = list(current_state.eaten_list)
		i = dots.index((current_state.x_pos, current_state.y_pos + 1))
		l[i] = True
		new_state = State(current_state.x_pos, current_state.y_pos + 1, current_state.dots_left - 1, l, current_state)
		if(not IsInFrontier(frontier, new_state)):
			frontier.append(new_state)

	char = maze[current_state.y_pos][current_state.x_pos - 1]
	if(char == ' '):
		new_state = State(current_state.x_pos - 1, current_state.y_pos, current_state.dots_left, list(current_state.eaten_list), current_state)
		if(not IsInFrontier(frontier,new_state)):
			frontier.append(new_state)
	elif(char == '.'):
		l = list(current_state.eaten_list)
		i = dots.index((current_state.x_pos - 1, current_state.y_pos))
		l[i] = True
		new_state = State(current_state.x_pos - 1, current_state.y_pos, current_state.dots_left - 1, l, current_state)
		if(not IsInFrontier(frontier,new_state)):
			frontier.append(new_state)

for line in maze:
	for c in line:
		sys.stdout.write(c)
	print('')

print("\n\n\n" + "BFS Search \n")

maze_file = open(sys.argv[1], 'r')
maze = []
for line in maze_file:
	maze.append(list(line)[:len(line)-1])

frontier = []
prev_states = {}

# Add initial state

frontier.append(State(player_start_x, player_start_y, len(dots), [False]*len(dots)))

# BFS Search
while frontier:
	# Get the next state
	current_state = frontier.pop(0)

	# Check if current state is goal state
	if(not current_state.dots_left):
		print("Goal Found!!!")
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
	char = maze[current_state.y_pos-1][current_state.x_pos]
	if(char == ' '):
		new_state = State(current_state.x_pos, current_state.y_pos - 1, current_state.dots_left, list(current_state.eaten_list), current_state)
		if(not IsInFrontier(frontier, new_state)):
			frontier.append(new_state)
	elif(char == '.'):
		l = list(current_state.eaten_list)
		i = dots.index((current_state.x_pos, current_state.y_pos - 1))
		l[i] = True
		new_state = State(current_state.x_pos, current_state.y_pos - 1, current_state.dots_left - 1, l, current_state)
		if(not IsInFrontier(frontier, new_state)):
			frontier.append(new_state)

	char = maze[current_state.y_pos][current_state.x_pos + 1]
	if(char == ' '):
		new_state = State(current_state.x_pos + 1, current_state.y_pos, current_state.dots_left, list(current_state.eaten_list), current_state)
		if(not IsInFrontier(frontier, new_state)):
			frontier.append(new_state)
	elif(char == '.'):
		l = list(current_state.eaten_list)
		i = dots.index((current_state.x_pos + 1, current_state.y_pos))
		l[i] = True
		new_state = State(current_state.x_pos + 1, current_state.y_pos, current_state.dots_left - 1, l, current_state)
		if(not IsInFrontier(frontier, new_state)):
			frontier.append(new_state)

	char = maze[current_state.y_pos + 1][current_state.x_pos]
	if(char == ' '):
		new_state = State(current_state.x_pos, current_state.y_pos + 1, current_state.dots_left, list(current_state.eaten_list), current_state)
		if(not IsInFrontier(frontier, new_state)):	
			frontier.append(new_state)
	elif(char == '.'):
		l = list(current_state.eaten_list)
		i = dots.index((current_state.x_pos, current_state.y_pos + 1))
		l[i] = True
		new_state = State(current_state.x_pos, current_state.y_pos + 1, current_state.dots_left - 1, l, current_state)
		if(not IsInFrontier(frontier, new_state)):
			frontier.append(new_state)

	char = maze[current_state.y_pos][current_state.x_pos - 1]
	if(char == ' '):
		new_state = State(current_state.x_pos - 1, current_state.y_pos, current_state.dots_left, list(current_state.eaten_list), current_state)
		if(not IsInFrontier(frontier,new_state)):
			frontier.append(new_state)
	elif(char == '.'):
		l = list(current_state.eaten_list)
		i = dots.index((current_state.x_pos - 1, current_state.y_pos))
		l[i] = True
		new_state = State(current_state.x_pos - 1, current_state.y_pos, current_state.dots_left - 1, l, current_state)
		if(not IsInFrontier(frontier, new_state)):
			frontier.append(new_state)

for line in maze:
	for c in line:
		sys.stdout.write(c)
	print('')
