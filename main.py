from random import randint
import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((900, 640), 0, 32)
playspace = pygame.Surface((500, 600))
running = True
fpsclock = pygame.time.Clock()

ico = pygame.image.load("Data/cheeze.png")
pygame.display.set_caption("ITS FALLING CHEEEZ")
pygame.display.set_icon(ico)

class Background(): #a
      def __init__(self, image, scorll_spiid):
            self.bgimage = pygame.image.load(image)
            self.rectBGimg = self.bgimage.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = self.rectBGimg.height
            self.bgX2 = 0
 
            self.moving_speed = scorll_spiid
         
      def update(self):
        self.bgY1 -= self.moving_speed
        self.bgY2 -= self.moving_speed
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height
             
      def render(self, render_to):
         render_to.blit(self.bgimage, (self.bgX1, self.bgY1))
         render_to.blit(self.bgimage, (self.bgX2, self.bgY2))


class font():
    def __init__(self, font_path, size_pt, INSERT_TEXT, colour):
        self.font = pygame.font.Font(font_path, size_pt)
        self.textimg = self.font.render(INSERT_TEXT, True, colour)

    def render_text(self, render_to , x_cordinatez, y_cordinatez):
        render_to.blit(self.textimg, (x_cordinatez, y_cordinatez))


class Player(pygame.sprite.Sprite):
    def __init__(self, image , x, y): 
        super().__init__()
        self.image = pygame.image.load(image) #only arg is just the the path of the source
        self.rect = self.image.get_rect() #the self in the beginning helps makes the whole process easier
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
    def __init__(self, image, speed):#, x, y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        #self.x = x
        #self.y = y
        self.t = 0
        self.speed = speed

    def update(self):
        self.t += 1/60
        self.rect.y += self.speed

        if self.rect.y >= 610:
            self.rect.x = randint(-50, playspace.get_width())#
            self.rect.y = -40

class coffee(pygame.sprite.Sprite):
    def __init__(self, image, speed):#, x, y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        #self.x = x
        #self.y = y
        self.t = 0
        self.speed = speed

    def draw(self, surface, x, y):
        self.x = x
        self.y = y
        surface.blit(self.image, (x, y))
        

    def update(self, MODE):
        self.t += 1/60
        if MODE == 1:
            self.rect.y += self.speed
            self.rect.x += self.speed
        if MODE == 2:
            self.rect.y += self.speed
            self.rect.x -= self.speed

        if self.rect.y >= 610:
            self.rect.x = 1
            self.rect.y = 40


bg1 = Background("Data/space.png", 1.5)


txttempnumbers = font("Data/OLDENGL.TTF", 20, "000000", (192, 192, 192))
txtscore = font("Data/l_10646.ttf", 20, "Score", (192, 192, 192))
txtlife = font("Data/l_10646.ttf", 20, "Life", (192, 192, 192))

player = Player("Data/New_Kid.png", playspace.get_width()/2-35, 500)
playergroup = pygame.sprite.Group()
playergroup.add(player)

#ENEMY
cheez_group = pygame.sprite.Group()
chez = cheeze("Data/cheeze.png", 3.5)
cheez_group.add(chez)

cofe = coffee("Data/Coffee.png", 4)
coffee_group = pygame.sprite.Group()
coffee_group.add(cofe)


while running:
    screen.fill((50, 50, 50))
    screen.blit(playspace, [20, 20])
    playspace.fill((221,221,221))

    txtscore.render_text(screen, 550, 100)
    txttempnumbers.render_text(screen, 610, 104)#add another text object to be the numbers and add a func to update th numbers to the class
    txtlife.render_text(screen, 550, 200)
    
    bg1.update()
    bg1.render(playspace)

    key_pressed = pygame.key.get_pressed()    
    playergroup.update(key_pressed)
    playergroup.draw(playspace)#surface
    cheez_group.draw(playspace)
    cheez_group.update()
    coffee_group.draw(playspace) #takes two but 4 where given when (playspace, number, number)
    coffee_group.update(1)    


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
