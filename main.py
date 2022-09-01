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

player = Player(pygame.image.load("Data/Basement_Kid.png"), 450, 700)
group = pygame.sprite.Group()
group.add(player)

while running:  
    screen.fill((221,221,221))

    key_pressed = pygame.key.get_pressed()
    group.update(key_pressed)
    group.draw(screen)#surface


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
