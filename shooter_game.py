#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer


win_w = 700
win_h = 500
class GameSprite(sprite.Sprite):
    def __init__(self,p_im,p_x,p_y,p_s,p_h,p_w):
        super().__init__()
        self.image = transform.scale(image.load(p_im),(p_h,p_w))
        self.speed = p_s
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 20:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
    def fire(self):
        kick = mixer.Sound("fire.ogg")
        kick.play()
        bullet = Bullet("bullet.png",self.rect.centerx-10,self.rect.top,-10,30,30)
        Bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y<0:
            self.kill

class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost
        if self.rect.y>500:
            self.rect.y = 0
            self.rect.x = randint(10,620)
            lost = lost +1

window = display.set_mode((win_w,win_h))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"),(700,500))
hero = Player("rocket.png", 5, 400, 4, 50, 100)
monsters = sprite.Group()
Bullets = sprite.Group()
for i in range (5):
    monster = Enemy("ufo.png", randint(10,620),0,randint(1,5),70,70)
    monsters.add(monster)
font.init()
font1 = font.SysFont(None,36)
clock = time.Clock()
mixer.init()
fps = 60
finish = False
game = True
lost = 0
score = 0
bullets = sprite.Group()
num_fire = 0
rec_time=0
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rec_time == False:
                    num_fire = num_fire + 1
                    hero.fire()
                elif num_fire >=5 and rec_time == False:
                    last_time = timer()
                    rec_time = True
    if finish != True:
        window.blit(background,(0,0))
        hero.update()
        hero.reset()
        text_lose = font1.render("Пропущено"+str(lost),1,(255,255,255))
        text_score = font1.render("Счет"+str(score),1,(255,255,255))
        window.blit(text_lose,(10,50))
        window.blit(text_score,(30,70))
        monsters.draw(window)
        monsters.update()
        Bullets.draw(window)
        Bullets.update()
    display.update()
    clock.tick(fps)



