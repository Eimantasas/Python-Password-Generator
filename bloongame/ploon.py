import pygame
import sys
import random
import math


Balloons = ['bloongame/graphics/bloon1.png','bloongame/graphics/bloon2.png','bloongame/graphics/bloon3.png','bloongame/graphics/bloon4.png','bloongame/graphics/bloon5.png']

Stones = ['bloongame/graphics/Stone1.png','bloongame/graphics/Stone2.png','bloongame/graphics/Stone3.png']

Pops = ['bloongame/SFX/pop1.mp3', 'bloongame/SFX/pop2.mp3', 'bloongame/SFX/pop3.mp3']

score = 0

game_over = False
 
class Explosion(pygame.sprite.Sprite):
    defaultlife = 8
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bloongame/graphics/pop.png')
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.life = self.defaultlife
    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('bloongame/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (100,300))
        self.mask = pygame.mask.from_surface(self.image)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5
        return keys

      
    def update(self):
        self.player_input()
        if self.rect.y < -80:
            self.rect.y = 500
        elif self.rect.y > 500:
            self.rect.y = -80

    def throw_dart(self):
        return Dart(player.rect.centerx, player.rect.centery)

class Dart(pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('bloongame/graphics/dart.png').convert_alpha()
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.rect.x += 15

        if self.rect.x >= 1000:
            self.kill()

class Bloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(random.choice(Balloons)).convert_alpha()
        self.rect = self.image.get_rect(center = (1050, random.randint(100,400)))
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        global score
        global game_over
        self.rect.x -= 5
        if self.rect.x <= -50:
            self.kill()
            game_over = True

        if pygame.sprite.spritecollide(self, bullet_group, True, pygame.sprite.collide_mask):
            bloon_group.add(Explosion(self.rect.center))
            score += 1
            pop_sfx = pygame.mixer.Sound(random.choice(Pops))
            pop_sfx.set_volume(0.1)
            pop_sfx.play()
            self.kill()
        return score

class Stone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(random.choice(Stones)).convert_alpha()
        self.rect = self.image.get_rect(center = (1050, random.randint(100,400)))
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        global game_over
        self.rect.x -= 5
        if pygame.sprite.spritecollide(self, player_group, True, pygame.sprite.collide_mask):
            self.kill()
            game_over = True
        if self.rect.x == -50:
            self.kill()




pygame.init()
screen = pygame.display.set_mode((1000,500))
pygame.display.set_caption('bingbong')
clock = pygame.time.Clock()
t_font = pygame.font.Font('bloongame/Fonts/Arial Rounded MT Regular.ttf', 50)

sky_surface = pygame.image.load('bloongame/graphics/sky.png').convert()
text_surface = t_font.render('Ploon', False, 'Blue')

score_message1 = t_font.render("Press Space to throw darts, avoid stones!", True, 'Black')
score_message1_rect = score_message1.get_rect(center = (500, 450))

game_message1 = t_font.render("Game over. Press space to try again.", True, 'Black')
game_message1_rect = game_message1.get_rect(center = (500, 400))

score_message2 = t_font.render(f'Your final score is: {score}',False, 'Black')
score_message2_rect = score_message2.get_rect(center = (500, 250))

player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

bullet = Dart(player.rect.centerx, player.rect.centery) 
bullet_group = pygame.sprite.Group()
bullet_group.add(bullet)
bullet_timer = 0

bloon = Bloon()
bloon_group = pygame.sprite.Group()

bloon_constant_spawn = 100
bloon_spawn = 100

stone = Stone()
stone_group = pygame.sprite.Group()
stone_group.add(stone)

stone_constant_spawn = 200
stone_spawn = 200

music1 = pygame.mixer.Sound('bloongame/Music/Touch The Bubbles 3 OST.mp3')
music1.set_volume(0.1)
music1.play()





while True:

    if game_over == False:

        if bullet_timer > 0:
            bullet_timer -= 15
        
        if bloon_spawn:
            bloon_spawn -= 1

        else:                  #This block of code makes the balloons spawn more frequently as the game progresses
            bloon = Bloon()
            bloon_group.add(bloon)
            bloon_spawn += bloon_constant_spawn
            bloon_constant_spawn -= 1
            if bloon_constant_spawn <= 37:
                bloon_constant_spawn = 37
        
        if stone_spawn:
            stone_spawn -= 1
        else:
            stone = Stone()
            stone_group.add(stone)
            stone_spawn += stone_constant_spawn
            stone_constant_spawn -= 1
            if stone_constant_spawn <= 80:
                stone_constant_spawn = 80
    
    else:
        screen.fill(0)
        screen.fill('blue')
        player_group.empty()
        bloon_group.empty()
        stone_group.empty()
        bullet_group.empty()
        screen.blit(game_message1,game_message1_rect)
        screen.blit(score_message2,score_message2_rect)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player_group.add(player)
            stone_group.add(stone)
            bullet_group.add(bullet)
            game_over = False




    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_SPACE and bullet_timer == 0:
                bullet_group.add(player.throw_dart())
                bullet_timer = 450

        if score >= 3:
            score_message1.fill(0)
        
    score_message = t_font.render(f'Your score: {score}',True, 'Black')
    score_message_rect = score_message.get_rect(center = (500, 80))

    screen.blit(sky_surface,(0,0))
    screen.blit(score_message,score_message_rect)
    screen.blit(score_message1,score_message1_rect)
    bullet_group.draw(screen)
    player_group.draw(screen)
    bloon_group.draw(screen)
    stone_group.draw(screen)
    player_group.update()
    bullet_group.update()
    bloon_group.update()
    stone_group.update()

        
    

    pygame.display.update() 
    clock.tick(60)
