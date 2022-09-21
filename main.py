from random import randint
import pygame, sys
from pygame.locals import *

pygame.mixer.pre_init(44100,-16 ,2 ,512)
pygame.init()
pygame.mixer.set_num_channels(32)

screen = pygame.display.set_mode((900, 640), 0, 32)
playspace = pygame.Surface((500, 600))
fpsclock = pygame.time.Clock()

ico = pygame.image.load("Data/cooki.png")
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
        self.hitrect = pygame.rect.Rect(self.rect.x/2 + 12, self.rect.y/2 - 12, 12, 12)
        #self.rect.center = [x,y]
        self.last_shot = pygame.time.get_ticks()
        self.bullet_group = pygame.sprite.Group()
        self.dead = False
        self.shot_cooldown = 100

    def reset(self):
        self.dead = False
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.bullet_group.empty()

    def check_collision(self, enemy_group):
        for b in self.bullet_group.sprites():
            if b.offscreen:
                self.bullet_group.remove(b)

            else:
                for s in enemy_group.sprites():
                    if b.rect.colliderect(s.rect):
                        print(s, "died")
                        enemy_group.remove(s)
                        self.bullet_group.remove(b)
                        enemyshotsound.play()

        if pygame.sprite.spritecollideany(self, enemy_group):
            print("PLAYER COLLIDE W/ENEMY")
            self.dead = True

    def update(self, enemy_group, keys_pressed):
        cur_time = pygame.time.get_ticks()

        #check for shoot
        if keys_pressed[pygame.K_z] and cur_time - self.last_shot > self.shot_cooldown:
            pewpewsound.play()
            self.bullet_group.add(Bullet(self.rect.centerx, self.rect.top))
            #self.bullet_group.add(Bullet(self.rect.centerx + 15, self.rect.top +10))
            #self.bullet_group.add(Bullet(self.rect.centerx - 15, self.rect.top +10))
            #self.bullet_group.add(Bullet(self.rect.centerx + 30, self.rect.top +15))
            #self.bullet_group.add(Bullet(self.rect.centerx - 30, self.rect.top +15))
            self.last_shot = cur_time
            print("shooting")

        speed = 5
        if keys_pressed[pygame.K_LSHIFT]:
            speed -= 2.5
        if keys_pressed[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= speed
            print("UP")
        if keys_pressed[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += speed
            print("DOWN")
        if keys_pressed[pygame.K_RIGHT] and self.rect.right < 500:
            self.rect.x += speed
            print("RIGHT")
        if keys_pressed[pygame.K_LEFT] and self.rect. left > 0:
            self.rect.x -= speed
            print("LEFT")

        self.check_collision(enemy_group)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Data/player_bullet1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.offscreen = False

    def update(self):
        self.rect.y -= 8 #speed of bullets movement
        if self.rect.y < -100:
            self.offscreen = True

class Cookie(pygame.sprite.Sprite):
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

class Donut(pygame.sprite.Sprite):
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
            self.rect.x = randint(-50, playspace.get_width())
            self.rect.y = -40

class Coffee(pygame.sprite.Sprite):
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
        if self.mode == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.t += 1/60
        if self.mode == 1:
            self.rect.y += randint(1, 3)#self.speed
            self.rect.x += randint(1, 2)#self.speed

        if self.mode == 2:
            self.rect.y += randint(1, 3)#self.speed
            self.rect.x -= randint(1, 2)#self.speed

        if self.rect.y >= 610 and self.mode == 1:
            self.rect.x = randint(-70,-50)
            self.rect.y = randint(-100, 100)

        if self.rect.y >= 610 and self.mode == 2:
            self.rect.x = randint(600, 620)
            self.rect.y = randint(-100, 100)
                
#VARIABLES AND INSTANCES FOR playing() START

#sounds and muse
pewpewsound = pygame.mixer.Sound("Data/mal_shoot2.wav")
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
player_group = pygame.sprite.GroupSingle()
player_group.add(player)

#ENEMY

enemy_group = pygame.sprite.Group()

#VARIABLES AND INSTANCES FOR playing() END!
#................................................
#VARIABLES AND INSTANCES FOR mainmenu() START
title_screen_and_bg = pygame.image.load("Data/MENU BG1.png") #these two are just images of 900 x 600 they are not 900x640, make the text and stars different layers later, and maybe a lil animation too (x_x)
alt_title_screen_and_bg = pygame.image.load("Data/MENU BG2.png")

START_BUTTON = Button("Data/buttonimage.png", (260, 377), "Start", pygame.font.Font("Data/l_10646.ttf", 35), (234, 146, 171), (175, 127, 194))#estimated pos
QUIT_BUTTON1 = Button("Data/buttonimage.png", (300, 450), "Quit", pygame.font.Font("Data/l_10646.ttf", 35), (234, 146, 171), (175, 127, 194))#estimated pos
 
RESTART_BUTTON = Button("Data/buttonimage.png", (450, 377), "Restart", pygame.font.Font("Data/l_10646.ttf", 35), (234, 146, 171), (175, 127, 194))#estimated pos
QUIT_BUTTON2 = Button("Data/buttonimage.png", (450, 477), "Quit", pygame.font.Font("Data/l_10646.ttf", 35), (234, 146, 171), (175, 127, 194))#estimated pos
        

#VARIABLES AND INSTANCES FOR mainmenu() END
#................................................
#VARIABLES AND INSTANCES FOR lost() START
ded = font("Data/l_10646.ttf", 50, "You lost", (255,255,255))
ded_bg = pygame.image.load("Data/youlost.png")
#VARIABLES AND INSTANCES FOR lost() END

def reset():
    player_group.sprite.reset()

    enemy_group.empty()
    for _ in range(32):
        enemy_group.add(Cookie("Data/cooki.png", randint(1, 5)))

    for _ in range(10):
        enemy_group.add(Coffee("Data/Coffee.png", 2, randint(600, 990), randint(-100, 100), 2))
        enemy_group.add(Coffee("Data/Coffee.png", 1, randint(-390,-50), randint(-100, 100) , 1))


def playing(mouse_pos, keys_pressed):
    if player.dead: 
        return lost

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

    #enemies
    enemy_group.update()
    enemy_group.draw(playspace)

    #player
    player_group.update(enemy_group, keys_pressed)
    player_group.draw(playspace)#surface

    player_group.sprite.bullet_group.update()
    player_group.sprite.bullet_group.draw(playspace)

    if keys_pressed[pygame.K_ESCAPE]:
        return mainmenu

    return playing

def mainmenu(mouse_pos, keys_pressed):
    screen.fill((0, 0, 36)) #colour of the background image backgrounds
    screen.blit(alt_title_screen_and_bg,(0,0))

    #insert BUTTONS here 
    for button in [START_BUTTON, QUIT_BUTTON1]:
        button.changeColor(mouse_pos)
        button.update(screen) 

    if keys_pressed[pygame.K_p]:
        reset()
        return playing

    if pygame.mouse.get_pressed(3)[0]:
        if START_BUTTON.checkForInput(mouse_pos):
            reset()
            return playing

        if QUIT_BUTTON1.checkForInput(mouse_pos):
            pygame.quit()
            sys.exit()

    return mainmenu

def lost(mouse_pos, keys_pressed): #currently behaves exactly like a PAUSE need to figure out how to reset playing() when this "function" is called
    screen.fill((0, 0, 36)) #colour of the background image backgrounds
    screen.blit(ded_bg, (0,10)) #<-- finish this
    ded.render_text(ded_bg, ded_bg.get_width()/2 - 100, 30)

    for button in [RESTART_BUTTON, QUIT_BUTTON2]:
        button.changeColor(mouse_pos)
        button.update(screen)
    
    if keys_pressed[pygame.K_p]:
        return playing

    if pygame.mouse.get_pressed(3)[0]:
        if RESTART_BUTTON.checkForInput(mouse_pos):
            reset()
            return playing

        if QUIT_BUTTON2.checkForInput(mouse_pos):
            pygame.quit()
            sys.exit()

    return lost


display = mainmenu
while True:
    mouse_pos = pygame.mouse.get_pos()
    keys_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    display = display(mouse_pos, keys_pressed)

    pygame.display.update()
    fpsclock.tick(60)

#TMR MAKE THE LOST RESET and also reset loc of enemies when shot could be used
#MAKE BULLET SLOW ENEMY
#FAST CLOCK = SCORE
#explosion sound lmms when she explode
