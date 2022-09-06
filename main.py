from random import randint
import pygame
from pygame.locals import *

pygame.init()

playspace = pygame.Surface((500, 600))
screen = pygame.display.set_mode((900, 640), 0, 32)
running = True
fpsclock = pygame.time.Clock()
pygame.display.set_caption("Poggers")

class Player(pygame.sprite.Sprite):
    def __init__(self, image , x, y): 
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, key):
        speed = 5
        if key[pygame.K_LSHIFT]:
            speed -= 2.5

        if key[pygame.K_UP]:
            self.rect.y -= speed
            print("UP")

        if key[pygame.K_DOWN]:
            self.rect.y += speed
            print("DOWN")
        if key[pygame.K_RIGHT]:
            self.rect.x += speed
            print("RIGHT")
        if key[pygame.K_LEFT]:
            self.rect.x -= speed
            print("LEFT")


class cheeze(pygame.sprite.Sprite):
    def __init__(self, image):#, x, y):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        #self.x = x
        #self.y = y
        self.t = 0

    def update(self):
        self.t += 1/60
        self.rect.y += 8

        if self.rect.y >= 600:
            self.rect.x = randint(0, playspace.get_width())
            self.rect.y = -40
#bgstuff
class background(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.t = 0

    
    def update(self, no):
        if no == 1:
            self.t += 1/60
            self.rect.y += 2

            if self.rect.y >= 600:
                self.rect.y = -1
            
        if no == 2:
            self.t += 1/60
            self.rect.y += 2

            if self.rect.y >= 1:
                self.rect.y = -600

        
                 
bg1 = background(pygame.image.load("Data/feild.png"))
player = Player(pygame.image.load("Data/Basement_Kid.png"), playspace.get_width()/2-35, 500)

bggroup = pygame.sprite.Group()
bggroup.add(bg1)
bggroup2 = pygame.sprite.Group()
bggroup2.add(bg1)

group = pygame.sprite.Group()
group.add(player)

cheez_group = pygame.sprite.Group()
for cheez in range (20):
    chez = cheeze(pygame.image.load("Data/cheeze.png"))#, randint(0, 900), 0)
    cheez_group.add(chez)

while running:
    screen.fill((50, 50, 50))
    screen.blit(playspace, [20, 20])
    playspace.fill((221,221,221))

    key_pressed = pygame.key.get_pressed()
    bggroup.draw(playspace)
    bggroup.update(1)
    bggroup2.update(2)
    
    group.update(key_pressed)
    group.draw(playspace)#surface
    cheez_group.draw(playspace)
    cheez_group.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            xpos = event.pos[0]
            ypos = event.pos[1]
            if event.button == 1:
                print(f"X = {xpos}\nY = {ypos}\n...\n")

    


    pygame.display.update()
    fpsclock.tick(60)
