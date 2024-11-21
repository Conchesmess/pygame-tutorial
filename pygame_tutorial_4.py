# Code explained here: https://coderslegacy.com/python/pygame-tutorial-part-3/

#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()
 
#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
 
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # define an enemy
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        # place the enemy on the screen wuth center at random x and y = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
    # The enemy moves continuously from the top to the bottom
    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        # if the enemy gets to the bottom, bring it back to the top
        if (self.rect.top > 600):
            # Award the player a point if the Enemy makes it to the bottom of the screen without a collision
            SCORE += 1
            # reset the enemey to the top of the screen
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    # Reset an enemy to the top of the screen
    def reset(self):
        # put the center of the enemy at a random x and y = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
 
# The player moves by using the arrow keys
class Player(pygame.sprite.Sprite):
    #define the player
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
    
        # You can use this code to move the player up and down
        # check how the code below keeps the sprite from going off the to the screen left or right
        #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
        #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)

        # this moves the player 5 pixels at a time when arrows are pressed
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                   
#Create the Sprites        
P1 = Player()
E1 = Enemy()
 
#Put the Sprites into Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
 
#Game Loop
while True:
       
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        # the image and the rect are not necessarily the same saze
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
 
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('crash.wav').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
         
    pygame.display.update()
    FramePerSec.tick(FPS)







