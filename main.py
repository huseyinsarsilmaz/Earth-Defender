import pygame
from pygame import mixer
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,700))
background = pygame.image.load("image/background.png").convert_alpha()
spaceship = pygame.image.load("image/spaceship.png").convert_alpha()
earth = pygame.image.load("image/earth.png").convert_alpha()
ufo = pygame.image.load("image/ufo.png").convert_alpha()
bomb = pygame.image.load("image/bomb.png").convert_alpha()
laser = pygame.image.load("image/laser.png").convert_alpha()
mixer.music.load("audio/music.mp3")
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

player = pygame.sprite.GroupSingle()
player.add(Player())

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: player.sprite.dx = -4
            elif event.key == pygame.K_d: player.sprite.dx = 4
            elif event.key == pygame.K_s: player.sprite.dy = 4
            elif event.key == pygame.K_w: player.sprite.dy = -4
            #elif event.key == pygame.K_SPACE and shot == False: fire(laser,player.x+29.5,player.y+10)
        if event.type == pygame.KEYUP:
            if( event.key == pygame.K_a or event.key == pygame.K_d) : player.sprite.dx = 0
            elif ( event.key == pygame.K_s or event.key == pygame.K_w) : player.sprite.dy = 0
    screen.blit(background,(0,0))
    player.update()
    player.draw(screen)
    pygame.display.update()
    clock.tick(60)