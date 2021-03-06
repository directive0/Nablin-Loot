import pygame
import random
from objects import *
from math import sin, cos, pi, atan2


# In the interest of efficiency I am loading all my images at the beginning.
pip = pygame.image.load('assets/pip.png')
flask = pygame.image.load('assets/flask.png')
pip = pygame.image.load('assets/pip.png')
fire1 = pygame.image.load("assets/CampfireFire.png")
fire2 = pygame.image.load("assets/CampfireFire2.png")
nabloot0 = pygame.image.load("assets/loot.png")
nablin0 = pygame.image.load("assets/nablin.png")
nablin1 = pygame.image.load("assets/f1.png")
nablin2 = pygame.image.load("assets/f2.png")
nablinhit = pygame.image.load("assets/nablinhit.png")
nablindeath = pygame.image.load("assets/nablindeath.png")
z0 = pygame.image.load("assets/z1.png")
z1 = pygame.image.load("assets/z2.png")
z2 = pygame.image.load("assets/z3.png")


pygame.display.set_icon(nablin2)

# the following images are for the barbarian
barbattack = pygame.image.load("assets/barbattack.png")
barbsleep = pygame.image.load("assets/barbariansleeping.png")
barbsnore = pygame.image.load("assets/barbariansnore.png")

z0 = pygame.image.load("assets/z0.png")
z1 = pygame.image.load("assets/z1.png")
z2 = pygame.image.load("assets/z2.png")
z3 = pygame.image.load("assets/z3.png")


barbsleepshadow = pygame.image.load("assets/barbsleepshadow.png")
barbshadow = pygame.image.load('assets/barbshadow.png')

#the following images are for shadows
nabshadow = pygame.image.load('assets/nabshadow.png')

# campfire images
logsimg = pygame.image.load('assets/CampfireLogs.png')
auraimg = pygame.image.load('assets/CampfireLight.png')


# the following function returns the angle to a desired destination when given an origin.
def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)

# the following returns a coordinate of a desired point at a certain angle and distance with reference to an origin
def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (cos(angle) * distance),
            pos[1] - (sin(angle) * distance))

# This class creates small pixelated embers that rise up from the fire in random directions.
class ember(object):
    def __init__(self,position):
        self.x, self.y = position
        self.starty = self.y 
        self.y = self.y - 20
        self.startx = self.x

        self.size=(2,2)
        
        self.replace()
        self.rect = pygame.Rect((self.x,self.y), self.size)
        
    
    def longevity(self):
        adjust = self.decide(-10,0)
        longval = 20 + adjust
        
        return longval
        
    def replace(self): 
        self.distance = 0
        self.position = self.decide(-20,20)
        self.r = 255
        self.g = 255
        self.x = self.startx + self.position
        self.y = self.starty - 20
        self.speed = 1 + self.decide(1,4)
        self.kill = self.longevity()
        
        
    def decide(self,a,b):
        decision = random.randint(a,b)
        return decision
        
        
    def update(self):
        if self.distance < self.kill:
            
            if self.distance > 10:
                self.r -= 5
                self.g -= 5
            self.color = self.r,self.g,0
            self.y -= self.speed

            if self.decide(0,1) == 0:
                self.x -= 1
            else:
                self.x += 1
            
            self.color = (self.r,self.g,0)
            self.distance += 1
        else:
            self.replace()
        
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self,surface):
        self.update()
        
        pygame.draw.rect(surface, self.color, self.rect)  

# This class handles the location, animation and collisions for the fire.    
class Fire(pygame.sprite.Sprite):

    def __init__(self,x,y,hero,barbarian):

        # Call the parent class (Sprite) constructor
        super(Fire,self).__init__()
        
        # Load the image
        self.image = fire1
    
        # the following is a timer interval used to direct the speed of animation
        self.timer = pygame.time.Clock()
        
        # the followin creates a mask from the supplied image (for collisions)
        self.mask = pygame.mask.from_surface(self.image)

        # we make the hero and enemy object accessible in the class so we can find their position when we need to.
        self.nablin = hero
        self.barbarian = barbarian
        
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        
        # we set the coordinates for the fire, as given to us when the class was instantiated.
        self.starty = y   
        self.startx = x
        
        self.rect.y = y
        self.rect.x = x
        self.speed = 1
        self.animtick = 0
        self.logs = Image()
        self.logsimg = logsimg
        self.logs.update(self.logsimg,self.startx,self.starty+20,)
        self.aura = Image()
        self.auraimg = auraimg
        self.aura.update(self.auraimg,self.startx-8,self.starty+20,)
        self.ember1 = ember(self.rect.midbottom)
        self.ember2 = ember(self.rect.midbottom)
        self.ember3 = ember(self.rect.midbottom)
        self.ember4 = ember(self.rect.midbottom)
        self.ember5 = ember(self.rect.midbottom)
        
    def getpos(self):
        #return current location
        return self.rect.midbottom
        
    def collide(self):
        
        rectollide = pygame.sprite.collide_rect(self.nablin,self)
        
        if rectollide:
            collision = pygame.sprite.collide_mask(self.nablin,self)
            if collision:
                self.nablin.hit(1,self)

    def update(self,surface):
        #be fire!
        randox = random.randint(-1,1)
        randoy = random.randint(-1,1)
        self.aura.update(self.auraimg,(self.startx-9)+randox,(self.starty+18)+randoy,)
        self.aura.draw(surface)
        self.logs.draw(surface)
        self.collide()
        
        self.animtick = random.randint(0,1)
        
        if self.animtick > 1:
            self.animtick = 0
        
        if self.animtick == 0:
            self.image = fire1
            
        if self.animtick == 1:
            self.image = fire2
            
        self.ember1.draw(surface)
        self.ember2.draw(surface)
        self.ember3.draw(surface)
        self.ember4.draw(surface)
        self.ember5.draw(surface)

class effect(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        
        # Call the parent class (Sprite) constructor
        super(effects,self).__init__()
        self.image = image
        self.x = x
        self.y = y
            
    def update(self,x,y):
        pass
        

#the following class is the main Hero. It responds to key presses, initiates an "attack" and can hide in bushes.
class HeroSprite(pygame.sprite.Sprite):
    
    def __init__(self, x, y, target, score, surface, lootlist,shadows):
        
        # Call the parent class (Sprite) constructor
        super(HeroSprite,self).__init__()
        
        self.surface = surface
        self.target = target
        self.score = score

        # Load the image
        self.image = nablin0

        self.speed =  10
        self.speedrun = 10
        self.speedwalk = 4
        self.animtick = 0
        
        # variables to control knockback events
        self.knock = False
        self.knocktick = 0
        self.knockdir = 0
        self.knockjump = 30
    
    
        #the following variables hold the player status
        self.facing = "right"
        self.moving = False
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x 
        self.mask = pygame.mask.from_surface(self.image)
        self.foot1 = pygame.mixer.Sound("assets/foot1.wav")
        self.foot2 = pygame.mixer.Sound("assets/foot2.wav")
        self.foot3 = pygame.mixer.Sound("assets/foot3.wav")
        self.foot4 = pygame.mixer.Sound("assets/foot4.wav")
        self.footy = 0
        
        
        #creates a shadow
        self.shadows = shadows
        self.shadow = Image()
        self.shadowimg  = nabshadow
        self.shadows.append(self.shadow)
        #stores player health
        self.health = 6
        
        #stores player inventory
        self.worldloot = lootlist
        
        #stores location of last looting (so as to stop duplicates)
        self.lastloot = (0,0)
        
        #amount of noise made
        self.noise = 0

    # this function governs looting, it is a work in progress
    def loot(self):
        col = pygame.sprite.collide_mask(self.target, self)

        self.thisloot = self.getpos()
        #check for collision with barbarian
        if self.thisloot != self.lastloot:
            self.lastloot = self.thisloot
            tryloot = col
        
        #print(tryloot)
        
        #if collisions detected
            if tryloot:
                self.worldloot.new(self.getpos())
                #make a new loot object    
    
    def use(self):
        pass
    
    # this function controls hit points. It is simply a decremental counter right now.
    def hit(self, amount,attacker):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self.knocktick = 2
        self.knock = True
        eposx,eposy = attacker.getpos()
        pposx,pposy = self.getpos()
        if eposx > pposx:
            self.knockdir = 0
        else:
            self.knockdir = 1
            
        if self.health == 0:
            return True
        else:
            return False
            
    # this function will allow the player to receive a knockback when hit by the enemy. It will recieve the direction it was hit from and the power of the knockback.
    def knockback(self):
        
        self.image = nablinhit
        if self.facing == "left":
            self.image = pygame.transform.flip(self.image,True,False)
        
        if self.knocktick >= 0:
            if self.knockdir == 0:
                self.rect.x -= self.knockjump
            if self.knockdir == 1:
                self.rect.x += self.knockjump
        else:
            self.knock = False
        
        self.checklimits()
        self.knocktick -= 1
        
    # This function returns the current health of the player to any object requesting it.
    def status(self):
        return self.health
    
    # this function stops the player from leaving the boundary of the screen
    def checklimits(self):
        currentx, currenty = self.rect.midbottom
        if currenty >= 480:
            self.rect.midbottom = currentx, 480
        elif currenty <= 110:
            self.rect.midbottom = currentx, 110
            
        if currentx >= 800:
            self.rect.midbottom = 800, currenty
        elif currentx <= 0:
            self.rect.midbottom = 0, currenty
     
    #this function draws the shadow to screen       
    def shadowdraw(self):
        if self.facing == "left":
            self.shadow.update(self.shadowimg,self.rect.x+10,self.rect.y+ 45)
        else:
            self.shadow.update(self.shadowimg,self.rect.x+10,self.rect.y+ 45)
            
        #self.shadow.draw(self.surface)
            
    # this object controls player footfall sounds.
    def footfall(self):
        
        if self.footy == 0:
            self.foot1.play()
        elif self.footy == 1:
            self.foot2.play()
        elif self.footy == 2:
            self.foot3.play()
        elif self.footy == 3:
            self.foot4.play()    
        
        self.footy += 1
    
        if self.footy >= 4:
            self.footy = 0
    
    # this function is called by the stealth meter and returns the current status of the player
    def walking(self):
        return self.moving
    
    def noise(self):
        return self.noise
                
    # this function governs movement. It receives a command from the main loop and interprets it as movement.     
    def move(self,direction,surface):
    
    #we need to add a function that detects between walking and sprinting. sprinting should cost more stealth
        self.moving = False
        if "run" in direction:
            self.speed = self.speedwalk
            self.noise = 1
        else:
            self.noise = 2
            self.speed = self.speedrun
            

        if "up" in direction:
            self.footfall()
            self.rect.y -= self.speed
            self.animtick += 1
            self.moving = True
            
        if "down" in direction:
            self.footfall()
            self.rect.y += self.speed
            self.animtick += 1
            self.moving = True
        
        if "right" in direction:
            self.footfall()
            self.facing = "right"
            self.rect.x += self.speed
            self.animtick += 1
            self.moving = True
        
        if "left" in direction:
            self.footfall()
            self.facing = "left"
            self.rect.x -= self.speed
            self.animtick += 1
            self.moving = True
        
        # if there is no movement (no messages in the movement list) set the status of the object to reflect that
        if len(direction) == 0:
            self.moving = False
            
        if "loot" in direction:
            self.image = nabloot0
            self.mask = pygame.mask.from_surface(self.image)
            self.moving = True
            self.noise = 3
            if self.facing == "left":
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)


        if self.animtick == 2:
            self.image = nablin1
            self.mask = pygame.mask.from_surface(self.image)
    
            if self.facing == "left":
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)

        if self.animtick == 4:
            self.image = nablin0
            self.mask = pygame.mask.from_surface(self.image)

            if self.facing == "left":
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)

        if self.animtick == 6:
            self.image = nablin2
            self.mask = pygame.mask.from_surface(self.image)

            if self.facing == "left":
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)

        if self.animtick == 8:
            self.image = nablin0
            self.mask = pygame.mask.from_surface(self.image)

            if self.facing == "left":
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)
        
        if self.animtick > 8:
            self.animtick = 0

        if not direction:
            self.animtick = 0
            
            if self.facing == "right":
                self.image = nablin0
                self.mask = pygame.mask.from_surface(self.image)

            if self.facing == "left":
                self.image = nablin0
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)
        else:
            pass

        
    # this function returns the players location with reference to the BOTTOM MIDDLE of the mask bounding box 
    def getrect(self):
        return self.rect,self.facing
    
    def getpos(self):

        return self.rect.midbottom
    
    def update(self):
        
        
        #the conditional checks to see if the player is being knocked back.
        if self.knock == True:
            self.shadowdraw()
            self.knockback()
            self.shadowdraw()
        else:
            direction = getkeys()
        
            #if the player has hit space
            if "use" in direction:
                self.worldloot.use(self)
            
            if "loot" in direction:
                
                self.loot()    
            self.shadowdraw()
            self.move(direction,self.surface)  
            self.shadowdraw()
        self.checklimits()
        
        

#the following class is the main barbarian. It should stay sleeping until the stealth meter runs out and then the barbarian wakes up and attacks.
class BarbarianSprite(pygame.sprite.Sprite):

    def __init__(self,world):
        self.world = world
        self.shadows = self.world.shadows
        # Call the parent class (Sprite) constructor
        super(BarbarianSprite,self).__init__()
        
        # Load the image
        self.image = barbsleep
        self.shadow = barbsleepshadow
        # initializes the animation ticks
        self.animtick = 0
        self.snoretick = 0
        
        # sets the characters facing direction
        self.facing = "right"
        
        self.speed = 4
        self.animspeed = .5
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.refresh()
        
        self.starty = 250
        self.startx = 320
        self.state = "asleep"
        self.position(220+160,250)
        #creates a shadow
        self.shadow = Image()
        self.shadowimg  = barbshadow
        self.sleepshadowimg  = barbsleepshadow
        self.shadows.append(self.shadow)
        
        self.snores = Image()
        self.world.effects.append(self.snores)
        self.snore()
        
        
    def getstate(self):
        return self.status  
    
    def getpos(self):
        if self.state == "asleep":
            #return current location
        
            retx,rety = self.rect.midbottom
        
            rety -= 35
        
            return retx,rety
        else:
            retx,rety = self.rect.midbottom
        
            rety -= 20
        
            return retx,rety
        
    def firego(self):
        if self.rect.y < self.starty:
            self.rect.y += 2

        if self.rect.y > self.starty:
            self.rect.y -= 2

        if self.rect.x < self.startx:
            self.rect.x += 2
        if self.rect.x > self.startx:
            self.rect.x -= 2

        if self.rect.x == self.startx & self.rect.y == self.starty:
            return True
        else:
            return False
 
    def walkingshadow(self):
        if self.facing == "right":
            self.shadow.update(self.shadowimg,self.rect.x,self.rect.y+ 110)
        else:
            self.shadow.update(self.shadowimg,self.rect.x+25,self.rect.y+ 110)
 
    #the following class updates the location of the shadow object
    def sleepshadow(self):
        
        self.shadow.update(self.sleepshadowimg,self.rect.x,self.rect.y + 25)
        #self.shadow.update(self.sleepshadowimg,self.rect.centerx,self.rect.centery)
        
        self.shadow.draw(self.surface)
 
    #the following class handles the actions of the barb when they are awoken.
    def woke(self):
        
        #remove the snoring effect from the list of world effects
        
        try:
            self.world.effects.remove(self.snores)
        except:
            pass
        
        #update the shadow for sleeping    
        self.sleepshadow()
        
        self.image = pygame.image.load("assets/barbarianwake.png")
        self.refresh()
        self.animtick += 1

        if self.animtick >= 25:
            self.state = "aggro"
            self.image = pygame.image.load("assets/barbarianstep1.png")
            self.rect.y -= 80
            self.rect.x += 20
            self.animtick == 0
    
    def aggro(self):
        
        # the next decision checks for collisions between the enemy and the player. If one is detected we enter the aggro state.
        collision = pygame.sprite.collide_mask(self.target, self)
        
        if collision:
            self.state  = "swipe"
            self.animtick = 0

        
        self.walkingshadow()
            
        #self.shadow.draw(self.surface)
        


        if self.animtick == 0:
            self.image = pygame.image.load("assets/barbarianstep1.png")
            
            if self.facing == "right":
                self.image = pygame.transform.flip(self.image,True,False)

        if self.animtick == 2:
            self.image = pygame.image.load("assets/barbarianstand.png")
            
            if self.facing == "right":
                self.image = pygame.transform.flip(self.image,True,False)

        if self.animtick == 3:
            self.image = pygame.image.load("assets/barbarianstep2.png")
            
            if self.facing == "right":
                self.image = pygame.transform.flip(self.image,True,False)

        if self.animtick == 4:
            self.image = pygame.image.load("assets/barbarianstand.png")
            
            if self.facing == "right":
                self.image = pygame.transform.flip(self.image,True,False)
        
        #self.refresh()

        # the following items check the angle and distance to the target and each anim-tick moves the barbarian in that direction.

        self.pos = self.rect.midbottom
        self.x, self.y = self.pos
        self.target_pos = self.playerx,self.playery
        self.angle = get_angle(self.pos, self.target_pos)
        self.pos = project(self.pos, self.angle, self.speed)
        self.rect.midbottom = self.pos
        
        if self.x < self.playerx:
            self.facing = "right"
        if self.x > self.playerx:
            self.facing = "left"
        
        #print(self.stealth.get())
        
        
        if self.stealth.get() <= .1:
         
            dist = getdist(self.target,self)
            
            if dist > 100:
                self.animtick = 0
                self.state = "dozing"
                

        self.animtick += self.animspeed

        if self.animtick > 4:
            self.animtick  = 0
            
    def swipe(self):
        #self.shadow.update(self.shadowimg,self.rect.x,self.rect.y+ 100)
        #self.shadow.draw(surface)
        self.image = barbattack
        
        if self.facing == "right":
            self.image = pygame.transform.flip(self.image,True,False)
        
        self.animtick += 1
        
        if self.animtick >= 4:
            self.state = "aggro"
        
        collision = pygame.sprite.collide_mask(self.target, self)
        
        if collision:
            self.state = "gotcha"
    
    def snore(self):
        
        snorex = self.rect.x + 30
        snorey = self.rect.y - 40
        
        if self.snoretick == 0:
            self.snores.update(z0,snorex,snorey)
        if self.snoretick == 1:
            self.snores.update(z1,snorex,snorey)
        if self.snoretick == 2:
            self.snores.update(z2,snorex,snorey)
        if self.snoretick == 3:
            self.snores.update(z3,snorex,snorey)
        
        self.snoretick += 1
        
        if self.snoretick > 3:
            self.snoretick = 0
        
    def doze(self):
        
        self.image = pygame.image.load("assets/barbarianstand.png")
        self.refresh
        
        if self.facing == "right":
            self.image = pygame.transform.flip(self.image,True,False)
        
        if self.animtick >= 0 and self.animtick <= 10:
            self.facing = "right"

        if self.animtick >= 11 and self.animtick <= 19:
            self.facing = "left"

        if self.animtick >= 20 and self.animtick <= 29:
            self.facing = "right"

        if self.animtick > 30:
            self.state = "asleep"
            
        self.animtick += 1
    
    def refresh(self):
        try:
            print(self.rect)

            oldx,oldy = self.rect.x,self.rect.y
        except:
            pass
            
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        try:
            self.rect.x,self.rect.y=oldx,oldy
        except:
            pass    
        print("and then")
        print(self.rect)    
    def asleep(self):
        
        if self.animtick == 0:
            self.image =  barbsleep
            
        elif self.animtick == 10:
            self.image =  barbsnore
            self.snore()
            
        self.refresh()
        
        self.animtick += .5
        
        if self.animtick > 20:
            self.animtick = 0
            
        if self.stealth.get() == 1:
            self.state = "woke"
        
        self.sleepshadow()

                
    def update(self,surface,target,stealth):
        self.surface = surface
        self.target = target
        self.stealth = stealth
        
        self.playerx,self.playery = target.getpos()
        
        if self.state == "woke":
            self.woke()

        if self.state == "aggro":
            self.aggro()

        if self.state == "swipe":
            self.swipe()

        if self.state == "asleep":
            self.asleep()
    
        if self.state == "dozing":
            self.doze()
            
    def gotcha(self):
        if self.state == "gotcha":
            self.state = "aggro"
            return True
        else:
            return False
        
    def position(self,x,y):
            # Move sprite to specified coordinates
        self.rect.y = y
        self.rect.x = x

#the following class is the bush! It sits around and provides cover for that pesky Nablin to hide from his persuers! What a cheeky little bush!
class Bush(pygame.sprite.Sprite):

    def __init__(self,x,y,shadows):

        self.shadows = shadows
        self.shadow = Image()

        # Call the parent class (Sprite) constructor
        super(Bush,self).__init__()
        
        # Load the image
        self.image = pygame.image.load("assets/bush.png")
        # Set our transparent color

        # sets the collision mask for the object using the transparency layer of the PNG
        self.mask = pygame.mask.from_surface(self.image)
        
        self.animtick = 0

        self.animating = False
        
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.centerx and rect.centery
        self.rect = self.image.get_rect()
        
        self.rect.centery = y
        self.rect.centerx = x
        
        shady = self.rect.centery 
        shadx = self.rect.centerx
        
        #print(shadx,shady)
        #print(self.rect.centerx,self.rect.centery)
        
        self.shadow.update(nabshadow,shadx,shady, center = True)
        self.shadows.append(self.shadow)
        
    def getpos(self):
        #return current location
        
        retx,rety = self.rect.midbottom
        
        rety -= 4
        
        return retx,rety
        
    def update(self):
        pass
        #be a bush for a while
        #self.shadow.draw()


        
