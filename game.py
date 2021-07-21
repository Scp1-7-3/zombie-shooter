from pygame import *
from random import *
font.init()
font2 = font.SysFont('Arial', 36)
mixer.init()
game = True
clock = time.Clock()
FPS = 120
win = display.set_mode((1000, 700))
display.set_caption("game")
place = transform.scale(image.load('place.png'),(1000,700))
cooldown = 0
cooldownr = 0
cheat = 0

class GameSprite(sprite.Sprite):
    def __init__(self, gamer_image,gamer_x, gamer_y, gamer_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(gamer_image),(size_x,size_y))
        self.speed = gamer_speed
        self.rect = self.image.get_rect()
        self.rect.x = gamer_x
        self.rect.y = gamer_y
    def reset(self):
        win.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_UP] and self.rect.y >= 108:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y <= 592:
            self.rect.y += self.speed

        global shoots
        global cooldown
        global cheat
    
        if not cooldown:
            if key_pressed[K_SPACE] and shoots !=0:
                shoot()
                cooldown = 10
            if cheat !=1:
                if len(bullets) >= 3:
                    cooldown = 100
                else:
                    cooldown = 10

            if key_pressed[K_c]:
                cooldown = 0
                shoots = 9999999
                cheat = 1
        else:
            cooldown -= 1
        global cooldownr
        if shoots == 0:
            
            if not cooldownr:
                shoots = 25
                
                cooldownr = 350

            else:
                text = font2.render("Перезарядка " + str(cooldownr // 100) , 1, (254, 195, 2))
                win.blit(text, (600, 20))
                cooldownr -= 1

            
        




        if self.rect.y == 108:
            shoots = 25 

class Bullet(GameSprite):
    def update(self):
        self.rect.x = self.rect.x - 10
        if self.rect.x <= 0:
            self.kill()

shoots = 0

def shoot():
    bullet = Bullet('bullet.png', turrel.rect.x-10, turrel.rect.y+15,10, 30, 15)
    bullets.add(bullet)
    global shoots
    shoots = shoots - 1



class Zombie(GameSprite):
    def update(self):
        self.rect.x = self.rect.x + 1
        sprite_list1 = sprite.groupcollide(zombies, bullets, True, True)

        if self.rect.x >= 1000:
            self.kill()
zombies = sprite.Group()
bullets = sprite.Group()




turrel = Player('turrel.png', 860, 400,2, 138, 108)

while game:
    clock.tick(FPS)
    win.blit(place,(0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    text = font2.render("Заряды " + str(shoots) , 1, (254, 195, 2))
    win.blit(text, (300, 20))
    if len(zombies) <= 10:
        zombie = Zombie('zombie.png', randint(-120, -10), randint(200, 600), randint(1, 10), 60, 70)
        zombies.add(zombie)
    text2  = font2.render("+ПАТРОНЫ", 1,(0,0,0))
    win.blit(text2,(760,160))
    turrel.reset()
    turrel.update()
    bullets.update()
    bullets.draw(win)
    zombies.update()
    zombies.draw(win)
    display.update()
    
