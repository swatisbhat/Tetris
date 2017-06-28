import pygame,sys,time
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
        pygame.key.set_repeat(250,25)
        self.height=cell*rows
        self.width=cell*(columns+8)
        self.board_width=cell*columns
        self.grid=[[8 if x%2==y%2 else 0 for x in xrange(columns)] for y in xrange(rows)]
        pygame.display.set_caption("TETRIS","TETRIS")
        self.window=pygame.display.set_mode((self.width,self.height))
        #pygame.mixer.init()
        #pygame.mixer.music.load('Angi.ogg')
        #pygame.mixer.music.play(-1)
        #pygame.mixer.music.set_volume(0.9)

        pygame.event.set_blocked(pygame.MOUSEMOTION) #block mouse motion events
        self.next_tetromino=shapes[random.randrange(len(shapes))]

        self.default_font=pygame.font.Font(pygame.font.get_default_font(),12)
        #start game
        self.start_game()



    def new_tetromino(self):
        self.tetromino=self.next_tetromino[:]
        self.next_tetromino=shapes[random.randrange(len(shapes))]
        self.x_tetro=int(columns/2-len(self.tetromino[0])/2)
        self.y_tetro=0

        if collision(self.board,self.tetromino,(self.x_tetro,self.y_tetro)):
            self.gameover=True


    def start_game(self):
        self.board=new_board()
        self.new_tetromino()
        self.score=0
        self.level=1
        self.cleared_lines=0
        pygame.time.set_timer(pygame.USEREVENT+1, 750)

    def display_msg(self,msg,offset):
        x_off,y_off=offset
        for line in msg.splitlines():
            self.window.blit(self.default_font.render(line,True,(255,255,255),(0,0,0)),(x_off,y_off))
            y_off+=10

    def center_msg(self, msg):
		for i, line in enumerate(msg.splitlines()):
			msg_image =  self.default_font.render(line, True,(255,255,255), (0,0,0))

			img_size_x, img_size_y = msg_image.get_size()
			img_size_x //= 2
			img_size_y //= 2

			self.window.blit(msg_image, (self.width // 2-img_size_x,self.height // 2-img_size_y+i*22))

    def draw_matrix(self,matrix,offset):
        x_off,y_off=offset
        for y, row in enumerate(matrix):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(self.window,colors[col],((x_off+x)*cell,(y_off+y)*cell,cell,cell),0)

    def shift(self,unit):
        if not self.gameover and not self.paused:
            x_new=self.x_tetro+unit

            #handle collisions with left and right borders
            if x_new<0:
                x_new=0
            if x_new>columns-len(self.tetromino[0]):
                x_new=columns-len(self.tetromino[0])

            if not collision(self.board,self.tetromino,(x_new,self.y_tetro)):
                self.x_tetro=x_new

    def next_level(self,cleared_lines):
        level_scores=[0,10,20,30,40,50]
        bonus=50
        if cleared_lines>1:
            self.score=self.score+level_scores[self.level]*cleared_lines+bonus*cleared_lines
        else:
            self.score=self.score+level_scores[self.level]*cleared_lines
        self.cleared_lines+=cleared_lines
        if self.cleared_lines>=self.level*2:
            self.level+=1
            delay=750-70*(self.level-1)
            delay=100 if delay<100 else delay
            pygame.time.set_timer(pygame.USEREVENT+1,delay)

    def drop_tetro(self,down_key):
        if not self.gameover and not self.paused:
            self.y_tetro+=1
            if down_key==True:
                self.score+=1

            #add tetromino to board when it reaches bottom
            if collision(self.board,self.tetromino,(self.x_tetro,self.y_tetro)):
                self.board=add_tetros(self.board,self.tetromino,(self.x_tetro,self.y_tetro))
                self.new_tetromino()

                cleared_lines=0
                #delete completed rows
                while True:
                    for i,row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board=delete_row(self.board,i)
                            cleared_lines+=1
                            break
                    else:
                        break
                self.next_level(cleared_lines)

    # TODO - return the offsets of rotated tetromino when changing the rotate function
    # The current rotate function is such that offsets remain same

    def rotate_tetromino(self):
        new_tetromino=rotate(self.tetromino)
        if not collision(self.board,new_tetromino,(self.x_tetro,self.y_tetro)):
            self.tetromino=new_tetromino




    def new_game(self):
        self.new_game=True

    def game_pause(self):
    	self.paused = not self.paused

    def game_resume(self):
        self.paused=not self.paused

    def quit(self):
        self.quit=True


    def run(self):
        key_actions={
            'UP': self.rotate_tetromino,
            'LEFT': lambda:self.shift(-1),
            'RIGHT': lambda:self.shift(1),
            'DOWN': lambda:self.drop_tetro(True),
            'ESCAPE': self.quit,
            'p':self.game_pause,
            'r':self.game_resume,
            'SPACE': self.new_game

        }
        self.quit=False
        self.gameover=False
        self.paused=False
        self.new_game=False

        while 1:
            #window colour
            self.window.fill((0,0,0))
            if self.gameover:
				self.center_msg("GAME OVER!\nYOUR SCORE: %d" % self.score);pygame.display.update();time.sleep(2);sys.exit()

            else:
                if self.paused:
                    self.center_msg("PAUSED")
                elif self.quit:
                    self.center_msg("QUITTING GAME!")
                    pygame.display.update()
                    sys.exit()
                elif self.new_game:
                    self.center_msg("NEW GAME")
                    pygame.display.update()
                    time.sleep(1)
                    self.start_game()
                    self.gameover=False
                    self.new_game=False
                else:
                    #draw on the window
                    pygame.draw.line(self.window,(255,255,255),(self.board_width+1,0),(self.board_width+1,self.height),1)
                    self.draw_matrix(self.grid,(0,0))
                    self.draw_matrix(self.board,(0,0))
                    self.draw_matrix(self.tetromino,(self.x_tetro,self.y_tetro))
                    self.draw_matrix(self.next_tetromino,(columns+2.5,3))
                    self.display_msg("NEXT TETROMINO:", (self.board_width+(1.5*cell),cell))
                    self.display_msg("SCORE: %d\n\nLEVEL: %d\n\nLINES CLEARED: %d"\
                     % (self.score, self.level, self.cleared_lines),(self.board_width+(1.5*cell), cell*6))
            pygame.display.update()
                    #event handling
            for event in pygame.event.get():
                if event.type==pygame.USEREVENT+1:
                    self.drop_tetro(False)

                elif event.type==pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key==eval("pygame.K_"+key):
                            key_actions[key]()

                elif event.type==pygame.QUIT:
                    self.quit=True


if __name__=='__main__':

    tetris=Tetris()
    tetris.run()
