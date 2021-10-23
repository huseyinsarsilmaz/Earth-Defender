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

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background,(0,0))
    pygame.display.update()
    clock.tick(60)