import pygame
from pygame import mixer
from sys import exit
import random
import math

#Constants
Player_rotation = 1.5
Enemy_spawn_time = 300
Enemy_spawn_decrement_tick = 60
Laser_energy_use = 2.5
Turbo_energy_use = 0.05
Player_movement_speed = 5
Enemy_player_collision_damage = 20
Bomb_earth_damage = 25
Bomb_player_damage = 10
Enemy_laser_damage = 5
Player_energy_recovery = 0.05
Player_health_recovery = 0.01
Bomb_Movemement_steps = 600
Enemy_bomb_launch_time = 400


pygame.init()
screen = pygame.display.set_mode((1200,700))
background = pygame.image.load("image/background.png").convert_alpha()
spaceship = pygame.image.load("image/spaceship.png").convert_alpha()
player_health_icon = pygame.transform.rotozoom(spaceship,0,0.55)
planet = pygame.image.load("image/earth.png").convert_alpha()
earth_health_icon = pygame.transform.rotozoom(pygame.image.load("image/earth_health.png").convert_alpha(),0,0.55)
earth_shield = pygame.image.load("image/earth_shield.png").convert_alpha()
earth_shield_control = pygame.image.load("image/earth_shield_control.png").convert_alpha()
ufo = pygame.image.load("image/ufo.png").convert_alpha()
bombimg = pygame.image.load("image/bomb.png").convert_alpha()
beam = pygame.image.load("image/laser.png").convert_alpha()
flame = pygame.image.load("image/flame.png").convert_alpha()
turbo = pygame.image.load("image/turbo.png").convert_alpha()
enemy_beam = pygame.image.load("image/enemy_laser.png").convert_alpha()
energy = pygame.transform.rotozoom(pygame.image.load("image/energy.png").convert_alpha(),0,0.55)
mixer.music.load("audio/music.mp3")
mixer.music.set_volume(0.35)
laser_sound = mixer.Sound("audio/laser.mp3")
enemy_hit = mixer.Sound("audio/enemy_hit.mp3")
laser_hit = mixer.Sound("audio/laser_hit.mp3")
bomb_drop = mixer.Sound("audio/bomb_drop.mp3")
pygame.display.set_caption("Earth Defender")
pygame.display.set_icon(spaceship)
clock = pygame.time.Clock()
score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship
        self.rect = self.image.get_rect(center = (600,350))
        self.health = 100
        self.energy = 100
        self.speed = Player_movement_speed
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
        self.health = 250
        self.rect = self.image.get_rect(center = (600,690))
        self.shielded = earth_shield

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
        if(self.rect.y < 0 or self.rect.y > 700 or self.rect.x < 0 or self.rect.x > 1200):
            self.shot = False
            laser.sprite.rect.center = (-250,-250)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,index):
        super().__init__()
        self.image = ufo
        self.index = index
        self.counter = 0
        self.health = 3
        self.steps = 1000
        self.bomb_time = 0
        self.laser_time = 0
        self.pos = [random.randint(0,1100),0]
        self.rect = self.image.get_rect(midbottom = self.pos)
        self.dangle = (-70 + 10*index)/(self.steps/2)
        self.angle = 0
        if( (-70 + 10*index) < 0) : self.dx = ((600 - abs(math.sin(math.radians(-70 + 10*index))*500)) - self.pos[0])/self.steps
        elif((-70 + 10*index) == 0) : self.dx = (600-self.pos[0])/self.steps
        else: self.dx = ((600 + math.sin(math.radians(-70 + 10*index))*500) - self.pos[0])/self.steps
        self.dy = (200 + (500 - (abs(math.cos(math.radians((-70 + 10*index)))*500))))/self.steps
        self.index = index
        
    def bomb_launch(self): 
        bomb_drop.play()
        bomb.add(Bomb([self.pos[0],self.pos[1]]))

    def laser_launch(self):
        laser_hit.play()
        enemy_laser.add(Enemy_laser([self.pos[0],self.pos[1]]))
        
    def update(self): 
        if( self.health < 3):
            if(self.laser_time == 100):
                self.laser_time = 0
                self.laser_launch()
            mx = player.sprite.rect.centerx - self.pos[0]
            my = player.sprite.rect.centery  - self.pos[1]
            self.angle = math.atan2(mx,my)
            self.dx = math.sin(self.angle)
            self.dy = math.cos(self.angle)
            self.pos[1] =self.pos[1] + self.dy
            self.pos[0] =self.pos[0] + self.dx
            self.image = pygame.transform.rotozoom(ufo,-self.angle,1)
            self.rect = self.image.get_rect(midbottom = self.pos)
            self.laser_time = self.laser_time +1
        else:
            self.bomb_time = self.bomb_time +1
            if(self.bomb_time == Enemy_bomb_launch_time):
                self.bomb_time = 0
                self.bomb_launch()
            if(self.counter <= self.steps):
                if(self.counter >= (self.steps/2)):
                    self.angle = self.angle + self.dangle
                self.pos[1] =self.pos[1] + self.dy
                self.pos[0] =self.pos[0] + self.dx
                self.counter = self.counter +1
            self.image = pygame.transform.rotozoom(ufo,-self.angle,1)
            self.rect = self.image.get_rect(midbottom = self.pos)

class Fire(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = flame
        self.rect = self.image.get_rect()
        self.pos = [0,0]
        self.angle = 0
        self.turbo = False
        self.playerx = 0
        self.playery = 0
    
    def update(self): 
        if(self.turbo == False) : self.image = pygame.transform.rotozoom(flame,-self.angle,1)
        else : self.image = pygame.transform.rotozoom(turbo,-self.angle,1)
        self.pos[0] = self.playerx - math.sin(math.radians(self.angle))*40
        self.pos[1] = self.playery + math.cos(math.radians(self.angle))*40
        self.rect = self.image.get_rect(center = self.pos)

class Bomb(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.counter = 0
        self.steps = Bomb_Movemement_steps
        self.dx = (600 - self.pos[0] )/self.steps
        self.dy = (700 - self.pos[1] )/self.steps
        self.angle = math.degrees(math.atan2(self.dx,self.dy))
        self.image = pygame.transform.rotozoom(bombimg,self.angle,0.65)
        self.rect = self.image.get_rect(center = self.pos)
    
    def update(self): 
        if(self.counter <= self.steps):
            self.pos[1] =self.pos[1] + self.dy
            self.pos[0] =self.pos[0] + self.dx
            self.counter = self.counter +1
        self.rect = self.image.get_rect(center = self.pos)

class Enemy_laser(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        mx = player.sprite.rect.centerx - self.pos[0]
        my = player.sprite.rect.centery - self.pos[1]
        self.angle = math.atan2(mx,my)
        self.dx = math.sin(self.angle)
        self.dy = math.cos(self.angle)
        self.image = pygame.transform.rotozoom(enemy_beam,math.degrees(self.angle),1)
        self.rect = self.image.get_rect(center = self.pos)
    
    def update(self): 
        self.pos[1] =self.pos[1] + self.dy*5
        self.pos[0] =self.pos[0] + self.dx*5
        self.rect = self.image.get_rect(center = self.pos)
     
player = pygame.sprite.GroupSingle()
player.add(Player())
earth = pygame.sprite.GroupSingle()
earth.add(Earth())
laser = pygame.sprite.GroupSingle()
laser.add(Laser())
enemy = pygame.sprite.Group()
enemy_spawn = 0
enemy_list = []
for i in range(15) : enemy_list.append(False)
fire = pygame.sprite.GroupSingle()
fire.add(Fire())
maximum = False
move = False
reverse = False
bomb = pygame.sprite.Group()
enemy_laser = pygame.sprite.Group()
shield_counter = 0
origin_tech = pygame.font.Font("font/OriginTech.ttf",100)
press_space_font = pygame.font.Font("font/OriginTech.ttf",50)
score_font = pygame.font.Font("font/OriginTech.ttf",40)
game_name = origin_tech.render("Earth Defender",True,(255,255,255))
game_over_text = origin_tech.render("GAME OVER",True,(255,255,255))
press_space_counter = 0
game_name_rect = game_name.get_rect(center = (600,300))
game_over_text_rect = game_over_text.get_rect(center = (600,300))
enemy_spawn_decrement = 0
starting_screen = True
game_over = False

while True:
    if(starting_screen == False and game_over == False):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT : player.sprite.dangle = -Player_rotation 
                elif event.key == pygame.K_RIGHT : player.sprite.dangle = Player_rotation 
                elif event.key == pygame.K_UP : move = True 
                elif event.key == pygame.K_DOWN:
                    move = True
                    reverse = True
                elif event.key == pygame.K_SPACE and laser.sprite.shot == False: 
                    if(player.sprite.energy >= 5):
                        player.sprite.energy = player.sprite.energy - Laser_energy_use
                        laser.sprite.shot = True
                        laser_sound.play()
                        laser.sprite.rect = laser.sprite.image.get_rect(
                        center = (player.sprite.rect.centerx + math.sin(math.radians(player.sprite.angle))*15,
                        player.sprite.rect.centery - math.cos(math.radians(player.sprite.angle))*15))
                        laser.sprite.angle = player.sprite.angle
                        laser.sprite.dx = 15*math.sin(math.radians(laser.sprite.angle))
                        laser.sprite.dy = -15*math.cos(math.radians(laser.sprite.angle))
                elif event.key == pygame.K_LSHIFT: player.sprite.speed = Player_movement_speed*2
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
                elif event.key == pygame.K_LSHIFT : player.sprite.speed = Player_movement_speed
        screen.blit(background,(0,0))
        if(move):
            player.sprite.dx = player.sprite.speed*math.sin(math.radians(player.sprite.angle))
            player.sprite.dy = -player.sprite.speed*math.cos(math.radians(player.sprite.angle))
            if(reverse):
                player.sprite.dx = -player.sprite.dx
                player.sprite.dy = -player.sprite.dy
        if(laser.sprite.shot  == True):
            laser.update()
            laser.draw(screen)
        if(move):
            if(player.sprite.speed == 5) : fire.sprite.turbo = False
            else: 
                player.sprite.energy = player.sprite.energy - Turbo_energy_use
                fire.sprite.turbo = True
            fire.sprite.angle = player.sprite.angle
            fire.sprite.playerx = player.sprite.rect.centerx
            fire.sprite.playery = player.sprite.rect.centery
            fire.update()
            fire.draw(screen)
        pygame.draw.rect(screen,(200,0,0),(55,18,180*(player.sprite.health/100),20))
        pygame.draw.rect(screen,(0,0,200),(55,63,180*(earth.sprite.health/250),20))
        pygame.draw.rect(screen,(200,200,0),(55,104,180*(player.sprite.energy/100),20))
        screen.blit(player_health_icon,(10,10))
        screen.blit(earth_health_icon,(10,55))
        screen.blit(energy,(10,100))
        enemy.update()
        enemy.draw(screen)
        for i in enemy.sprites():
            if( pygame.sprite.collide_mask(laser.sprite,i) != None ) :
                laser.sprite.rect.center = (-250,-250)
                if( i.health > 1): 
                    i.health = i.health -1
                else:
                    enemy_hit.play()
                    enemy_list[i.index] = False
                    i.kill()
                    score += 1
            if( pygame.sprite.collide_mask(player.sprite,i) != None):
                player.sprite.health = player.sprite.health - Enemy_player_collision_damage
                enemy_hit.play()
                enemy_list[i.index] = False
                i.kill()
                score += 1
        for i in bomb.sprites():
            earth.sprite.image = earth_shield_control
            if( pygame.sprite.collide_mask(earth.sprite,i) != None):
                shield_counter = 1
                earth.sprite.health = earth.sprite.health - Bomb_earth_damage
                i.kill()
            elif(shield_counter == 0):
                earth.sprite.image = planet
            if ( pygame.sprite.collide_mask(player.sprite,i) != None):
                player.sprite.health = player.sprite.health - Bomb_player_damage
                i.kill()
            if ( pygame.sprite.collide_mask(laser.sprite,i) != None):
                i.kill()
                laser.sprite.rect.center = (-250,-250)
        if( shield_counter > 0 ):
            shield_counter += 1
            if(shield_counter > 30) : shield_counter = 0
        if(earth.sprite.image == earth_shield_control) : earth.sprite.image = earth_shield
        for i in enemy_laser.sprites():
            if( pygame.sprite.collide_mask(player.sprite,i) != None):
                player.sprite.health = player.sprite.health - Enemy_laser_damage
                i.kill()
        earth.draw(screen)
        bomb.update()
        bomb.draw(screen)
        enemy_spawn += 1
        if(enemy_spawn == Enemy_spawn_time):
            for i in range(len(enemy_list)):
                    if enemy_list[i] == False:
                        maximum = False
                        break
                    elif( i == len(enemy_list)-1): maximum = True
            if( maximum == False):
                while True:
                    index = random.randint(0,14)
                    if( enemy_list[index] == False):
                        newEnemy = Enemy(index)
                        enemy.add(newEnemy)
                        enemy_list[index] = True
                        break
            enemy_spawn = 0  
        enemy_laser.update()
        enemy_laser.draw(screen)
        player.update()
        player.draw(screen)
        if(player.sprite.energy < 100): player.sprite.energy = player.sprite.energy + Player_energy_recovery
        if(player.sprite.energy < 0 ) : player.sprite.energy = 0
        if(player.sprite.health < 100): player.sprite.helth = player.sprite.health + Player_health_recovery
        score_text = "Score: " + str(score)
        score_display = score_font.render(score_text,False,(255,255,255))
        score_display_rect = score_display.get_rect(topright = [1180,20])
        screen.blit(score_display,score_display_rect)
        if(enemy_spawn_decrement < Enemy_spawn_decrement_tick) : enemy_spawn_decrement += 1
        else:
            enemy_spawn_decrement = 0
            if(Enemy_spawn_time > 60) : Enemy_spawn_time -= 1
        if(player.sprite.health <= 0 or earth.sprite.health <= 0):
            pygame.mixer.music.stop()
            game_over = True
    elif(starting_screen == True):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    starting_screen = False
                    mixer.music.play(loops = -1)
        screen.fill("#061221")
        screen.blit(game_name,game_name_rect)
        if(press_space_counter < 10): press_space_text = "> Press Space to Start <"
        elif(press_space_counter < 20): press_space_text = ">> Press Space to Start <<"
        elif(press_space_counter < 30): press_space_text = ">>> Press Space to Start <<<"
        elif(press_space_counter < 40): press_space_text = ">> Press Space to Start <<"
        if(press_space_counter < 40): press_space_counter += 1
        else: press_space_counter = 0
        press_space = press_space_font.render(press_space_text,False,(255,255,255))
        press_space_rect = press_space.get_rect(center=(600,400))
        screen.blit(press_space,press_space_rect)
    else:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                exit()
        screen.fill("#000000")
        screen.blit(game_over_text,game_over_text_rect)
        score_text = "Score: " + str(score)
        score_display = score_font.render(score_text,False,(255,255,255))
        score_display_rect = score_display.get_rect(center=(600,400))
        screen.blit(score_display,score_display_rect)
    pygame.display.update()
    clock.tick(60)