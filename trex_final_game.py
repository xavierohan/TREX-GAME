import pygame
import neat
# check if i need to install neat-python
import random
import os
import random
import time

pygame.init()
print(pygame.font.get_fonts())

WIN_WIDTH = 600
WIN_HEIGHT = 800
font = pygame.font.SysFont("agencyfb", 30, True)

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
hitbox_outline = 0  # 255 to get the the outline

bullet_sound = pygame.mixer.Sound('bullet.wav')
jump_sound = pygame.mixer.Sound("Jumping-sound-effect.wav")
hit_sound = pygame.mixer.Sound('Retro-game-over-sound-effect.wav')

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

    def __init__(self, x):
        self.x = x
        self.small = cactus_imgs[0]
        self.many = cactus_imgs[2]
        self.passed = False
        self.obstacles = obstacle_imgs
        self.index = random.randint(0, 2)
        self.img = cactus_imgs[0]
        self.random_dist = random.randrange(-200, 100, 40)

    def move(self):
        if score < 20:
            vel = 12
        elif 20 < score < 40:
            vel = 15
        elif 40< score < 60:
            vel = 17
        else:
            vel = 18.5
        self.x -= vel

    def draw(self, win):

        if self.index == 0:
            win.blit(self.obstacles[0], (self.x + self.random_dist, 530))

        elif self.index == 1:
            win.blit(self.obstacles[1], (self.x + self.random_dist, 490))

        else:
            win.blit(self.obstacles[2], (self.x + self.random_dist, 530))

    def collide(self):
        if self.index == 0:
            j_hitbox = (self.x + self.random_dist + 15, 520, 10, 80)
            h = pygame.draw.rect(win, (hitbox_outline, 0, 0), j_hitbox, 2)
        elif self.index == 1:
            j_hitbox = (self.x + self.random_dist + 15, 500, 30, 100)
            h = pygame.draw.rect(win, (hitbox_outline, 0, 0), j_hitbox, 2)
        else:
            j_hitbox = (self.x+ self.random_dist + 25, 520, 60, 80)
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


dino = Dino(100, 500)
cac = [Cactus(700)]
bird = Bird(850)
vel = 5
m = 1
run = True
clk = pygame.time.Clock()
k = 5
bullets = []
not_hit = True

while run:

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
            if len(bullets) < 5:
                bullet_sound.play()
                bullets.append(Bul(dino.x + 95, 520, 6, (255, 255, 255,)))

    for i in bullets:
        if 600 > i.x > 0:
            i.x += i.vel
            bullet_hitbox = (i.x - 10, i.y - 10, 20, 20)
            bullet_rect = pygame.draw.rect(win, (hitbox_outline, 0, 0), bullet_hitbox, 2)
            if bird.passed:
                if bullet_rect.colliderect(bird_rect):
                    bird.x = dino.x - 50


        else:
            bullets.pop(bullets.index(i))
    for q in bullets:
        q.draw(win)

    if dino.isjump:
        #jump_sound.play()
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

        dino_hitbox_jump = (dino.x, dino.y + 50, 80, 60)
        f = pygame.draw.rect(win, (hitbox_outline, 0, 0), dino_hitbox_jump, 2)
        if s.colliderect(f):
            run = False

        if not keys[pygame.K_a]:
            dino.duck = False
            dino.isjump = False
            dino.run = True

    rem = []

    new_cac = False
    for i in cac:
        if not i.passed and i.x < dino.x:
            i.passed = True
            new_cac = True
        if i.x + i.small.get_width() < 0:
            rem.append(i)
        i.move()
    if new_cac:
        score += 1
        cac.append(Cactus(700))
    for i in rem:
        cac.remove(i)
    for j in cac:
        s = j.collide()
        if s.colliderect(r):
            run = False
        if dino.duck:
            if s.colliderect(f):
                run = False
        j.draw(win)

    rem2 = []
    new_bird = False
    bird_dist =  random.choice([1000, 2000, 3000, 4000])

    if score > k:
        if bird.x > dino.x - 50:

            bird.passed = True
            bird.move()
            bird.draw(win)
            win.blit(bird.img, (bird.x, 480))
            bird_hitbox = (bird.x + 20, 490, 60, 40)
            bird_rect = pygame.draw.rect(win, (hitbox_outline, 0, 0), bird_hitbox, 2)
            if bird_rect.colliderect(r):
                run = False
        else:
            bird = Bird(dino.x + bird_dist)

    score_text = font.render("Score: " + str(score), 1, (255, 255, 255))
    instructions = font.render("Jump --> SPACEBAR || Duck --> A || Bullet --> B ", 1, (255, 255, 255))
    win.blit(score_text, (0, 0))
    win.blit(instructions, (0, 50))
    pygame.display.flip()

    win.fill((0, 0, 0))
