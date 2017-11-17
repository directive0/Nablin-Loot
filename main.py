#looter alpha 10
# C.Barrett - 2017

import pygame
from entities import *
from objects import *

pandora = True

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.display.init()
pygame.font.init()

# set the screen resolution, changed to facilitate the openpandora screen res
screenSize = (800, 480)

# I forget, probably colour depth?
modes = pygame.display.list_modes(16)

# instantiate a pygame display with the name "surface"
if pandora:
	surface = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
	pygame.mouse.set_visible(False)
else:
	surface = pygame.display.set_mode(screenSize)

vignette = pygame.image.load("assets/overlay.png")
sidebarsrc = pygame.image.load("assets/Sidebar.png")

status = "start"
gameover = False

def plantbushes(numbush,startx,starty,endy,variation,spritelist, bushlist):
    #determine spacing for trees
    distance = abs(starty-endy)
    
    jump = int(distance / numbush)
    
    for i in range(numbush):
        #plant a bush
        cursor = starty + (jump * i)
        
        planted = bush(startx, cursor)
        bushes.append(planted)
        spritelist.add(planted)
        #move the cursor down
    
    return bushes

def sortsprites(sprites):
    for i in sprites:
        target = i
        
        testx,testy = target.getpos()
        
        sprites.change_layer(i,testy)

# I'm playing with the idea of containing the world within its own class to keep things organized, but I think it'll just be unwieldy.
class world(object):
    def __init__(self):
        self.start()
    
    def start(self):
        
        self.clock = pygame.time.Clock()
        
        # The following objects are the Item Frame, the Hearts, score, and the stealth bar.
        self.items = itemFrame((4,4),surface)
        self.health = damage((140,4),surface)
        self.stealth = metertick(4,130)
        self.scoreobj = score()

        self.barbarian = BarbarianSprite()
        self.nablin = HeroSprite(224,64,self.barbarian,self.scoreobj,self.surface, self.items)
        self.harold = Bush(224,240)
        self.walter = Bush(550,240)
        self.roy = Bush(400,100)
        self.pyra = Fire(510, 350,nablin,barbarian)
        self.splashimg = Image()
        self.splashimg.update(splash,0,0)
        self.backimg = Image()
        self.backimg.update(background,80,0)
        self.all_sprites_list = pygame.sprite.LayeredUpdates()
        self.all_sprites_list.add(self.pyra,self.barbarian,self.nablin,self.harold,self.walter,self.roy)
        self.bushes = [self.harold,self.walter,self.roy]
        
        
        self.splashimg.draw(surface)
        self.titletext = Label()
        self.titletext.update("Press Space to Begin!",30,200,120,mainfont,white)
        self.titletext.draw(surface)
        self.overlay = Image()
        self.overlay.update(vignette,80,0)
        
        

        
        
        # The Following objects load and configure the music.
        pygame.mixer.music.load('assets/lvl1.mp3')
        pygame.mixer.music.set_volume(0.1)

        # We check for key presses 
        pygame.event.get()
        
        # we put the event list into an object we can pass to our next decision
        self.key = pygame.key.get_pressed()
    
        # if the player presses space the game begins. Otherwise stay put.
        if key[pygame.K_SPACE]:
            pygame.mixer.music.play(-1, 0.0)
            self.status = "game"
        else:
            pass
    
    

while(status != "quit"):

    # the following conditional sets up the scene.
    if status == "start":
        clock = pygame.time.Clock()
        
        # The following objects are the Item Frame, the Hearts, score, and the stealth bar.
        health = damage((140,4),surface)
        stealth = metertick(4,130)
        scoreobj = score(20,140,40)
        items = itemFrame((4,4),surface,scoreobj)

        barbarian = BarbarianSprite()
        nablin = HeroSprite(224,64,barbarian,scoreobj,surface, items)
        harold = Bush(224,240)
        walter = Bush(550,240)
        roy = Bush(400,100)
        pyra = Fire(510, 350,nablin,barbarian)
        splashimg = Image()
        splashimg.update(splash,0,0)
        backimg = Image()
        backimg.update(background,80,0)
        all_sprites_list = pygame.sprite.LayeredUpdates()
        all_sprites_list.add(pyra,barbarian,nablin,harold,walter,roy)
        bushes = [harold,walter,roy]
        
        
        splashimg.draw(surface)
        titletext = Label()
        titletext.update("Press Space to Begin!",30,200,120,mainfont,white)
        titletext.draw(surface)
        overlay = Image()
        overlay.update(vignette,80,0)
        
        # The Following objects load and configure the music.
        pygame.mixer.music.load('assets/lvl1.mp3')
        pygame.mixer.music.set_volume(0.1)

        # We check for key presses 
        pygame.event.get()
        
        # we put the event list into an object we can pass to our next decision
        key = pygame.key.get_pressed()
    
        # if the player presses space the game begins. Otherwise stay put.
        if key[pygame.K_SPACE]:
            pygame.mixer.music.play(-1, 0.0)
            status = "game"
        else:
            pass
    
    
    # the next conditional runs when the game is underway
    if status == "game":
            
        # call on the hero sprite to update.
        nablin.update()
        
        # call on the barbarian sprite to update
        barbarian.update(surface,nablin,stealth)
        
        
        # this object checks to see if the barbarian attacked the player and landed a hit.
        caught = barbarian.gotcha()
        
        # if a collisions was detected we tell the hero object so it can register a hit
        if caught:
            gameover = nablin.hit(1,barbarian)
            
            
            
            if gameover:
                status = "game over"
        
        # fill the screen to erase the previous frame
        surface.fill(black)
        
        # Draw the background
        
        backimg.draw(surface)
        # update the campfire
        pyra.update(surface)


        # I need to go through the list of all the sprites and order them based on their Y pos so that the lower the y pos the lower the layer, the higher the y pos the higher the layer.
        sortsprites(all_sprites_list)


        # Draw all sprites to screen
        all_sprites_list.draw(surface)
        
        # draw the vignette overlay
        overlay.draw(surface)
        
        
        # draw our UI elements.
        scoreobj.draw(surface)
        stealth.update(surface,bushes,nablin)
        health.draw(nablin)
        items.draw()

    if status == "game over":
        titletext.update("GAME OVER!",50,200+160,200,mainfont,white)
        titletext.draw(surface)
            # this next item checks to see if the q key was pressed
        key = pygame.key.get_pressed()
    
        if key[pygame.K_SPACE]:
            status = "start"


    pygame.event.get()

    # this next item checks to see if the q key was pressed
    key = pygame.key.get_pressed()

    if key[pygame.K_q]:
        pygame.mixer.music.stop()
        status = "quit"
    else:
        pass
        #status = "go!"
    pygame.display.flip()
    clock.tick(15)
