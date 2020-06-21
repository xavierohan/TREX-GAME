import numpy
import pygame

import random
import os
import random
import time

pygame.init()
gg =0

WIN_WIDTH = 800 + gg  # 600
WIN_HEIGHT = 800
font = pygame.font.SysFont("comicsansms", 30, True)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("TREX GAME")

bird_imgs = [pygame.image.load(os.path.join("imgs", "bird.png")), pygame.image.load(os.path.join("imgs", "bird2.png"))]
cactus_imgs = [pygame.image.load(os.path.join("imgs", "cactusSmall.png")),
               pygame.image.load(os.path.join("imgs", "cactusBig.png")),
               pygame.image.load(os.path.join("imgs", "cactusSmallMany.png"))]
dino_img = pygame.image.load(os.path.join("imgs", "dino.png"))
dino_dead_img = pygame.image.load(os.path.join("imgs", "dinoDead.png"))
dino_duck_imgs = [pygame.image.load(os.path.join("imgs", "dinoduck1.png")),
                  pygame.image.load(os.path.join("imgs", "dinoduck2.png"))]
dino_run_imgs = [pygame.image.load(os.path.join("imgs", "dinorun1.png")),
                 pygame.image.load(os.path.join("imgs", "dinorun2.png"))]
dino_jump_img = pygame.image.load(os.path.join("imgs", "dinoJump.png"))

obstacle_imgs = cactus_imgs
hitbox_outline = 255  # 255 to get the the outline

clock = pygame.time.Clock()
score = 0


class Dino:
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.tick_count = 0
        self.height = self.y
        self.img_count = 0
        self.img = dino_img
        self.jumpcount = 12.5
        self.isjump = False
        self.duck = False
        self.run = True

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def draw(self):
        if self.run:

            self.img_count += 1

            if self.img_count <= self.ANIMATION_TIME:
                self.img = dino_run_imgs[0]
            elif self.img_count <= self.ANIMATION_TIME * 2:
                self.img = dino_run_imgs[1]
                self.img_count = 0

        elif self.duck:
            self.img_count += 1
            if self.img_count <= self.ANIMATION_TIME:
                self.img = dino_duck_imgs[0]
            elif self.img_count <= self.ANIMATION_TIME * 2:
                self.img = dino_duck_imgs[1]
                self.img_count = 0

        elif self.isjump:
            self.img = dino_jump_img


class Cactus:
    vel = 12

    def __init__(self, x):
        self.x = x
        self.small = cactus_imgs[0]
        self.many = cactus_imgs[2]
        self.passed = False
        self.obstacles = obstacle_imgs
        self.index = random.randint(0, 2)
        self.img = cactus_imgs[0]
        self.random_dist = random.randrange(-100+gg, 100+gg, 20+gg)

    def move(self, score):
        if score < 10:
            self.vel = 13
        elif 10 <= score < 20:
            self.vel = 18
        elif 20 <= score < 30:
            self.vel = 24
        elif 30 <= score < 40:
            self.vel = 28
        else:
            self.vel = 32
        self.x -= self.vel

    def draw(self, win):

        if self.index == 0:
            win.blit(self.obstacles[0], (self.x + self.random_dist + 200 + gg, 530))

        elif self.index == 1:
            win.blit(self.obstacles[1], (self.x + self.random_dist + 200 + gg, 490))

        else:
            win.blit(self.obstacles[2], (self.x + self.random_dist + 200 + gg, 530))

    def collide(self):
        if self.index == 0:
            j_hitbox = (self.x + self.random_dist + 200 + gg + 15, 520, 10, 80)
            h = pygame.draw.rect(win, (hitbox_outline, 0, 0), j_hitbox, 2)
        elif self.index == 1:
            j_hitbox = (self.x + self.random_dist + 200 + gg + 15, 500, 30, 100)
            h = pygame.draw.rect(win, (hitbox_outline, 0, 0), j_hitbox, 2)
        else:
            j_hitbox = (self.x + self.random_dist + 200 + gg + 25, 520, 60, 80)
            h = pygame.draw.rect(win, (hitbox_outline, 0, 0), j_hitbox, 2)
        return h


class Bird:
    vel = 5
    ANIMATION_TIME = 6

    def __init__(self, x):
        self.x = x
        self.imgs = bird_imgs
        self.passed = False
        self.img_count = 0
        self.img = bird_imgs[0]

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        self.img_count += 1
        if self.img_count <= self.ANIMATION_TIME:
            self.img = bird_imgs[0]

        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = bird_imgs[1]
            self.img_count = 0


class Bul:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def game_intro(top_score):
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    win.fill((255, 255, 255))
    win_text = font.render("TREX GAME  ", 1, (0, 0, 0))
    top_score_text = font.render("HIGH SCORE: " + str(top_score), 1, (0, 0, 0))
    instructions = font.render("Jump-SPACEBAR || Bullet-S || ENTER - TO PLAY", 1, (0, 0, 0))
    win.blit(top_score_text, (0, 0))
    win.blit(instructions, (20, 400))
    win.blit(win_text, (200 + 100, 250))
    win.blit(bird_imgs[0], (480 + 200, 530))
    win.blit(cactus_imgs[0], (280 + 100, 580))
    win.blit(dino_run_imgs[0], (80, 550))
    pygame.draw.line(win, (0, 0, 0), (0, 660),
                     (WIN_WIDTH, 660))
    pygame.display.update()
    clock.tick(15)

    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_q:
                pygame.quit()
                exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()


top_score = 0


def main(top_score):
    dino = Dino(100, 500)
    cac = [Cactus(800)]
    bird = Bird(850)
    vel = 5
    m = 1
    run = True
    intro = True
    clk = pygame.time.Clock()
    k = 5
    bullets = []
    not_hit = True
    collide = False
    score = 0

    while run:

        if score > top_score:
            top_score = score

        if intro:
            game_intro(top_score)
            pygame.time.delay(1500)
            intro = False

        clk.tick(40)

        pygame.draw.line(win, (255, 255, 255), (0, 610),
                         (WIN_WIDTH, 610))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if dino.run:
            dino_hitbox = (dino.x, dino.y + 10, 80, 90)
            r = pygame.draw.rect(win, (hitbox_outline, 0, 0), dino_hitbox, 2)
            dino.duck = False
            dino.isjump = False
            dino.draw()
            win.blit(dino.img, (100, 500))

            if keys[pygame.K_SPACE]:
                dino.isjump = True
                dino.run = False
            elif keys[pygame.K_a]:
                dino.duck = True
                dino.run = False
            elif keys[pygame.K_s]:
                if len(bullets) < 1:
                    bullets.append(Bul(dino.x + 95, 520, 6, (255, 255, 255,)))

        for i in bullets:
            if 800+gg > i.x > 0:
                i.x += i.vel
                bullet_hitbox = (i.x - 10, i.y - 10, 20, 20)
                bullet_rect = pygame.draw.rect(win, (hitbox_outline, 0, 0), bullet_hitbox, 2)
                if bird.passed:
                    if bullet_rect.colliderect(bird_rect):
                        bird.x = dino.x - 50
                        i.x = dino.x - 100
            else:
                bullets.pop(bullets.index(i))
        for q in bullets:
            q.draw(win)

        if dino.isjump:
            dino_hitbox = (dino.x, dino.y + 20, 80, 90)
            r = pygame.draw.rect(win, (hitbox_outline, 0, 0), dino_hitbox, 2)
            dino.run = False
            dino.duck = False
            dino.draw()
            win.blit(dino.img, (dino.x, dino.y))

            if dino.jumpcount >= -12.5:
                neg = 1
                if dino.jumpcount < 0:
                    neg = -1
                dino.y -= (dino.jumpcount ** 2) * 0.5 * neg
                dino.jumpcount -= 1

            else:
                dino.isjump = False
                dino.run = True
                dino.jumpcount = 12.5

        elif dino.duck:
            dino.run = False
            dino.isjump = False
            dino.draw()
            win.blit(dino.img, (dino.x, dino.y + 42))

            dino_hitbox_jump = (dino.x, dino.y + 42, 80, 60)
            f = pygame.draw.rect(win, (hitbox_outline, 0, 0), dino_hitbox_jump, 2)
            if s.colliderect(f):
                collide = True
                # run = False

            if not keys[pygame.K_a]:
                dino.duck = False
                dino.isjump = False
                dino.run = True

        rem = []

        new_cac = False
        for i in cac:
            if not i.passed and i.x+50 < dino.x:
                i.passed = True
                new_cac = True
            if i.x + 600+gg + i.small.get_width() < 0:
                rem.append(i)
            i.move(score)
        if new_cac:
            score += 1
            cac.append(Cactus(800))
        for i in rem:
            cac.remove(i)
        for j in cac:
            s = j.collide()
            if s.colliderect(r):
                collide = True
                # run = False
            if dino.duck:
                if s.colliderect(f):
                    collide = True
                    # run = False
            j.draw(win)

        rem2 = []
        new_bird = False
        bird_dist = random.choice([1000, 2000, 3000, 4000])

        if score > k:
            if bird.x > dino.x - 50:

                bird.passed = True
                bird.move()
                bird.draw(win)
                win.blit(bird.img, (bird.x, 480))
                bird_hitbox = (bird.x + 20, 490, 60, 40)
                bird_rect = pygame.draw.rect(win, (hitbox_outline, 0, 0), bird_hitbox, 2)
                if bird_rect.colliderect(r):
                    collide = True
                    # run = False
            else:
                bird = Bird(dino.x + bird_dist)

        if collide:
            pygame.time.delay(1500)
            win.fill((0, 0, 0))
            if score < top_score :
                msg = font.render(" YOU LOSE, Just GIVE UP Already @_@ " , 2, (255, 255, 255))
            elif score == top_score:
                msg = font.render(" YOU LOSE, -_- ", 2, (255, 255, 255))
            win.blit(msg, (0, 0))
            pygame.display.update()
            pygame.time.delay(2000)
            main(top_score)

        score_text = font.render("Score: " + str(score), 1, (255, 255, 255))
        instructions = font.render("Jump --> SPACEBAR || Duck --> A || Bullet --> S ", 1, (255, 255, 255))
        win.blit(score_text, (0, 0))
        win.blit(instructions, (0, 50))
        pygame.display.update()
        win.fill((0, 0, 0))


main(top_score)
