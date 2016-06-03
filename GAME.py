import pygame
import sys
from pygame.locals import *
import random

WINDOW_WIDTH = 660
WINDOW_HEIGHT = 660
CELL_SIZE = 10

FPS = 20

TURQUISE  = (64, 224, 208)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
NAVY = (0, 0, 128)
OLIVE_DRAB = (107, 142, 35)
RED = (255, 0, 0)

assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size"
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size"

NR_CELL_WIDTH = WINDOW_WIDTH / CELL_SIZE  # number of cells wide
NR_CELL_HEIGHT = WINDOW_HEIGHT / CELL_SIZE - 6  # Number of cells high


def drawGrid(display):
	for x in range(0, WINDOW_WIDTH, CELL_SIZE):  # draw vertical lines
		pygame.draw.line(display, NAVY, (x, 0), (x, WINDOW_HEIGHT - 30))
	for y in range(0, WINDOW_HEIGHT - 25, CELL_SIZE):  # draw horizontal lines
		pygame.draw.line(display, NAVY, (0, y), (WINDOW_WIDTH, y))

def blankGrid():
	gridDict = {}
	for y in range (NR_CELL_HEIGHT):
		for x in range (NR_CELL_WIDTH):
			gridDict[x,y] = 0
	return gridDict

def GridRandom(lifeDict):
	for item in lifeDict:
		lifeDict[item] = random.randint(0,1)
	return lifeDict

def ClearGrid(lifeDict):
	for item in lifeDict:
		lifeDict[item] = 0
	return lifeDict

#Colours the cells black for life and turquise for no life
def colourGrid(display, item, lifeDict):
	x = item[0]
	y = item[1]
	y = y * CELL_SIZE # translates array into grid size
	x = x * CELL_SIZE # translates array into grid size
	if lifeDict[item] == 0:
		pygame.draw.rect(display, TURQUISE, (x, y, CELL_SIZE, CELL_SIZE))
	if lifeDict[item] == 1:
		pygame.draw.rect(display, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
	return None

#Determines how many alive neighbours there are around each cell
def getNeighbours(item, lifeDict):
	neighbours = 0
	for x in range (-1, 2):
		for y in range (-1, 2):
			checkCell = (item[0] + x, item[1] + y)
			if checkCell[0] < NR_CELL_WIDTH  and checkCell[0] >= 0:
				if checkCell [1] < NR_CELL_HEIGHT and checkCell[1] >= 0:
					if lifeDict[checkCell] == 1:
						if x == 0 and y == 0: # negate the central cell
							neighbours += 0
						else:
							neighbours += 1
	return neighbours

#determines the next generation by running a 'tick'
def tick(lifeDict):
	newTick = {}
	for item in lifeDict:
		#get number of neighbours for that item
		numberNeighbours = getNeighbours(item, lifeDict)
		if lifeDict[item] == 1: # For those cells already alive
			if numberNeighbours < 2: # kill under-population
				newTick[item] = 0
			elif numberNeighbours > 3: #kill over-population
				newTick[item] = 0
			else:
				newTick[item] = 1 # keep status quo (life)
		elif lifeDict[item] == 0:
			if numberNeighbours == 3: # cell reproduces
				newTick[item] = 1
			else:
				newTick[item] = 0 # keep status quo (death)
	return newTick

def R_pentomino(lifeDict):
	#R-pentomino
	lifeDict[48,32] = 1
	lifeDict[49,32] = 1
	lifeDict[47,33] = 1
	lifeDict[48,33] = 1
	lifeDict[48,34] = 1
	return lifeDict

def Acorn(lifeDict):
	#Acorn
	lifeDict[105,55] = 1
	lifeDict[106,55] = 1
	lifeDict[109,55] = 1
	lifeDict[110,55] = 1
	lifeDict[111,55] = 1
	lifeDict[106,53] = 1
	lifeDict[108,54] = 1
	return lifeDict

def Diehard(lifeDict):
	#Diehard
	lifeDict[45,45] = 1
	lifeDict[46,45] = 1
	lifeDict[46,46] = 1
	lifeDict[50,46] = 1
	lifeDict[51,46] = 1
	lifeDict[52,46] = 1
	lifeDict[51,44] = 1
	return lifeDict

def text_objects(text, font):
	textSurface = font.render(text, True, WHITE)
	return textSurface, textSurface.get_rect()

def buttons(display, message, lifeDict):
	if message == 'Clear':
		print 'Clear'
		lifeDict = ClearGrid(lifeDict)
	if message == 'Diehard':
		print 'Diehard'
		lifeDict = Diehard(lifeDict)
	elif message == 'Acorn':
		print 'acorn'
		lifeDict == Acorn(lifeDict)
	elif message == 'R-pentomino':
		print 'R-pentomino'
		lifeDict = R_pentomino(lifeDict)
	elif message == 'Random':
		print 'Random'
		lifeDict = GridRandom(lifeDict)

def button(display, msg, x, y, w, h, i_color, a_color, lifeDict):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(display, a_color, (x, y, w, h))
		if click == (1, 0, 0):
			buttons(display, msg, lifeDict)
	else:
		pygame.draw.rect(display, i_color, (x, y, w, h))

	smallText = pygame.font.Font("freesansbold.ttf",15)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ( (x + (w / 2)), (y + (h / 2)) )
	display.blit(textSurf, textRect)

def main():
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption('Conways Game of Life')
	display.fill(TURQUISE)

	lifeDict = blankGrid()

	#Colours the live cells, blanks the dead
	for item in lifeDict:
		colourGrid(display, item, lifeDict)

	drawGrid(display)
	pygame.display.update()

	while True:  # MAIN LOOP of the game
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		#runs a tick
		button(display, 'Clear', 10, 630, 70, 20, RED, BLACK, lifeDict)
		button(display, 'Diehard', 130, 630, 80, 20, NAVY, OLIVE_DRAB, lifeDict)
		button(display, 'Acorn', 260, 630, 80, 20, NAVY, OLIVE_DRAB, lifeDict)
		button(display, 'R-pentomino', 400, 630, 100, 20, NAVY, OLIVE_DRAB, lifeDict)
		button(display, 'Random', 540, 630, 70, 20, NAVY, OLIVE_DRAB, lifeDict)
		lifeDict = tick(lifeDict)

		#Colours the live cells, blanks the dead
		for item in lifeDict:
			colourGrid(display, item, lifeDict)

		drawGrid(display)


		pygame.display.update()
		FPSCLOCK.tick(FPS)

if __name__ == '__main__':
	main()