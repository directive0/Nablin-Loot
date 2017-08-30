import pygame
from entities import *

# the following are my color standards
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)
air = (255,0,255)

mainfont = "assets/boot.ttf"
background = pygame.image.load('assets/background.bmp')
splash = pygame.image.load('assets/splash.bmp')
 
# the following class is used to display images
class Image(object):
    def __init__(self):
        self.x = 258
        self.y = 66
        self.Img = pygame.image.load('assets/background.bmp')
    
    def update(self, image, nx, ny):
        self.x = nx
        self.y = ny
        self.Img = image
        
    
    def draw(self, surface):
        surface.blit(self.Img, (self.x,self.y))

class Box(object):
    def __init__(self):
        self.x=0
        self.y=0
        self.vx=1
        self.vy=1
        self.size=(50,50)
        self.color=(0,0,255)
        
    def update(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
    
    def draw(self, surface):
        rect = pygame.Rect((self.x,self.y), self.size)
        pygame.draw.rect(surface, self.color, rect)

#the following class is for text
class Label(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = white
        self.fontSize = 33
        self.myfont = pygame.font.Font(mainfont, self.fontSize)
    
    def update(self, content, fontSize, nx, ny, fontType, color):
        self.x = nx
        self.y = ny
        self.content = content
        self.fontSize = fontSize
        self.myfont = pygame.font.Font(fontType, self.fontSize)
        self.color = color
    
    def draw(self, surface):
        label = self.myfont.render(self.content, 1, self.color)
        surface.blit(label, (self.x, self.y))

def getkeys():
    
    key = pygame.key.get_pressed()
    
    direction = "stationary"
    
    if key[pygame.K_SPACE]:
        direction = "loot"

    if key[pygame.K_LEFT]:
        direction = "left"
    if key[pygame.K_RIGHT]:
        direction = "right"
    if key[pygame.K_UP]:
        direction = "up"
    if key[pygame.K_DOWN]:
        direction ="down"
    
    if key[pygame.K_LEFT]:
        if key[pygame.K_UP]:
            direction = "upleft"
    
    if key[pygame.K_LEFT]:
        if key[pygame.K_DOWN]:
            direction = "downleft"

    if key[pygame.K_RIGHT]:
        if key[pygame.K_UP]:
            direction = "upright"

    if key[pygame.K_RIGHT]:
        if key[pygame.K_DOWN]:
            direction = "downright"

    return direction

class metertick(object):
    def __init__(self):
        self.meter = Box()
        self.metervalue = 200
    
    def get(self):
        return self.metervalue

    def tick(self, surface):
        self.metervalue -= 1
        if self.metervalue < 0:
            self.metervalue = 0
        self.meter.update(400, 15, (self.metervalue,10), white)
        self.meter.draw(surface)
        
        return self.metervalue 
        
    def draw(self,surface):
        self.metervalue += .5
        if self.metervalue  > 200:
            self.metervalue = 200
        self.meter.update(400, 15, (self.metervalue,10), white)
        self.meter.draw(surface)
        return self.metervalue
        
    def update(self, surface, bush, hero):
        collision = pygame.sprite.collide_mask(bush, hero)
        
        if collision:
            stealthnum = self.draw(surface)
        else:
            stealthnum = self.tick(surface)
        
        
class score(object):
    def __init__(self):
        self.scoreval = 0
        
    def get(self):
        self.scorefortext = int(self.scoreval)
        return self.scorefortext 
    
    def change(self,incdec,value):
        if incdec == "add":
            self.scoreval += value
        elif incdec == "sub":
            self.scoreval -= value
        else:
            pass
    
    def draw(self,surface):
        scorevalue = str(self.get())
        scoretext = Label()
        scoretext.update("Score: " + scorevalue,15,5,5,mainfont,white)
        scoretext.draw(surface)

class damage(object):
    def __init__(self):
        self.damageval = 0
    
