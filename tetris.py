import pygame,sys
import random

#constants
columns=15
rows=30
cell=22

#define colours
colors = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35, 35 ) ]
#(189,183,107)]

#define the tetromino shapes
shapes=[
    [
        [1,1],
        [1,1]
    ],
    [
        [2,2,2],
        [0,2,0]
    ],
    [
       [3,3,3,3]
    ],
    [
        [4,0,0],
        [4,4,4]
    ],
    [
        [0,0,5],
        [5,5,5]
    ],
    [
        [6,6,0],
        [0,6,6]
    ],
    [
        [0,7,7],
        [7,7,0]
    ]
]

def new_board():
    board=[[0 for x in xrange(columns)] for y in xrange(rows)]
    board+=[[1 for x in xrange(columns)]]
    return board

def rotate(shape):
    return [[shape[y][x] for y in xrange(len(shape))] for x in xrange(len(shape[0])-1,-1,-1)]

def collision(board,shape,offset):
    x_off,y_off=offset
    for y,row in enumerate(shape):
        for x,col in enumerate(row):
            try:
                if col and board[y+y_off][x+x_off]:
                    return True
            except IndexError:
                return True

    return False

def delete_row(board,row):
    del board[row]
    return [[0 for i in xrange(columns)]] + board

def add_tetros(board,shape,offset):
    x_off,y_off=offset
    for y,row in enumerate(shape):
        for x,col in enumerate(row):
            board[y+y_off-1][x+x_off]+=col
    return board

class Tetris(object):
    def __init__(self):
        pygame.init()

        self.height=cell*rows
        self.width=cell*(columns+8)
        self.board_width=cell*columns
        self.grid=[[8 if x%2==y%2 else 0 for x in xrange(columns)] for y in xrange(rows)]

        self.window=pygame.display.set_mode((self.width,self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION) #block mouse motion events
        self.next_tetromino=shapes[random.randrange(len(shapes))]
        #start game
        self.start_game()

    def new_tetromino(self):
        self.tetromino=self.next_tetromino[:]
        self.next_tetromino=shapes[random.randrange(len(shapes))]
        self.x_tetro=int(columns/2-len(self.tetromino[0])/2)
        self.y_tetro=0


    def start_game(self):
        self.board=new_board()
        self.new_tetromino()

    def draw_matrix(self,matrix,offset):
        x_off,y_off=offset
        for y, row in enumerate(matrix):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(self.window,colors[col],((x_off+x)*cell,(y_off+y)*cell,cell,cell),0)

    def shift(self,unit):
        x_new=self.x_tetro+unit

        #handle collisions with left and right borders
        if x_new<0:
            x_new=0
        if x_new>columns-len(self.tetromino[0]):
            x_new=columns-len(self.tetromino[0])

        if not collision(self.board,self.tetromino,(x_new,self.y_tetro)):
            self.x_tetro=x_new

    def drop_tetro(self,down_key):
        self.y_tetro+=1

        #add tetromino to board when it reaches bottom
        if collision(self.board,self.tetromino,(self.x_tetro,self.y_tetro)):
            self.board=add_tetros(self.board,self.tetromino,(self.x_tetro,self.y_tetro))
            self.new_tetromino()

            #delete completed rows
            while True:
                for i,row in enumerate(self.board[:-1]):
                    if 0 not in row:
                        self.board=delete_row(self.board,i)
                        break
                break


    def rotate_tetromino(self):
        new_tetromino=rotate(self.tetromino)

        # TODO - return the offsets of rotated tetromino when changing the rotate function
        # The current rotate function is such that offsets remain same
        if not collision(self.board,new_tetromino,(self.x_tetro,self.y_tetro)):
            self.tetromino=new_tetromino

    def run(self):
        key_actions={
            'UP': self.rotate_tetromino,
            'LEFT': lambda:self.shift(-1),
            'RIGHT': lambda:self.shift(1),
            'DOWN': lambda:self.drop_tetro(True)

        }
        while 1:
            #window colour
            self.window.fill((0,0,0))

            #draw on the window
            pygame.draw.line(self.window,(255,255,255),(self.board_width+1,0),(self.board_width+1,self.height),1)
            self.draw_matrix(self.grid,(0,0))
            self.draw_matrix(self.board,(0,0))
            self.draw_matrix(self.tetromino,(self.x_tetro,self.y_tetro))
            self.draw_matrix(self.next_tetromino,(columns+2,3))

            #event handling
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key==eval("pygame.K_"+key):
                            key_actions[key]()

            #rendering
            pygame.display.update()

if __name__=='__main__':
    tetris=Tetris()
    tetris.run()
