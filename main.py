import pygame
pygame.init()
WIDTH = 750
screen = pygame.display.set_mode((WIDTH, WIDTH))
WHITE = (255, 255, 255)
RED =   (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CYAN = (216, 191, 216)
SIZE = 10
queue = []
di = [0,0,1,-1,1,-1,-1,1]
dj = [1,-1,0,0,1,-1,1,-1]
click_start = 0
click_end = 0

class Node():
    def __init__(self, row, col, width):
        self.map = 0
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.color = WHITE
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def blocked(self):
        return self.color == BLACK
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

def make_Grid(rows, width):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range (rows):
            node = Node(i, j, SIZE)
            grid[i].append(node)
    return grid

def draw(screen,grid, rows, width):
    screen.fill(WHITE)
    for row in grid:
        for Node in row:
            Node.draw()

def mouse_pos():
    global click_start
    global click_end
    x, y = pygame.mouse.get_pos()
    x = x // SIZE
    y = y // SIZE
    if  click_start == 0 and grid[x][y].color == WHITE:
         click_start = pygame.mouse.get_pos()
         grid[x][y].color = GREEN
         grid[x][y].draw()
    elif click_end == 0 and grid[x][y].color == WHITE:
        click_end = pygame.mouse.get_pos()
        grid[x][y].color = RED
        grid[x][y].draw()
    elif grid[x][y].color == GREEN:
        click_start = 0
        grid[x][y].color = WHITE
        grid[x][y].draw()
    elif grid[x][y].color == RED:
        click_end = 0
        grid[x][y].color = WHITE
        grid[x][y].draw()
    else:
        grid[x][y].color = BLACK
        grid[x][y].draw()
    pygame.display.update()

def Inside(x, y):
    return x < 75 and y < 75 and x >= 0 and y >= 0

grid = make_Grid(75,SIZE)
draw(screen,grid,75,SIZE)

def Dijkstra(startx, starty):
    grid[startx][starty].map = 1
    grid[startx][starty].color = GREEN
    grid[startx][starty].draw()
    queue.append((startx,starty))

    while len(queue) > 0:
        i = queue[0][0]
        j = queue[0][1]
        queue.pop(0)
        if i == click_end[0] // SIZE and j == click_end[1] // SIZE:
            return None
        for d in range(4):
           i_next = i + di[d]
           j_next = j + dj[d]

           if Inside(i_next,j_next) and (grid[i_next][j_next].color == WHITE or grid[i_next][j_next].color == RED):
                 grid[i_next][j_next].map = grid[i][j].map + 1
                 queue.append((i_next, j_next))
                 if(grid[i_next][j_next].color == WHITE):
                     grid[i_next][j_next].color = CYAN

                 grid[i_next][j_next].draw()
        pygame.display.update()

def Backtracking(startx, starty):

    grid[startx][starty].color = RED
    grid[startx][starty].draw()
    queue.clear()
    queue.append((startx, starty))
    print(startx, starty)
    while len(queue) > 0:
        i = queue[0][0]
        j = queue[0][1]
        queue.pop(0)
        for d in range(4):
           i_next = i + di[d]
           j_next = j + dj[d]

           if Inside(i_next,j_next) and grid[i_next][j_next].map == grid[i][j].map - 1:
                 queue.append((i_next, j_next))
                 grid[i_next][j_next].color = RED
                 grid[i_next][j_next].draw()
                 break
        pygame.time.Clock().tick(20)
        pygame.display.update()

def Afisare():
    for i in range(20):
        for j in range(20):
            print(grid[i][j].map, end =" ")
        print("\n")
pygame.display.update()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0]:
            mouse_pos()
        if event.type == pygame.KEYDOWN:
             if (event.key == pygame.K_SPACE):
                  Dijkstra(click_start[0] // SIZE, click_start[1] // SIZE)
                 # Afisare()
                  Backtracking(click_end[0] // SIZE, click_end[1] // SIZE)
    #print(click_start)