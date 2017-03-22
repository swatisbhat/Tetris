import pygame,sys
import random

#constants
cols=15
rows=30
cell=22

#define colours
colors = [
(0,0,0 ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(240,  230, 140 ),
(189,183,107)]

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
    board=[[0 for x in xrange(cols)] for y in xrange(rows)]
    board+=[[1 for x in xrange(cols)]]
    return board

def rotate(shape):
    return [[shape[y][x] for y in xrange(len(shape))] for x in xrange(len(shape[0])-1,-1,-1)

class Tetris(object):
    def __init__(self):
        pygame.init()
        
        self.height=cell*rows
        self.width=cell*(cols+8)
        self.board_width=cell*cols
        self.grid=[[8 if x%2==y%2 else 9 for x in xrange(cols)] for y in xrange(rows)]
        
        self.window=pygame.display.set_mode((self.width,self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION) #block mouse motion events
        
        self.next_tetromino=shapes[random.randrange(len(shapes))]
        #start game
        self.start_game()
            
    def new_tetromino(self):
        self.tetromino=self.next_tetromino[:]
        self.next_tetromino=shapes[random.randrange(len(shapes))]
        self.x_tetro=int(cols/2-len(self.tetromino[0])/2)
        self.y_tetro=0
            
            
    def start_game(self):
        #self.board=new_board()
        self.new_tetromino()
            

      
    def draw_matrix(self,matrix,offset):
        x_off,y_off=offset
        for y, row in enumerate(matrix):
            for x, col in enumerate(row):
                pygame.draw.rect(self.window,colors[col],((x_off+x)*cell,(y_off+y)*cell,cell,cell),0)
            
    def rotate_tetromino(self):
        self.tetromino=rotate(self.tetromino)
        
    def run(self):
        key_actions={
        'UP': self.rotate_tetromino
        }
        while 1:
            #window colour
            self.window.fill((0,0,0))
        
            #draw on the window
            self.draw_matrix(self.grid,(0,0))
            pygame.draw.line(self.window,(255,255,255),(self.board_width+1,0),(self.board_width+1,self.height),1)
            self.draw_matrix(self.tetromino,(self.x_tetro,self.y_tetro+10))
            self.draw_matrix(self.next_tetromino,(cols+2,3))
            
            
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
