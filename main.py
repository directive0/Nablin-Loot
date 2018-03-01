# Nablin Loot v0.13
# C.Barrett - 2018

# Pygame controls the graphical elements of the scene
import pygame

#These classes control the entities in the scene (player, barbarian) and the objects (UI elements, variable classes)
from entities import *
from objects import *

# flag to control whether or not game is being played on an OpenPandora handheld
pandora = False

# Pygame configuration calls to activate the audio buss, the display and the font driver.
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
# need to add:
#   -Hourglass
#   -pseudo random events
#   - stealth is footfalls not a countdown timer
#   - items have effects and buffs

class world(object):
    def __init__(self, nobush = 3, difficulty = 0):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.display.init()
        pygame.font.init()
        
        # set the screen resolution, changed to facilitate the openpandora screen res
        screenSize = (800, 480)
        
        # I forget, probably colour depth?
        modes = pygame.display.list_modes(16)
        
        if pandora:
            self.surface = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
            pygame.mouse.set_visible(False)
        else:
            self.surface = pygame.display.set_mode(screenSize)
        self.start()
    
    # The following function loads our sprites, gets the audio ready and prepares the scene for creation.
    def start(self):
        
        self.clock = pygame.time.Clock()
        
        self.leveltime = leveltimer(self.surface)
        self.scoreobj = score(20,140,40)
        self.items = itemFrame((4,4),self.surface,self.scoreobj)
        
        self.shadows = []
        
        self.barbarian = BarbarianSprite(self.shadows)
        self.nablin = HeroSprite(100,64,self.barbarian,self.scoreobj,self.surface, self.items,self.shadows)
        self.harold = Bush(224,240,self.shadows)
        self.walter = Bush(550,240,self.shadows)
        self.roy = Bush(400,100,self.shadows)
        self.pyra = Fire(510, 350,self.nablin,self.barbarian)
        self.splashimg = Image()
        self.splashimg.update(splash,0,0)
        self.backimg = Image()
        self.backimg.update(background,0,0)
        self.all_sprites_list = pygame.sprite.LayeredUpdates()


        self.bushes = [self.harold,self.walter,self.roy]
        # The following objects are the Item Frame, the Hearts, score, and the stealth bar.
        # # The following objects are the Item Frame, the Hearts, score, and the stealth bar.
        self.health = damage((140,4),self.surface)
        self.stealth = stealthbox(4,130,self.surface,self.barbarian,self.bushes,self.nablin)



        self.all_sprites_list.add(self.pyra,self.barbarian,self.nablin,self.bushes)        
        
        self.splashimg.draw(surface)
        self.titletext = Label()
        self.titletext.update("Press Space to Begin!",30,200,120,mainfont,white)
        self.titletext.draw(surface)
        self.overlay = Image()
        self.overlay.update(vignette,0,0)
        
        #Determine a number of bushes this level will have
        
        
        #Determine the possibility of a wizard appearing
        
        
        # The Following objects load and configure the music.
        pygame.mixer.music.load('assets/lvl1.ogg')
        pygame.mixer.music.set_volume(0.1)

        # We check for key presses 
        pygame.event.get()
        
        # we put the event list into an object we can pass to our next decision
        self.key = pygame.key.get_pressed()
        
        pygame.display.flip()
        # if the player presses space the game begins. Otherwise stay put.
        if self.key[pygame.K_SPACE]:
            pygame.mixer.music.play(-1, 0.0)
            self.status = "game"
        else:
            pass
    
    # The following function draws a frame of the game itself.
    
    def game(self):
        
        self.status = "game"
        # fill the screen to erase the previous frame
        self.surface.fill(black)
        
        # Draw the background        
        self.backimg.draw(self.surface)
        
        print(self.shadows)
        for i in range(len(self.shadows)):
            self.shadows[i].draw(self.surface) 
        
        # update the campfire
        self.pyra.update(self.surface)

        # call on the hero sprite to update.
        self.nablin.update()
        
        # call on the barbarian sprite to update
        self.barbarian.update(self.surface,self.nablin,self.stealth)

        # I need to go through the list of all the sprites and order them based on their Y pos so that the lower the y pos the lower the layer, the higher the y pos the higher the layer.
        sortsprites(self.all_sprites_list)


        # Draw all sprites to screen
        self.all_sprites_list.draw(self.surface)
        
        # draw the vignette overlay
        self.overlay.draw(self.surface)
        
        
        # draw our UI elements.
        self.scoreobj.draw(self.surface)
        self.stealth.tick()
        self.health.draw(self.nablin)
        self.items.draw()
        
        # this object checks to see if the barbarian attacked the player and landed a hit.
        self.caught = self.barbarian.gotcha()
        
        if self.leveltime.draw():
            self.status = "game over"
        
        # if a collisions was detected we tell the hero object so it can register a hit
        if self.caught:
            self.gameover = self.nablin.hit(1,self.barbarian)
            
            
            
            if self.gameover:
                self.status = "game over"
            
        return self.status



# three nights, chance of wizard increases each night by 10.
# if barb awakes you have to try and escape. Failing is game over.
# at the end of each night your loot is appraised
# end of game is high score ranking

gameplay = world()
while(status != "quit"):
    #gameplay = world()
    # the following conditional sets up the scene.
    if status == "start":
        #gameplay = world()
        # we create a timer object to control the scene.
        clock = pygame.time.Clock()

        # # we put the event list into an object we can pass to our next decision
        key = pygame.key.get_pressed()
    
        # if the player presses space the game begins. Otherwise stay put.
        if key[pygame.K_SPACE]:
            pygame.mixer.music.play(-1, 0.0)
            status = "game"
        else:
            pass
    
    
    # the next conditional runs when the game is underway
    if status == "game":
        status = gameplay.game()
        # # this object checks to see if the barbarian attacked the player and landed a hit.
        # caught = barbarian.gotcha()

    # if at any point the status is changed to game over:
    if status == "game over":
        # put the "game over" label onscreen.
        titletext = Label()
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
