import sys

if(len(sys.argv) !=2):
	print("USAGE: Search.py mazefile")

class State:
	x_pos = 0
	y_pos = 0
	dots_left = 0
	eaten_list = []
	parent = None

	def __init__(self, x = 0, y = 0, d = 0, el = [], p = None):
		self.x_pos = x
		self.y_pos = y
		self.dots_left = d
		self.eaten_list = el
		self.parent = p

mazeFile = open(sys.argv[1], 'r')

maze = []
for line in mazeFile:
	maze.append(list(line)[:len(line)-1])

for line in maze:
	for c in line:
		sys.stdout.write(c)
	print('')

second = State(4)
first = State(0,0,0,0,second)
print(first.parent.x_pos)
