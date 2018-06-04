import sys;
from pygame.locals import *
import pygame;
import time;
from random import randint

class Player:
    pos_x = [];
    pos_y = [];
    player_img = "block.png"
    step = 18;
    length = 3;
    maxLength = 3;
    player_rect = pos_x,pos_y
    speed = 15;
    direction = 0;

    updateCountMax = 2;
    updateCount = 0;

    def __init__(self,maxLength):
        self.maxLength = maxLength;
        for i in range(0,self.maxLength):
            self.pos_x.append(-100);
            self.pos_y.append(-100);
        self.pos_x[0] = self.step;
        self.pos_y[0] = self.step;
        self.pos_x[1] = 1 * self.step;
        self.pos_x[2] = 2* self.step;
        self.pos_y[1] = 1 * self.step;
        self.pos_y[2] = 2* self.step;
    def update(self):
        self.updateCount += 1;
        if( self.updateCount > self.updateCountMax):

            #update followers pos
            for i in range(self.length - 1,0,-1):
                self.pos_x[i] = self.pos_x[i - 1];
                self.pos_y[i] = self.pos_y[i - 1];

            #update head of snake pos
            if(self.direction == 0):
                if(self.pos_x[0] > 700):
                    self.pos_x[0] = 0;
                self.pos_x[0] += self.step;
            if(self.direction == 1):
                if(self.pos_x[0] < 1):
                    self.pos_x[0] = 720;
                self.pos_x[0] -= self.step;
            if(self.direction == 2):
                if(self.pos_y[0] > 460):
                    self.pos_y[0] = 0
                self.pos_y[0] += self.step;
            if(self.direction == 3):
                if(self.pos_y[0] < 1):
                    self.pos_y[0] = 480;
                self.pos_y[0] -= self.step;

            #reset update count
            self.updateCount = 0;

    def reset(self):
        self.length = 3;
        self.direction = 0
        self.pos_x[0] = self.step;
        self.pos_y[0] = self.step;
        self.pos_x[1] = 1 * self.step;
        self.pos_x[2] = 2* self.step;
        self.pos_y[1] = 1 * self.step;
        self.pos_y[2] = 2* self.step;

    def move_Right(self):
        if(self.direction != 1):
            self.direction = 0;

    def move_Left(self):
        if(self.direction != 0):
            self.direction = 1;

    def move_Down(self):
        if(self.direction != 3):
            self.direction = 2;

    def move_Up(self):
        if(self.direction != 2):
            self.direction = 3;

    def drawTail(self,screen, image):
        for i in range(0, self.length):
            screen.blit(image,(self.pos_x[i],self.pos_y[i]));

class Food:
    x = 0;
    y = 0;
    food_img = "apple.png"
    food_rect = x,y
    step = 16;

    def __init__(self,x,y):
        self.x = x * self.step;
        self.y = y * self.step;
        self.food_rect = self.x, self.y

    def draw(self, screen, image):
        screen.blit(image,(self.x, self.y));


class Score:
    num = 0;
    myfont = None;
    text = None;
    def __init__(self,):
        pygame.font.init();
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30);
        self.text = self.myfont.render("Score: ", False,(0,0,0));

    def update(self):
        self.text = self.myfont.render("Score: " +str(self.num), False,(0,0,0));

    def draw(self,screen):
        screen.blit(self.text,(0,0));



class GameLogic:
    def collision(self,x1, y1, x2, y2, bsize):
        if(x1 >= x2 - 7 and (x1 <= x2 +(bsize))):
            if(y1 >= y2 -(bsize -7) and (y1<= y2 + (bsize))):
                return True
        return False;

class Game:
    win_size = win_width, win_height = 720, 480;
    player = 0;
    high_score = 0;
    food = 0;
    score = 0;
    screen = pygame.display.set_mode(win_size);

    def __init__(self):
        self.player = Player(2000);
        self.food = Food(5,5);
        self.score = Score();
        self.logic = GameLogic();
        self.running = True;
        self.lost = False;
        self.snake = None;
        self.apple = None;

    def on_init(self):
        pygame.init();
        self.running = True;
        self.snake = pygame.image.load(self.player.player_img).convert();
        self.apple = pygame.image.load(self.food.food_img).convert();

    def quitEvent(self, event):
        if(event.type == QUIT):
            self.running = False;


    def render(self):
        self.screen.fill((255,255,255));
        self.player.drawTail(self.screen, self.snake);
        self.food.draw(self.screen, self.apple);
        self.score.draw(self.screen);
        pygame.display.flip()

    def loop(self):
        self.player.update();
        self.score.update();

        #check for snake eating
        for i in range(0, self.player.length):
            if(self.logic.collision(self.food.x,self.food.y,self.player.pos_x[i], self.player.pos_y[i], self.food.step)):
                self.food.x = randint(1,30) * self.food.step;
                self.food.y = randint(1,20) * self.food.step;
                self.player.length += 1;
                self.score.num += 1;

        #snake on snake collision
        for i in range(2, self.player.length):
            if(self.logic.collision(self.player.pos_x[0],self.player.pos_y[0],self.player.pos_x[i],self.player.pos_y[i],(self.player.step - 7))):
                self.reset();


        pass


    def reset(self):
        print("YOU LOSE");
        self.player.reset();
        self.score.num = 0;
    def endGame(self):
        pygame.quit();

    def playGame(self):
        if self.on_init() == False:
            self._running = False;
        while(self.running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if(keys[K_RIGHT] or keys[K_d]):
                self.player.move_Right();
            if(keys[K_LEFT] or keys[K_a]):
                self.player.move_Left();
            if(keys[K_UP] or keys[K_w]):
                self.player.move_Up();
            if(keys[K_DOWN] or keys[K_s]):
                self.player.move_Down();
            if(keys[K_ESCAPE]):
                self.running = False;
            self.render();
            self.loop()
            time.sleep (1.0 / 10000000000000.0);
        self.endGame();

if __name__ == "__main__" :
    theGame = Game();
    theGame.playGame();
# snake
