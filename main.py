#looter alpha 6
# C.Barrett - 2017

import pygame
from entities import *
from objects import *


pygame.init()
pygame.font.init()

# the following are my color standards

# set the screen resolution
screenSize = (640, 480)

# I forget, probably colour depth?
modes = pygame.display.list_modes(16)

# instantiate a pygame display with the name "surface"
surface = pygame.display.set_mode(screenSize)
vignette = pygame.image.load("assets/overlay.png")

status = "start"



while(status != "quit"):
    
    if status == "start":
        clock = pygame.time.Clock()

        scoreobj = score()
        
        barbarian = BarbarianSprite()
        nablin = HeroSprite(64,64)
        harold = Bush(64,240)
        splashimg = Image()
        splashimg.update(splash,0,0)
        backimg = Image()
        backimg.update(background,0,0)
        all_sprites_list = pygame.sprite.OrderedUpdates()
        all_sprites_list.add(barbarian)
        all_sprites_list.add(nablin)
        all_sprites_list.add(harold)
        stealth = metertick()
        splashimg.draw(surface)
        titletext = Label()
        titletext.update("Press Space to Begin!",30,200,120,mainfont,white)
        titletext.draw(surface)
        overlay = Image()
        overlay.update(vignette,0,0)

        pygame.event.get()
        key = pygame.key.get_pressed()
        
        if key[pygame.K_SPACE]:
            
            status = "game"
        else:
            pass

    if status == "game":
        
        surface.fill(black)
        
        backimg.draw(surface)
        
        nablin.update(nablin,barbarian,scoreobj,surface)
        barbarian.update(surface,nablin,stealth)
        overlay.draw(surface)
        stealth.update(surface,harold,nablin)
        
        scoreobj.draw(surface)


        
        caught = barbarian.gotcha()
        
        if caught:
            status = "game over"
            
        
        all_sprites_list.draw(surface)

    if status == "game over":
        titletext.update("GAME OVER!",50,200,200,mainfont,white)
        titletext.draw(surface)
            # this next item checks to see if the q key was pressed
        key = pygame.key.get_pressed()
    
        if key[pygame.K_SPACE]:
            status = "start"


    pygame.event.get()

    # this next item checks to see if the q key was pressed
    key = pygame.key.get_pressed()

    if key[pygame.K_q]:
        status = "quit"
    else:
        pass
        #status = "go!"
    pygame.display.flip()
    clock.tick(20)
