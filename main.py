from random import randint
import pygame, sys
from pygame.locals import *

pygame.mixer.pre_init(44100,-16 ,2 ,512)
pygame.init()
pygame.mixer.set_num_channels(32)

screen = pygame.display.set_mode((900, 640), 0, 32)
playspace = pygame.Surface((500, 600))
fpsclock = pygame.time.Clock()

ico = pygame.image.load("Data/cheeze.png")
pygame.display.set_caption("ITS FALLING CHEEEZ")
pygame.display.set_icon(ico)

class Background(): #a
      def __init__(self, image, scroll_speed):
            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect()
 
            self.y = -self.rect.height
            self.x = 0
 
            self.y2 = 0
            self.x2 = 0
 
            self.moving_speed = scroll_speed
         
      def update(self):
        self.y += self.moving_speed
        self.y2 += self.moving_speed

        if self.y2 >= self.rect.height:
            self.y = -self.rect.height
            self.y2 = 0
             
      def render(self, render_to):
         render_to.blit(self.image, (self.x, self.y))
         render_to.blit(self.image, (self.x2, self.y2))

class Button(): #Can be improved, continue work below
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = pygame.image.load(image)
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

#class Button():
#    def __init__(self, default_image, hovering_image , pos, text_input, font, default_colour, hovering_colour):
#        self.default_image = default_image
#        self.hovering_image = hovering_image
#        self.x_pos = pos[0]
#        self.y_pos = pos[1]
#        self.font = font
#        self.default_colour, self.hovering_colour = default_colour, hovering_colour
#        self.text_input = text_input
#        self.text = self.font.render(self.text_input, True, self.default_colour)
#        if self.image is None:
#            self.image = self.text
#        #self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
#        #self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
#        #ADD IMAGES FOR HOVER AND CLICK , AND COLOUR FOR CLICK
        
        

class font():
    def __init__(self, font_path, size_pt, INSERT_TEXT, colour):
        self.font = pygame.font.Font(font_path, size_pt)
        self.textimg = self.font.render(INSERT_TEXT, True, colour)

    def render_text(self, render_to , x_cordinatez, y_cordinatez):
        render_to.blit(self.textimg, (x_cordinatez, y_cordinatez))

class Player(pygame.sprite.Sprite):
    def __init__(self, image , x, y, health): 
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image),(24, 45)) #only arg is just the the path of the source
        self.rect = self.image.get_rect() #the self in the beginning helps makes the whole process easier
        self.spawn_x = x
        self.spawn_y = y
        self.rect.x = x
        self.rect.y = y
        self.rect.center = [x,y]
        self.last_shot = pygame.time.get_ticks()

    def update(self):

        key = pygame.key.get_pressed()
        shot_cooldown = 100 #ms

        cur_time = pygame.time.get_ticks()

           #check for shoot
        if key[pygame.K_z] and cur_time - self.last_shot > shot_cooldown:
            pewpewsound.play()
            bullet = Player_Bullet(self.rect.centerx, self.rect.top)
            bulletgroup.add(bullet)
            self.last_shot = cur_time
            print("shooting")

        speed = 5
        if key[pygame.K_LSHIFT]:
            speed -= 2.5
        if key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= speed
            print("UP")
        if key[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += speed
            print("DOWN")
        if key[pygame.K_RIGHT] and self.rect.right < 500:
            self.rect.x += speed
            print("RIGHT")
        if key[pygame.K_LEFT] and self.rect. left > 0:
            self.rect.x -= speed
            print("LEFT")

        if self.rect.colliderect(cheez1.rect) or self.rect.colliderect(coffee1.rect) or self.rect.colliderect(coffee2.rect) : #OBJECT DEPENDANT(THE RECTS SHOULD ME THE ENEMIES) also not the best implementation.. rework later
            if cheez1.alive() == True or coffee1.alive() == True or coffee2.alive() == True :
                print("PLAYER COLLIDE W/ENEMY")
                #get a EXPLOSION >:o
                self.rect.x = self.spawn_x
                self.rect.y = self.spawn_y
                lost()


class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Data/player_bullet1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 8 #speed of bullets movement
        if self.rect.colliderect(cheez1.rect) or self.rect.colliderect(cheez2.rect) or self.rect.colliderect(cheez3.rect)or self.rect.colliderect(cheez4.rect) or self.rect.colliderect(cheez5.rect)or self.rect.colliderect(coffee1.rect) or self.rect.colliderect(coffee2.rect) or self.rect.colliderect(coffee3.rect) : #OBJECT DEPENDANT(THE RECTS SHOULD ME THE ENEMIES) also not the best implementation.. rework later
            if cheez1.alive() == True or coffee1.alive() == True or coffee2.alive() == True :
                print("BULLET COLLIDE")
                self.kill()
                enemyshotsound.play()

class cheeze(pygame.sprite.Sprite):
    def __init__(self, image, speed):##, x, y):
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
        
        if self.rect.colliderect(player.rect): #OBJECT DEPENDANT (ARGUMENT SHLOULD BE THE INSTANCE NAME FOLLOWED BY ATTRIBUTE)
            print("COLLIDED")
            #self.kill()

class cookie(pygame.sprite.Sprite):
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
            #self.kill()
            self.rect.x = randint(-50, playspace.get_width())#
            self.rect.y = -40

class coffee(pygame.sprite.Sprite):
    def __init__(self, image, speed, x, y, mode): #MODE 1: Left to Right, Mode 2: Right to left
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.spawn_x = x
        self.spawn_y = y
        self.rect.x = x
        self.rect.y = y
        self.t = 0
        self.speed = speed
        self.mode = mode  

    def update(self):
        self.t += 1/60
        if self.mode == 1:
            self.rect.y += self.speed
            self.rect.x += self.speed
        if self.mode == 2:
            self.rect.y += randint(1, 4)#self.speed
            self.rect.x -= randint(1, 13)#self.speed

        if self.rect.y >= 610 and self.mode == 1:
            self.rect.x = randint(-70,-50)
            self.rect.y = randint(-5, 260)

        if self.rect.y >= 610 and self.mode == 2:
            self.rect.x = randint(600, 620)
            self.rect.y = randint(-5, 260)

        if self.rect.colliderect(player.rect): #OBJECT DEPENDANT (ARGUMENT SHLOULD BE THE INSTANCE NAME FOLLOWED BY ATTRIBUTE)
            print("COLLIDED COFFEE ")
            self.kill()
                
#VARIABLES AND INSTANCES FOR playing() START

#sounds and muse
pewpewsound = pygame.mixer.Sound("Data/mal_shoot.wav")
enemyshotsound = pygame.mixer.Sound("Data/shot.wav")
enemyshotsound.set_volume(0.1)
pewpewsound.set_volume(0.008)
pygame.mixer.music.load("Data/my_sweet_dreams.wav")
pygame.mixer.music.set_volume(0.09)
pygame.mixer.music.play(-1)
pink_star_layer = Background("Data/Pink star.png", 5.25*1.5)
lighter_purple_star_layer = Background("Data/light_purple_star.png", 3*1.5)
indigo_star_layer = Background("Data/Indigo_star.png", 2.25*1.5)


txttempnumbers = font("Data/OLDENGL.TTF", 20, "000000", (192, 192, 192))
txtscore = font("Data/l_10646.ttf", 20, "Score", (192, 192, 192))
txtlife = font("Data/l_10646.ttf", 20, "Life", (192, 192, 192))
arcade_mode = font("Data/l_10646.ttf", 25, "Arcade Mode", (192, 192, 192))

player = Player("Data/New_Kid.png", playspace.get_width()/2, 500, 3)
playergroup = pygame.sprite.Group()
playergroup.add(player)

bulletgroup = pygame.sprite.Group()

#ENEMY
cheez_group = pygame.sprite.Group()
cheez1 = cheeze("Data/cheeze.png", randint(2, 7))
cheez2 = cheeze("Data/cheeze.png", randint(2, 7))
cheez3 = cheeze("Data/cheeze.png", randint(2, 7))
cheez4 = cheeze("Data/cheeze.png", randint(2, 7))
cheez5 = cheeze("Data/cheeze.png", randint(2, 7))
cheez_group.add(cheez1,cheez2,cheez3,cheez4,cheez5)

coffee_group = pygame.sprite.Group()
coffee1 = coffee("Data/Coffee.png", 2, randint(600, 620), randint(-5, 260), 2)
coffee2 = coffee("Data/Coffee.png", 5, randint(-70,-50), 10, 1)
coffee3 = coffee("Data/Coffee.png", 3, randint(-100,-50), randint(-5, 200), 2)
coffee_group.add(coffee1,coffee2,coffee3)

#VARIABLES AND INSTANCES FOR playing() END!
#................................................
#VARIABLES AND INSTANCES FOR mainmenu() START
title_screen_and_bg = pygame.image.load("Data/MENU BG1.png") #these two are just images of 900 x 600 they are not 900x640, make the text and stars different layers later, and maybe a lil animation too (x_x)
alt_title_screen_and_bg = pygame.image.load("Data/MENU BG2.png")
START_BUTTON = Button("Data/buttonimage.png", (260, 377), "Start", pygame.font.Font("Data/l_10646.ttf", 35), (234, 146, 171), (175, 127, 194))#estimated pos
QUIT_BUTTON = Button("Data/buttonimage.png", (300, 450), "Quit", pygame.font.Font("Data/l_10646.ttf", 35), (234, 146, 171), (175, 127, 194))#estimated pos
#VARIABLES AND INSTANCES FOR mainmenu() END
#................................................
#VARIABLES AND INSTANCES FOR lost() START
ded = font("Data/l_10646.ttf", 50, "You lost", (255,255,255))
ded_bg = pygame.image.load("Data/youlost.png")
#VARIABLES AND INSTANCES FOR lost() END

def playing():
    while True:
        screen.fill((50, 50, 50))
        screen.blit(playspace, [20, 20])
        playspace.fill((74,66,84)) #use 221 if check
        #score
        txtscore.render_text(screen, 550, 100)
        txttempnumbers.render_text(screen, 610, 104)#add another text object to be the numbers and add a func to update th numbers to the class
        txtlife.render_text(screen, 550, 200)
        arcade_mode.render_text(screen, 640, 20)

        #background layers
        pink_star_layer.update()
        lighter_purple_star_layer.update()
        indigo_star_layer.update()
        #
        pink_star_layer.render(playspace)
        lighter_purple_star_layer.render(playspace)
        indigo_star_layer.render(playspace)

        #player
        playergroup.update()
        playergroup.draw(playspace)#surface

        #enemies
        cheez_group.draw(playspace)
        cheez_group.update()

        coffee_group.draw(playspace)
        coffee_group.update()    

        #player bullets
        bulletgroup.draw(playspace)
        bulletgroup.update()



        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                mainmenu()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos = event.pos[0]
                ypos = event.pos[1]
                if event.button == 1:
                    print(f"X = {xpos}\nY = {ypos}\n...\n")

        pygame.display.update()
        fpsclock.tick(60)

def mainmenu():
    while True:
        screen.fill((0, 0, 36)) #colour of the background image backgrounds
        screen.blit(alt_title_screen_and_bg,(0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        #insert BUTTONS here 
        for button in [START_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        #    
        
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if key[pygame.K_p]:
                playing()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos = event.pos[0]
                ypos = event.pos[1]
                if event.button == 1:
                    print(f"X = {xpos}\nY = {ypos}\n...\n")
            #
                if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playing()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            #


        pygame.display.update()
        fpsclock.tick(60)

def lost(): #currently behaves exactly like a PAUSE need to figure out how to reset playing() when this "function" is called
    while True:
        screen.fill((0, 0, 36)) #colour of the background image backgrounds
        screen.blit(ded_bg, (0,10)) #<-- finish this
        ded.render_text(ded_bg, ded_bg.get_width()/2 - 100, 30)

        LOST_MOUSE_POS = pygame.mouse.get_pos()

        #insert BUTTONS here  
        RESTART_BUTTON = Button("Data/buttonimage.png", (450, 377), "Restart", pygame.font.Font("Data/l_10646.ttf", 35), (234, 146, 171), (175, 127, 194))#estimated pos
        QUIT_BUTTON = Button("Data/buttonimage.png", (450, 477), "Quit", pygame.font.Font("Data/l_10646.ttf", 35), (234, 146, 171), (175, 127, 194))#estimated pos
         
        #
        for button in [RESTART_BUTTON, QUIT_BUTTON]:
            button.changeColor(LOST_MOUSE_POS)
            button.update(screen)
        #    
        
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if key[pygame.K_p]:
                playing()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                xpos = event.pos[0]
                ypos = event.pos[1]
                if event.button == 1:
                    print(f"X = {xpos}\nY = {ypos}\n...\n")
            #
                if RESTART_BUTTON.checkForInput(LOST_MOUSE_POS):
                    playing()
                if QUIT_BUTTON.checkForInput(LOST_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            #


        pygame.display.update()
        fpsclock.tick(60)


mainmenu()

#TMR MAKE THE LOST RESET and also reset loc of enemies when shot could be used
#MAKE BULLET SLOW ENEMY
#FAST CLOCK = SCORE
#explosion sound lmms when she explode
