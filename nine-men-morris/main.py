import pygame 
import sys
from pygame import mixer
pygame.init()
mixer.init()


screen = pygame.display.set_mode((900,800))

img = [pygame.image.load("images/img1.png"),pygame.image.load("images/img1.png")]
img = [pygame.transform.scale(img[0], (80,80)),pygame.transform.scale(img[1], (80,80))]

background_img = pygame.image.load("images/background.jpg")
background_img = pygame.transform.scale(background_img,(900,800))

black_color = (0,0,0)
white_color = (255,255,255)


index_start = 150
index_start_width = 150
index_start_height = 95

diff = 100

A = [[(index_start_width,index_start_height),(index_start_width + 3*diff,index_start_height),(index_start_width + 6*diff,index_start_height) ,
     (index_start + 6*diff,index_start_height + 3*diff) , (index_start + 6*diff,index_start_height + 6*diff) , (index_start + 3*diff,index_start_height + 6*diff), 
     (index_start,index_start_height + 6*diff) , (index_start,index_start_height + 3*diff) ] ,
     [(index_start + diff , index_start_height + diff),(index_start + 3*diff,index_start_height + diff),(index_start + 5*diff,index_start_height + diff) ,
     (index_start + 5*diff,index_start_height + 3*diff) , (index_start + 5*diff,index_start_height + 5*diff) , (index_start + 3*diff,index_start_height + 5*diff), 
     (index_start + diff ,index_start_height + 5*diff) , (index_start + diff,index_start_height + 3*diff) ],
     [(index_start + 2*diff , index_start_height + 2*diff) , (index_start + 3*diff,index_start_height + 2*diff),(index_start + 4*diff,index_start_height + 2*diff) ,
     (index_start + 4*diff,index_start_height + 3*diff) , (index_start + 4*diff,index_start_height + 4*diff) , (index_start + 3*diff,index_start_height + 4*diff), 
     (index_start + 2*diff ,index_start_height + 4*diff) , (index_start  + 2*diff ,index_start_height + 3*diff) ] ]

d = {}
for i in range(3):
    for j in range(8):
        d[A[i][j]] = (i,j)

list_postion = [[-1 for j in range(8)] for i in range(3)]

turn_message = ["first player to place","second player to place","first player to remove piece","second player to remove piece","first player to move","second player to move","first player wins","second player wins"]

def postion():
    for i in range(3):
        for j in range(8):
            list_postion[i][j] = pygame.Rect(0,0,50,50)
            list_postion[i][j].center = [A[i][j][0],A[i][j][1]]

def get_postion(x,y):
    for i in range(3):
        for j in range(8):
            if pygame.Rect.collidepoint(list_postion[i][j],x,y) == True:
                return (i,j)
    return (-1,-1)
    



def draw_board():
    screen.fill(white_color)
    screen.blit(background_img,(0,0))
    rx = 10
    for i in range(8):
        pygame.draw.circle(screen,black_color,A[0][i],rx)
        pygame.draw.circle(screen,black_color,A[1][i],rx)
        pygame.draw.circle(screen,black_color,A[2][i],rx)
    line_color = (0,0,0)
    line_width = 5
    for i in range(3):
        pygame.draw.line(screen,line_color,A[i][0],A[i][2],line_width)
        pygame.draw.line(screen,line_color,A[i][4],A[i][2],line_width)
        pygame.draw.line(screen,line_color,A[i][4],A[i][6],line_width)
        pygame.draw.line(screen,line_color,A[i][0],A[i][6],line_width)
    for i in [1,3,5,7]:
        pygame.draw.line(screen,line_color,A[0][i],A[2][i],line_width)

def draw_piece(turn,x,y):
    rect_image = img[turn].get_rect(center = A[x][y])
    screen.blit(img[turn],rect_image)

def rect_text_box(sentence):
    font = pygame.font.Font('freesansbold.ttf',40)
    text = font.render(sentence, True, white_color, black_color)
    textRect = text.get_rect()
    textRect.center = (450,770)
    screen.blit(text,textRect)


def game_sound(x):
    mixer.music.set_volume(0.7)
    if x==0:
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/add.wav"))
    elif x==1:
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/remove.wav"))
    elif x==2:
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/move.wav"))
    elif x==3:
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/win.wav"))




class game:
    def __init__(self):
        self.places = [[-1 for j in range(8)] for i in range(3)]
        self.player_add = [0,0]
        self.player_remove = [9,9]
        self.turn = 0
        self.if_win = 0
        self.x_old = -1
        self.y_old = -1
        self.done = False
        self.sound = -1

    def add(self,x,y,turn):
        if self.places[x][y] != -1:
            return False
        self.places[x][y] = turn
        self.player_add[turn] += 1
        self.sound = 0
        return True

    def move(self,x_new,y_new,x_old,y_old,turn):
        if self.places[x_new][y_new] != -1 or self.places[x_old][y_old] != turn:
            return False
        if y_new in [0,2,4,6] and x_new==x_old and (y_new == (y_old+1)%8 or y_new == (y_old-1)%8):
            self.places[x_new][y_new] = turn
            self.places[x_old][y_old] = -1
            self.sound = 2
            return True
        if y_new in [1,3,5,7]:
            if (y_new == (y_old+1)%8 or y_new == (y_old - 1)%8) and x_old == x_new:
                self.places[x_new][y_new] = turn
                self.places[x_old][y_old] = -1
                self.sound = 2
                return True
            if ((x_new==0 and x_old == 1) or (x_new==1 and x_old==0) or (x_new==1 and x_old==2) or (x_new==2 and x_old==1)) and (y_new == y_old):
                self.places[x_new][y_new] = turn
                self.places[x_old][y_old] = -1
                self.sound = 2
                return True
        return False


    def three_seq(self,x,y,turn):
        if y in [0,2,4,6]:
            if self.places[x][y] == self.places[x][(y+1)%8] == self.places[x][(y+2)%8] == turn:
                return True
            if self.places[x][y] == self.places[x][(y-1)%8] == self.places[x][(y-2)%8] == turn:
                return True
            return False
        if y in [1,3,5,7]:
            if self.places[0][y] == self.places[1][y] == self.places[2][y] == turn:
                return True
            if self.places[x][y] == self.places[x][(y+1)%8] == self.places[x][(y-1)%8] == turn:
                return True
            return False
        return False

    def remove(self,x,y,turn):
        if (self.places[x][y] == (turn+1)%2 and self.player_remove[(turn+1)%2]==3) or (self.places[x][y] == (turn+1)%2 and self.player_add[(turn+1)%2]==3):
            self.places[x][y] = -1
            self.player_remove[(turn+1)%2] -= 1
            self.sound = 1
            return True
        if self.places[x][y] == turn or self.places[x][y] == -1 or self.three_seq(x,y,(turn+1)%2):
            return False
        self.places[x][y] = -1
        self.player_remove[(turn+1)%2] -= 1
        self.sound = 1
        return True
    
    def win(self,turn):
        if self.player_remove[(turn+1)%2] < 3:
            self.done = True
            self.sound = 3
            return True

    def start_game(self,x,y):
        self.sound = -1
        if self.if_win == 1:
            if self.remove(x,y,self.turn):
                self.if_win = 0
                if self.win(self.turn):
                    self.message = turn_message[6 + self.turn]
                elif sum(self.player_add) == 18:
                    self.turn = (self.turn+1)%2
                    self.message = turn_message[4 + self.turn]
                else:
                    self.turn = (self.turn+1)%2
                    self.message = turn_message[self.turn]
        elif min(self.player_add)<9:
            if self.add(x,y,self.turn):
                if self.three_seq(x,y,self.turn):
                    self.if_win = 1
                    self.message = turn_message[2 + self.turn]
                else:
                    self.turn = (self.turn+1)%2
                    if sum(self.player_add)==18:
                        self.message = "first player turn to move"
                    else:   
                        self.message = turn_message[self.turn]
        elif min(self.player_add)==9:
            if self.x_old == -1 and self.places[x][y]==self.turn:
                self.x_old = x 
                self.y_old = y
                self.message = "select postion to move"
            else:
                if self.move(x,y,self.x_old,self.y_old,self.turn):
                    self.x_old = -1
                    self.y_old = -1
                    if self.three_seq(x,y,self.turn):
                        self.message = turn_message[2 + self.turn]
                        self.if_win = 1
                    else:
                        self.turn = (self.turn+1)%2
                        self.message = "first player turn to move" if self.turn == 0 else "second player turn to move"
                elif self.x_old != -1:
                    self.message = "select valid postion"
                

            

    def draw(self):
        draw_board()
        for i in range(3):
            for j in range(8):
                if self.places[i][j]!=-1:
                    draw_piece(self.places[i][j],i,j)
        rect_text_box(self.message)





def main():
    done = False
    postion()
    draw_board()
    rect_text_box(turn_message[0])
    win_if = 0
    turn = 0
    gm = game()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                done = True
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  
                done = True
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x,y = get_postion(pos[0],pos[1])
                if x==-1:
                    break
                if min(gm.player_remove) >= 3:
                    gm.start_game(x,y)
                    gm.draw()
                    game_sound(gm.sound)
        pygame.display.flip()
main()
