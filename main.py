from random import randint
import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((900, 800), 0, 32)
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
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.x = x
        self.y = y
        self.t = 0

    def update(self, x, y):
        self.t += 1/60
        self.rect.y += 8
        #self.rect.y = y #REMOVE THIS AND IT WORKS BUT IDK WHY

        if self.rect.y <= 800:
            self.rect.x = randint(0, 900)

            self.rect.x = x
        
        


player = Player(pygame.image.load("Data/Basement_Kid.png"), 450, 700)
group = pygame.sprite.Group()
group.add(player)

cheez_group = pygame.sprite.Group()
for cheez in range (20):
    chez = chez = cheeze(pygame.image.load("Data/cheeze.png"), randint(0, 900), 0)
    cheez_group.add(chez)

while running:  
    screen.fill((221,221,221))

    key_pressed = pygame.key.get_pressed()
    group.update(key_pressed)
    group.draw(screen)#surface
    cheez_group.draw(screen)
    cheez_group.update(chez.rect.x, chez.rect.y)


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
