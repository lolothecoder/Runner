import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Mario_Walk1.gif').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Mario_Walk2.gif').convert_alpha()
        player_walk_3 = pygame.image.load('graphics/Mario_Walk3.gif').convert_alpha()

        self.player_walk = [player_walk_1, player_walk_2, player_walk_3]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Mario_Jump.gif').convert_alpha()
        self.player_jump = pygame.transform.scale(self.player_jump, (80, 80))

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100,320))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 320:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 320:
            self.rect.bottom = 320

    def animation_state(self):
        if self.rect.bottom < 320:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'bullet':
            bullet = pygame.image.load('graphics/bullet.png').convert_alpha()
            bullet = pygame.transform.scale(bullet, (70, 50))
            self.frames = [bullet]
            y_pos = 200
        else:
            goomba_1 = pygame.image.load('graphics/goomba_1.png').convert_alpha()
            goomba_1 = pygame.transform.scale(goomba_1, (60, 60))
            goomba_2 = pygame.image.load('graphics/goomba_2.png').convert_alpha()
            goomba_2 = pygame.transform.scale(goomba_2, (60, 60))
            self.frames = [goomba_1, goomba_2]
            y_pos = 320
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.speed = int(get_score()/12) * 2 + 6
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(f'Score: {int(current_time/1000)}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    #print(current_time)
    return current_time

def get_score():
    current_time = pygame.time.get_ticks() - start_time
    return int(current_time/1000)

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group, False):
        obstacle_group.empty()
        return False
    return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Speed")
clock = pygame.time.Clock()
test_font = pygame.font.Font('fonts/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/mario.mp3')
bg_music.set_volume(0.5)
bg_music.play()
bg_music.play(loops = -1)


player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/bg.jpg').convert_alpha()
sky_surface = pygame.transform.scale(sky_surface, (800, 400))

ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
ground_surface = pygame.transform.scale(ground_surface, (800, 800))


# Intro Screen
player_stand = pygame.image.load('graphics/mario.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1.1)
player_stand_rect = player_stand.get_rect(center = (400,200))

title_surface = test_font.render('Ultimate Runner', False, (64,64,64))
title_rect = title_surface.get_rect(midtop = (400, 30))

message_surface = test_font.render('Press spacebar to play', False, (64,64,64))
message_rect = message_surface.get_rect(midtop = (400, 340))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

goomba_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(goomba_animation_timer, 170)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #goomba_rect.left = 800
                start_time = pygame.time.get_ticks()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bullet', 'goomba', 'goomba'])))
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,-100))

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
    else:
        screen.fill((70,153,201))
        screen.blit(player_stand, player_stand_rect)
        player_stand_rect.midbottom = (400, 300)

        score_message = test_font.render(f'Last Score: {int(score/1000)}', False, (64,64,64))
        score_message_rect = score_message.get_rect(midtop = (400, 340))
        screen.blit(title_surface, title_rect)

        if score == 0:
            screen.blit(message_surface, message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
