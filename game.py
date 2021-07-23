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
cheater = 0
death = 0
score = 0
finish = False
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

    def update(self):
        if sprite.spritecollide(zombie, self, False):
            turret.kill()
class Player(GameSprite):
    def update(self):
        if not finish:
            key_pressed = key.get_pressed()
            if key_pressed[K_UP] and self.rect.y >= 108:
                self.rect.y -= self.speed
            if key_pressed[K_DOWN] and self.rect.y <= 592:
                self.rect.y += self.speed

            global shoots
            global cooldown
            global cheat
            global cheater
            if key_pressed[K_c]:
                cheat = 1 
                cheater = 1
                
            if not cooldown:
                if cheat ==1:
                    shoots = 9999999999999999
                    if key_pressed[K_SPACE] and shoots !=0:
                        shoot()
                        cooldown = 0
                else:
                    if key_pressed[K_SPACE] and shoots !=0:
                        shoot()
                        cooldown = 10
            
                    if len(bullets) >= 3:
                        cooldown = 100
                    else:
                        cooldown = 10
                    
            else:
                cooldown -= 1
            global cooldownr
            if shoots == 0:
                
                if not cooldownr:
                    shoots = 25
                    
                    cooldownr = 350

                else:
                    text = font2.render("Перезарядка " + str(cooldownr // 100) , 1, (254, 195, 2))
                    win.blit(text, (530, 20))
                    cooldownr -= 1

            
    

            if self.rect.y <= 108:
                shoots = 25 
                cheat = 0

class Bullet(GameSprite):
    if not finish:
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
        if not finish:
            self.rect.x = self.rect.x + 1
            sprite_list1 = sprite.groupcollide(zombies, bullets, True, True)
            global score
            if sprite_list1:
                score = score + 1
                
            if self.rect.x >= 1000:
                self.kill()
            global death
            if self.rect.x >= 800:
                death = death + 1
                self.kill()
        



zombies = sprite.Group() 
bullets = sprite.Group()
turrel = Player('turrel.png', 600, 400,3, 138, 108)




while game:
    clock.tick(FPS)
    win.blit(place,(0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    text = font2.render("Заряды " + str(shoots) , 1, (254, 195, 2))
    win.blit(text, (280, 20))
    if len(zombies) < 8:
        zombie = Zombie('zombie.png', randint(-200, -100), randint(200, 600), randint(1, 100), 60, 80)
        zombies.add(zombie)
    text2  = font2.render("+ПАТРОНЫ", 1,(0,0,0))
    win.blit(text2,(580,160))
    if death == 0:
            house_full = transform.scale(image.load('house_full.png'),(200,650))
            win.blit(house_full,(800,10))
    elif death == 1:
        
        house_half = transform.scale(image.load('house_half.png'),(200,650))
        win.blit(house_half,(800,10))
    elif death == 2:
        house_dead = transform.scale(image.load('house_dead.png'),(200,650))
        win.blit(house_dead,(800,10))
        finish = True
    
    if finish == True:
        text2  = font2.render("Ты проиграл", 1,(171, 44, 44))
        win.blit(text2,(400,370))
        if cheater == 1:
            text2  = font2.render("Очки: ЧИТЕР", 1,(122, 15, 15))
            win.blit(text2,(400,440))
        else:
            text2  = font2.render("Очки: "+str(score), 1,(189, 207, 27))
            win.blit(text2,(440,440))
        
    turrel.reset()
    turrel.update()
    bullets.update()
    bullets.draw(win)
    zombies.update()
    zombies.draw(win)
    
    display.update()
    
