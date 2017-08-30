import pygame
from objects import *

class Fire(object):
    pass

#the following class is the main Hero. It responds to key presses, initiates an "attack" and can hide in bushes.
class HeroSprite(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        
        # Call the parent class (Sprite) constructor
        super(HeroSprite,self).__init__()


        # Load the image
        self.image = pygame.image.load("assets/nablin.png")

        self.speed =  10
        self.animtick = 0

        self.facing = "right"
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x 
        self.mask = pygame.mask.from_surface(self.image)
        
        
        
        #creates a shadow
        self.shadow = Image()
        self.shadowimg  = pygame.image.load('assets/nabshadow.png')

    def loot(self,nablin,barbarian):
        col = pygame.sprite.collide_mask(barbarian, nablin)
        print("looted!", col)
        return col
    
    def hit(self):
        pass
    
    def move(self,direction,surface):

        if direction == "up":
            self.rect.y -= self.speed
            self.animtick += 1
        elif direction == "down":
            self.rect.y += self.speed
            self.animtick += 1
        elif direction == "right":
            self.facing = "right"
            self.rect.x += self.speed
            self.animtick += 1
        elif direction == "left":
            self.facing = "left"
            self.rect.x -= self.speed
            self.animtick += 1
        elif direction == "upleft":
            self.facing = "left"
            self.rect.x -= self.speed
            self.rect.y -= self.speed
            self.animtick += 1
        elif direction == "downleft":
            self.facing = "left"
            self.rect.x -= self.speed
            self.rect.y += self.speed
            self.animtick += 1
        elif direction == "upright":
            self.facing = "right"
            self.rect.y -=self.speed
            self.rect.x += self.speed
            self.animtick += 1
        elif direction == "downright":
            self.facing = "right"
            self.rect.y += self.speed
            self.rect.x += self.speed   
            self.animtick += 1

        if direction == "loot":
            self.image = pygame.image.load("assets/loot.png")
            self.mask = pygame.mask.from_surface(self.image)
    
            if self.facing == "left":
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)


        if self.animtick == 2:
            self.image = pygame.image.load("assets/f1.png")
            self.mask = pygame.mask.from_surface(self.image)
    
            if self.facing == "left":
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)

        if self.animtick == 4:
            self.image = pygame.image.load("assets/f2.png")
            self.mask = pygame.mask.from_surface(self.image)

            if self.facing == "left":
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)

        if self.animtick == 6:
            self.image = pygame.image.load("assets/f3.png")
            self.mask = pygame.mask.from_surface(self.image)

            if self.facing == "left":
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)

        if self.animtick == 8:
            self.image = pygame.image.load("assets/f4.png")
            self.mask = pygame.mask.from_surface(self.image)

            if self.facing == "left":
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)

        if self.animtick >= 8:
            self.animtick = 0
            
        
        if self.facing == "left":
            self.shadow.update(self.shadowimg,self.rect.x+10,self.rect.y+ 45)
        else:
            self.shadow.update(self.shadowimg,self.rect.x+10,self.rect.y+ 45)
            
        self.shadow.draw(surface)


        
        if direction == "stationary":
            self.animtick = 0
            
            if self.facing == "right":
                self.image = pygame.image.load("assets/nablin.png")
                self.mask = pygame.mask.from_surface(self.image)

            
            if self.facing == "left":
                self.image = pygame.image.load("assets/nablin.png")
                self.image = pygame.transform.flip(self.image,True,False)
                self.mask = pygame.mask.from_surface(self.image)
    
    def getpos(self):
        return self.rect.x, self.rect.y
    
    def update(self,hero,target,score,surface):

        direction = getkeys()
        
        if direction == "loot":
            hit = self.loot(hero,target)
            print(hit)
            if hit:
                score.change("add",5)
        self.move(direction,surface)  

#the following class is the main barbarian. It should stay sleeping until the stealth meter runs out and then the barbarian wakes up and attacks.
class BarbarianSprite(pygame.sprite.Sprite):

    def __init__(self):
        
        # Call the parent class (Sprite) constructor
        super(BarbarianSprite,self).__init__()
        
        # Load the image
        self.image = pygame.image.load("assets/barbariansleeping.png")
        self.shadow = pygame.image.load("assets/barbshadow.png")
        # initializes the animation ticks
        self.animtick = 0
        
        # sets the characters facing direction
        self.facing = "right"
        
        self.speed = 2
        self.animspeed = .5
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.starty = 240
        self.startx = 320
        self.state = "asleep"
        self.position(220,240)
        #creates a shadow
        self.shadow = Image()
        self.shadowimg  = pygame.image.load('assets/barbshadow.png')
        self.sleepshadowimg  = pygame.image.load('assets/barbsleepshadow.png')

    def getstate(self):
        return self.status

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

    def update(self,surface,target,stealth):
        playerx,playery = target.getpos()
        
        if self.state == "woke":
            self.shadow.update(self.sleepshadowimg,self.rect.x,self.rect.y+ 25)
            self.shadow.draw(surface)
            
            self.image = pygame.image.load("assets/barbarianwake.png")
            self.animtick += 1
            print(self.animtick)
            if self.animtick >= 25:
                self.state = "aggro"
                self.image = pygame.image.load("assets/barbarianstep1.png")
                self.rect.y -= 80
                self.rect.x += 20
                self.animtick == 0

        if self.state == "aggro":

            
            if self.facing == "right":
                self.shadow.update(self.shadowimg,self.rect.x,self.rect.y+ 110)
            else:
                self.shadow.update(self.shadowimg,self.rect.x+25,self.rect.y+ 110)
                
            self.shadow.draw(surface)
            
            collision = pygame.sprite.collide_mask(target, self)
            
            if collision:
                self.state  = "swipe"
                self.animtick = 0

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


            if self.rect.y < playery-65:
                self.rect.y += self.speed

            if self.rect.y > playery-65:
                self.rect.y -= self.speed

            if self.rect.x < playerx:
                self.rect.x += self.speed
                self.facing = "right"
            if self.rect.x > playerx:
                self.facing = "left"
                self.rect.x -= self.speed

            self.animtick += self.animspeed

            if self.animtick > 4:
                self.animtick  = 0

        if self.state == "swipe":
            #self.shadow.update(self.shadowimg,self.rect.x,self.rect.y+ 100)
            #self.shadow.draw(surface)
            self.image = pygame.image.load("assets/barbattack.png")
            
            if self.facing == "right":
                self.image = pygame.transform.flip(self.image,True,False)
            
            self.animtick += 1
            
            if self.animtick >= 4:
                self.state = "aggro"
            
            collision = pygame.sprite.collide_mask(target, self)
            
            if collision:
                self.state = "gotcha"

        if self.state == "asleep":
            self.shadow.update(self.sleepshadowimg,self.rect.x,self.rect.y+ 25)
            self.shadow.draw(surface)
            
            if self.animtick == 0:
                self.image =  pygame.image.load("assets/barbariansleeping.png")
                
            elif self.animtick == 10:
                self.image =  pygame.image.load("assets/barbariansnore.png")

            self.animtick += .5
            
            if self.animtick > 20:
                self.animtick = 0
                
            if stealth.get() == 0:
                self.state = "woke"

    def gotcha(self):
        if self.state == "gotcha":
            return True
        else:
            return False
        
    def position(self,x,y):
            # Move sprite to specified coordinates
        self.rect.y = y
        self.rect.x = x

#the following class is the bush! It sits around and provides cover for that pesky Nablin to hide from his persuiers! What a cheeky little bush!
class Bush(pygame.sprite.Sprite):

    def __init__(self,x,y):

        # Call the parent class (Sprite) constructor
        super(Bush,self).__init__()
        
        # Load the image
        self.image = pygame.image.load("assets/bush.png")
        # Set our transparent color

        
        self.mask = pygame.mask.from_surface(self.image)
        
        self.animtick = 0

        self.animating = False
        
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        
        self.starty = y   
        self.startx = x
        
        self.rect.y = y
        self.rect.x = x
        
    def getpos(self):
        #return current location
        return self.rect.x, self.rect.y

    def update(self):
        #be a bush for a while
        pass
