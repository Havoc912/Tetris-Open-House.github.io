import pygame
import random

pygame.font.init()

# Variables
swidth = 800
sheight = 700
pwidth = 300  # 300 / 10 = 30 width per block
pheight = 600  # 600 / 20 = 30 height per block
blocksize = 30

topleftx = (swidth - pwidth) // 2  # Top left play area
toplefty = sheight - pheight  # Top left play area

# SHAPES
S = [['.....',
       '.....',
       '..00.',
       '.00..',
       '.....'],
      ['.....',
       '..0..',
       '..00.',
       '...0.',
       '.....']]

Z = [['.....',
       '.....',
       '...00',
       '..00.',
       '.....'],
      ['.....',
       '..0..',
       '..00.',
       '...0.']]

I = [['..0..',
       '..0..',
       '..0..',
       '..0..',
       '.....'],
      ['.....',
       '0000.',
       '.....',
       '.....',
       '.....']]

O = [['.....',
       '.....',
       '.00..',
       '.00..',
       '.....']]

J = [['.....',
       '.0...',
       '.000.',
       '.....',
       '.....'],
       ['.....',
        '..00.',
        '..0..',
        '..0..',
        '.....'],
       ['.....',
        '.....',
        '.000.',
        '...0.',
        '.....'],
       ['.....',
        '..0..',
        '..0..',
        '.00..',
        '.....']]

L = [['.....',
        '...0.',
        '.000.',
        '.....',
        '.....'],
       ['.....',
        '..0..',
        '..0..',
        '..00.',
        '.....'],
       ['.....',
        '.....',
        '.000.',
        '.0...',
        '.....'],
       ['.....',
        '.00..',
        '..0..',
        '..0..',
        '.....']]

T = [['.....',
        '..0..',
        '.000.',
        '.....',
        '.....'],
       ['.....',
        '..0..',
        '..00.',
        '..0..',
        '.....'],
       ['.....',
        '.....',
        '.000.',
        '..0..',
        '.....'],
       ['.....',
       '..0..',
       '.00..',
       '..0..',
       '.....']]

shapes = [S, Z, I, O, J, L, T]
shapecolours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# index 0 - 6 represent shapes

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.colour = shapecolours[shapes.index(shape)]  # Colour is relevant to shape
        self.rotation = 0  # Defaulted to '0'
def create_grid(locked_pos=()):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]  # makes grid 10 X 20
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c  # Checks if block in lock_pos is already there
    return grid

def convert_shape_format(shape):
    positions = []
    format= shape.shape[(shape.rotation+1) % len(shape.shape)]#If the rotation=0, remainder = 0. If the rotation = 1, remainder = 1. If  the rotation = 4, the remainder = 0
    for i, line in enumerate(format): #keeps track of the number of iterations(loops) in a loop
        row = list(line)
        for j, column in enumerate(row):# loops through each line in a list and see if it is a period or a 0
            if column  == '0':
                positions.append((shape.x + j, shape.y+i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions
def get_shape():
    return Piece(5, 0,random.choice(shapes))


def draw_grid(surface, grid):
  sx = topleftx
  sy = toplefty
  for i in range (len(grid)):
    pygame.draw.line(surface, (128,128,128),(sx,sy+i*blocksize),(sx+pwidth, sy+i*blocksize))
    for j in range (len(grid[i])):
        pygame.draw.line(surface, (128,128,128),(sx + j*blocksize,sy),(sx+j*blocksize, sy+pheight))#Draws lines

def clear_rows(board, locked_positions):
    completed_rows = []
    for row in range(len(board)):
        if all(cell != (0, 0, 0) for cell in board[row]):
            completed_rows.append(row)

    for row in completed_rows:
        del board[row]
        board.insert(0, [(0, 0, 0)] * 10)

    # Update locked_positions
    for row in completed_rows:
        for col in range(10):
            del locked_positions[(col, row)]
            for above_row in range(row - 1, -1, -1):
                if (col, above_row) in locked_positions:
                    locked_positions[(col, above_row + 1)] = locked_positions[(col, above_row)]
                    del locked_positions[(col, above_row)]

def draw_next_shape(shape,surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('NEXT SHAPE', 1, (255, 255, 255))

    sx= topleftx + pwidth + 50
    sy=toplefty + pheight//2 - 100
    shapeformat= shape.shape[(shape.rotation+1) % len(shape.shape)]

    for i, line in enumerate(shapeformat):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.colour, (sx + j *blocksize, sy+i*blocksize, blocksize, blocksize),0)
        surface.blit(label,(sx + 10, sy- 30))



def draw_window(surface, grid):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (topleftx + pwidth // 2 - (label.get_width() // 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, (255, 255, 255) if grid[i][j] == (0, 0, 0) else grid[i][j],
                             (topleftx + j * blocksize, toplefty + i * blocksize, blocksize, blocksize))

    draw_grid(surface, grid)  # Draw the grid lines

    pygame.draw.rect(surface, (255, 0, 0), (topleftx, toplefty, pwidth, pheight), 4)

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    shape_format = convert_shape_format(shape)
    for pos in shape_format:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def main(win):
    locked_positions = {}  # Blank dictionary
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.colour

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.colour
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            clear_rows(grid, locked_positions)
            #draw_next_shape(next_piece,grid)

        draw_window(win, grid)
        pygame.display.update()  # Update the display after drawing

        if check_lost(locked_positions):
            run = False


def main_menu(win):
    main(win)


win = pygame.display.set_mode((swidth, sheight))
pygame.display.set_caption('Tetris')
main_menu(win)
