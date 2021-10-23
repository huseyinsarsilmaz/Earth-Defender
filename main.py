from operator import truediv
import pygame
from pygame import mixer
from sys import exit
import random
import math

from pygame import rect

pygame.init()
screen = pygame.display.set_mode((1200,700))
background = pygame.image.load("image/background.png").convert_alpha()
spaceship = pygame.image.load("image/spaceship.png").convert_alpha()
planet = pygame.image.load("image/earth.png").convert_alpha()
ufo = pygame.image.load("image/ufo.png").convert_alpha()
bomb = pygame.image.load("image/bomb.png").convert_alpha()
beam = pygame.image.load("image/laser.png").convert_alpha()
mixer.music.load("audio/music.mp3")
laser_sound = mixer.Sound("audio/laser.mp3")
#mixer.music.play(loops = -1)
pygame.display.set_caption("Earth Defender")
pygame.display.set_icon(spaceship)
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship
        self.rect = self.image.get_rect(center = (600,350))
        self.angle = 0
        self.dangle = 0
        self.dx = 0
        self.dy = 0

    def update(self):
        self.image = pygame.transform.rotozoom(spaceship,-self.angle,1)
        self.rect = self.image.get_rect(center=self.rect.center)
        if(self.angle == -360 or self.angle == 360) : self.angle = 0
        self.angle =  self.angle + self.dangle
        self.rect.x += self.dx
        self.rect.y += self.dy
        if(self.rect.midleft[0] <= 0) : self.rect = self.image.get_rect(midleft = (0,self.rect.midleft[1]))
        elif(self.rect.midright[0] >= 1200) : self.rect = self.image.get_rect(midright = (1200,self.rect.midright[1]))
        if(self.rect.midtop[1] <= 0):  self.rect = self.image.get_rect(midtop = (self.rect.midtop[0],0))
        elif(self.rect.midbottom[1] >= 700):  self.rect = self.image.get_rect(midbottom = (self.rect.midbottom[0],700))

class Earth(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = planet
        self.rect = self.image.get_rect(center = (600,700))

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = beam
        self.rect = self.image.get_rect()
        self.angle = 0
        self.rect.x = -200
        self.rect.y = -200
        self.dy = -10
        self.shot = False
    
    def update(self): 
        self.image = pygame.transform.rotozoom(beam,-self.angle,1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.y += self.dy
        self.rect.x += self.dx
        if(self.rect.y < 0 or self.rect.y > 700 or self.rect.x < 0 or self.rect.x > 1200) : self.shot = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ufo
        self.pos = [random.randint(0,1100),0]
        self.rect = self.image.get_rect(midbottom = self.pos)
        self.dx = 0
        self.dy = 0.25
    def update(self): 
        self.pos[1] =self.pos[1] + self.dy
        self.rect = self.image.get_rect(center = self.pos)

player = pygame.sprite.GroupSingle()
player.add(Player())
earth = pygame.sprite.GroupSingle()
earth.add(Earth())
laser = pygame.sprite.GroupSingle()
laser.add(Laser())
enemy = pygame.sprite.Group()
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer,3000)
move = False
reverse = False

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT : player.sprite.dangle = -2
            elif event.key == pygame.K_RIGHT : player.sprite.dangle = 2
            elif event.key == pygame.K_UP : move = True 
            elif event.key == pygame.K_DOWN:
                move = True
                reverse = True
            elif event.key == pygame.K_SPACE and laser.sprite.shot == False: 
                laser.sprite.shot = True
                laser_sound.play()
                laser.sprite.rect = laser.sprite.image.get_rect(center = (player.sprite.rect.center))
                laser.sprite.angle = player.sprite.angle
                laser.sprite.dx = 15*math.sin(math.radians(laser.sprite.angle))
                laser.sprite.dy = -15*math.cos(math.radians(laser.sprite.angle))
        if event.type == pygame.KEYUP:
            if( event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) : player.sprite.dangle = 0
            elif ( event.key == pygame.K_UP): 
                move = False
                player.sprite.dangle = 0
                player.sprite.dx = 0
                player.sprite.dy = 0
            elif ( event.key == pygame.K_DOWN): 
                move = False
                reverse = False
                player.sprite.dangle = 0
                player.sprite.dx = 0
                player.sprite.dy = 0
        if event.type == enemy_timer:
            newEnemy = Enemy()
            enemy.add(newEnemy)
    screen.blit(background,(0,0))
    earth.draw(screen)
    if(move):
        player.sprite.dx = 4*math.sin(math.radians(player.sprite.angle))
        player.sprite.dy = -4*math.cos(math.radians(player.sprite.angle))
        if(reverse):
            player.sprite.dx = -player.sprite.dx
            player.sprite.dy = -player.sprite.dy
    player.update()
    player.draw(screen)
    if(laser.sprite.shot  == True):
        laser.update()
        laser.draw(screen)
    enemy.update()
    enemy.draw(screen)
    pygame.display.update()
    clock.tick(60)