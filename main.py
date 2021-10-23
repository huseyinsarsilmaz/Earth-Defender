import pygame
from pygame import mixer
from sys import exit
import random

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
mixer.music.play(loops = -1)
pygame.display.set_caption("Earth Defender")
pygame.display.set_icon(spaceship)
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship
        self.rect = self.image.get_rect(center = (600,350))
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

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
        self.rect.x = -200
        self.rect.y = -200
        self.dy = -10
        self.shot = False
    
    def update(self): 
        self.rect.y += self.dy
        if(self.rect.y < 0) : self.shot = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ufo
        self.pos = [random.randint(0,1100),0]
        self.rect = self.image.get_rect(midbottom = self.pos)
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
pygame.time.set_timer(enemy_timer,7500)

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: player.sprite.dx = -4
            elif event.key == pygame.K_RIGHT: player.sprite.dx = 4
            elif event.key == pygame.K_DOWN: player.sprite.dy = 4
            elif event.key == pygame.K_UP: player.sprite.dy = -4
            elif event.key == pygame.K_SPACE and laser.sprite.shot == False: 
                laser.sprite.shot = True
                laser_sound.play()
                laser.sprite.rect = laser.sprite.image.get_rect(center = (player.sprite.rect.midtop))
        if event.type == pygame.KEYUP:
            if( event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) : player.sprite.dx = 0
            elif ( event.key == pygame.K_DOWN or event.key == pygame.K_UP) : player.sprite.dy = 0
        if event.type == enemy_timer:
            enemy.add(Enemy())
    screen.blit(background,(0,0))
    earth.draw(screen)
    player.update()
    player.draw(screen)
    if(laser.sprite.shot  == True):
        laser.update()
        laser.draw(screen)
    enemy.update()
    enemy.draw(screen)
    pygame.display.update()
    clock.tick(60)