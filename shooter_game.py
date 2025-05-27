#Create your own shooter

from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((700, 500))
display.set_caption("SHOOTER GAME")
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, mode):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.mode = mode

    def update(self):
        if self.mode == 0:
            self.rect.y += self.speed
        else:
            self.rect.y += self.speed
            if self.rect.x < win_width- 100:
                self.rect.x += self.speed


        global lost    
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y<0:
            self.kill() 

background = transform.scale(image.load("galaxy.jpg"), (700, 500))
win_width = 700
win_height = 500
lost = 0

bullets = sprite.Group()
hero = Player('rocket.png',5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
img_bullet = 'bullet.png'
for i in range (1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80),-40, 80, 50, randint(1,2), randint(0,1))
    monsters.add(monster)
asteroids=sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(30,win_width - 30), -40, 80, 50, randint(1,3),randint(0,1))
    asteroids.add(asteroid)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
speed = 10

run = True
clock = time.Clock()
FPS = 40

finish = False
max_lost = 3000 
goal = 100
font.init()
font = font.Font(None, 35)
win = font.render("YOU WIN!", True, (255, 215, 0))
lose = font.render("YOU LOSE", True, (180,0,0))
score = 0
lost = 0
num_fire = 0
life = 100000
rel_time = False
life_color = (0,150,0)
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire< 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    hero.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True        
    if finish != True:
        window.blit(background,(0,0))
        hero.update()
        hero.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time <1:
                reload = font.render(' Wait, reload........',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
        text = font.render("Score: " + str(score), 1,(255,255,255))
        window.blit(text, (10,20))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1,4), randint(1, 2))
            monsters.add(monster)

        if sprite.spritecollide(hero, monsters, False):
            life -= 1
        if life <=0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        if score >= goal:
            finish = True
            window.blit(win,(200,200))
        text = font.render("missed: " + str(lost), 1,(255,255,255))
        window.blit(text, (10,50))

        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
        
        text_life = font.render(str(life), 1, life_color)
        window.blit(text_life,(650,10))

    display.update()
    clock.tick(FPS)