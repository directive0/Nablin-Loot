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
heart = pygame.image.load('assets/heart.png')
halfheart = pygame.image.load('assets/halfheart.png')
itemframe = pygame.image.load('assets/itemframe.png')
itembubble = pygame.image.load('assets/bubble.png')

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

# the following class displays simple rectangles.
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

# the following function reports the current state of the keyboard event list. 
# If a player pressed a key it ends up in the event list which the program will need in order to respond.
# it returns a simple string indicating what state the keys are at.
# I have made it so key combos are returned for the up/left and down/right style inputs
def getkeys():
    
    key = pygame.key.get_pressed()
    
    direction = "stationary"
    
    if key[pygame.K_SPACE]:
        direction = "loot"

    if key[pygame.K_LSHIFT]:
        direction = "use"


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

# this class is the stealth meter. 
# Draw increases the bar, update decreases.
class metertick(object):
    def __init__(self,x,y):
        self.meter = Box()
        self.metervalue = 122
        self.metermax = 122
        self.x = x
        self.y = y
    
    def get(self):
        return self.metervalue

    def tick(self, surface):
        self.metervalue -= 1
        if self.metervalue < 0:
            self.metervalue = 0
        self.meter.update(self.x,self.y, (self.metervalue,10), white)
        self.meter.draw(surface)
        
        return self.metervalue 
        
    def draw(self,surface):
        self.metervalue += .5
        if self.metervalue  > self.metermax:
            self.metervalue = self.metermax
        self.meter.update(self.x, self.y, (self.metervalue,10), white)
        self.meter.draw(surface)
        return self.metervalue
        
    def update(self, surface, bush, hero):
        
        collidersum = 0
        
        for i in range(len(bush)):
            rectollide = pygame.sprite.collide_rect(bush[i],hero)
            collision = pygame.sprite.collide_mask(bush[i], hero)
            
            if rectollide:
                if collision:
                    collidersum +=1
            
        if collidersum > 0:
            stealthnum = self.draw(surface)
        else:
            stealthnum = self.tick(surface)
        
#This class handles the score integer and displays it as a text object
class score(object):
    def __init__(self,size,x,y):
        self.scoreval = 0
        self.x = x
        self.y = y
        self.size = size
        
    def get(self):
        self.scorefortext = int(self.scoreval)
        return self.scorefortext 
        
    def add(self,value):
        self.scoreval += value
    
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
        scoretext.update("Score: " + scorevalue,self.size,self.x,self.y,mainfont,white)
        scoretext.draw(surface)

# this class will handle damage. It is passed the hero object and then draws the hearts to screen where requested.
class damage(object):
    def __init__(self, location, surface):
        self.surface = surface
        self.damageval = 0
        self.heartimage = heart
        self.halfheartimage = halfheart
        self.value = 6
        self.jump = 30
        self.location = location
    
    # this next function is passed values from the main draw function
    # and places a heart of the appropriate kind at the appropriate location.
    # This allows me to easily repeat the task so I can reduce steps
    
    def placeheart(self,location,jumpscaler,full):
        x,y = location
        x = x + (self.jump * jumpscaler)
        
        if full:
            hearttype = self.heartimage
        else:
            hearttype = self.halfheartimage
        
        self.surface.blit(hearttype, (x,y))
    
    # the following function draws the hearts to screen. It takes the value from the player object and some coordinates for where to draw
    def draw(self, player):

        # get the health of the player
        self.value = player.status()

        
        # divide the health value (0-6) by two to give us the number of hearts.
        
        fullhearts = float(self.value) / float(2)

        # a full heart is worth 2 it points, so we divide the current health value by 2 to see how many full hearts we have
        
        # loop to draw 3 possible hearts.
        for i in range(3):
            # checks the hearts value is greater than 1 each time through the loop. If it is isn't it will draw a half heart. If the number is zero no heart is drawn.
            if fullhearts >= 1:
                self.placeheart(self.location,i,True)
            if fullhearts == .5:
                self.placeheart(self.location,i,False)
            
            # decrement the hearts variable so each time through the loop a heart is drawn representing the remaining value.
            fullhearts -= 1
            
# the following class handles the location of items.
class itemFrame(object):
    def __init__(self, location, surface, score):
        self.surface = surface
        self.location = location
        self.frame = itemframe
        self.items = []
        self.decided = False
        self.rolling = False
        self.interval = 160
        self.lasttime = 0
        self.timer = 0
        self.holdloot = []
        self.score = score
        
    def use(self):
        if len(self.holdloot) > 0:
            toploot = self.holdloot[-1]
            
            
        
    def roll(self):
        self.timenow = pygame.time.get_ticks()
        elapsed = self.timenow - self.lasttime
        print(elapsed)
        if elapsed < self.interval:
            
            print("Drawing bubble")
            self.surface.blit(itembubble, (self.lootx+10,self.looty-142))
        
            self.surface.blit(self.lootimage, (self.lootx+10,self.looty-142))
            print(self.lootx,self.looty)
        else:
            self.rolling = False
            self.holdloot.append(self.newloot)
        
        
    def new(self,location):
        self.lasttime = pygame.time.get_ticks()
        self.rolling = True
        self.lootx, self.looty = location
        self.newloot = Loot()
        self.lootimage = self.newloot.getimage()
        self.lootvalue = self.newloot.get(2)
        self.score.add(self.lootvalue)
        
    def additem(self, item):
        
        self.items.append(item)
        print(self.items)
        
    
    def draw(self):
        if self.rolling:
            self.roll()
          
        self.x,self.y = self.location
        self.surface.blit(itemframe, (self.x,self.y))
        if len(self.holdloot) > 0:
            toploot = self.holdloot[-1]
            topimage = toploot.getimage()
            self.surface.blit(topimage, (self.x+26,self.y+26))
# The following class determines the kind of item that will be picked up by the player. The class is instantiated when the player loots their target. 
# Once instatiated a random number is drawn, if the number is within a range then they have successfully looted an item. 
# Another random number is then drawn to determine what item they have looted. A mechanism needs to be created to direct how the item will effect gameplay.

# loot layout
# 0 = name
# 1 = effect
# 2 = value
# 3 = throwable
# 4 = img path

loots = (("Coin Bag",0,100,0,"assets/purse.png"),("Pip",1,500,1,"assets/pip.png"),("Potion of Healing",2,200,1,"assets/flask.png")) 

class Loot(object):
    def __init__(self):
        self.info = (0,0,0,0,0)
        
        self.state = 0
        
        self.decide()

    def use(self):
        pass
        
    def getinfo(self):
        return self.info
    
    def get(self, i):
        value = string = self.info[i]
        return value
    
    def getimage(self):
        string = str(self.info[4])
        print(self.info)
        image = pygame.image.load(string)
        return image
        
    def decide(self):
        decideint = random.randint(0,70)
        
        if decideint >= 0 and decideint <= 50:
            self.info = loots[0]
            self.state = 1
            
        if decideint >= 51 and decideint <= 60:
            self.info = loots[1]
            self.state = 1
            
        if decideint >= 61 and decideint <= 70:
            self.info = loots[2]
            self.state = 1
        
    def draw(self):
        pass
        