import pygame
import random
import math
import time
from entities import *

# the following are my color standards
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)
air = (255,0,255)

mainfont = "assets/boot.ttf"
background = pygame.image.load('assets/background.png')
splash = pygame.image.load('assets/splash.png')
heart = pygame.image.load('assets/heart.png')
halfheart = pygame.image.load('assets/halfheart.png')
itemframe = pygame.image.load('assets/itemframe.png')
itembubble = pygame.image.load('assets/bubble.png')
flasksmall = pygame.image.load('assets/flasksmall.png')
pipsmall = pygame.image.load('assets/pipsmall.png')
pursesmall = pygame.image.load('assets/pursesmall.png')


glasses = []

for i in range(15):
    imagename = "glass" + str(int(i)) + ".png"
    fullpath = "assets/" + imagename
    image = pygame.image.load(fullpath)
    glasses.append(image)


#the following function measures distance
def getdist(targeta,targetb):
    ax, ay = targeta.getpos()
    bx, by = targetb.getpos()

    dist = math.hypot(ax-bx,ay-by)
    return dist
    
# The following class is to handle interval timers.
class timer(object):

    # Constructor code logs the time it was instantiated.    
    def __init__(self):
        self.timeInit = time.time()

    # The following funtion returns the last logged value.        
    def timestart(self):
        return self.timeInit
        
    # the following function updates the time log with the current time.
    def logtime(self):
        self.lastTime = time.time()

    # the following function returns the interval that has elapsed since the last log.        
    def timelapsed(self):
        self.timeLapse = time.time() - self.lastTime
        #print(self.timeLapse)
        return self.timeLapse



# the following class is used to display images
class Image(object):
    def __init__(self):
        self.x = 258
        self.y = 66
        self.Img = heart
    
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
# it returns a list of strings indicating what state the keys are at.

def getkeys():
    
    direction = []
    key = pygame.key.get_pressed()

    
    
    if key[pygame.K_SPACE]:
        direction.append("loot")

    if key[pygame.K_HOME]:
        direction.append("loot")

    if key[pygame.K_LSHIFT]:
        direction.append("use")

    if key[pygame.K_PAGEDOWN]:
        direction.append("use")


    if key[pygame.K_LEFT]:
        direction.append("left")
        
    if key[pygame.K_RIGHT]:
        direction.append("right")
        
    if key[pygame.K_UP]:
        direction.append("up")
        
    if key[pygame.K_DOWN]:
        direction.append("down")

    return direction


class stealthbox(object):
    def __init__(self,x,y,surface,enemy, bush, hero):
        self.hero = hero
        self.enemy = enemy
        self.bush = bush
        self.meter = Box()
        self.metervalue = 0
        self.metermax = 122
        self.x = x
        self.y = y
        self.surface = surface
        self.effector = 3
        self.cool = .1
        self.coolfast = 5
        self.colour = [255,255,255]
        
    def get(self):
        if self.metervalue >= self.metermax:
            return True
        else:
            return False
    
    def colourize(self):
        #print(self.metervalue)
        #print("made it to colourize")
        if self.metervalue > 0:
            scaler = (self.metervalue / self.metermax)
        else:
            scaler = 0
        #print(scaler)
        r = 255 * scaler
        g = 0
        b = 255 - r   
        
        self.colour = [r,g,b]
        
        for i in range(len(self.colour)):
            if self.colour[i] > 255:
                self.colour[i] = 255
            if self.colour[i] < 0:
                self.colour[i] = 0     
        #print(self.colour)
        
    def bound(self):
        if self.metervalue > self.metermax:
            self.metervalue = self.metermax
            
        if self.metervalue < self.x:
            self.metervalue = self.x
    
    def effected(self,amount):
        self.amount = amount
        self.metervalue = self.metervalue + self.amount
    
    def tick(self):
        dist = getdist(self.hero,self.enemy)
        #print(dist)
        herowalking = self.hero.walking()
        
        #print(herowalking)
        self.rando = random.randint(0,100)

        self.rando = self.rando / float(100)


        #print(self.rando)
        
        self.randeffect = self.rando * self.effector
        #print(self.randeffect)
        self.scaled  = self.randeffect - int(dist * .01)
        
        if herowalking:
            if self.metervalue < self.metermax:
                self.metervalue += self.scaled
        else:
            if self.metervalue > self.x:
                if self.check():
                    self.metervalue -= self.coolfast
                    
                else:
                    self.metervalue -= self.cool
        self.bound()
        self.colourize()
        
        r,g,b = self.colour[0], self.colour[1],self.colour[2]
                
        self.meter.update(self.x,self.y, (self.metervalue,10), (r,g,b))
        self.meter.draw(self.surface)

        return self.metervalue 

    def draw(self):

        self.metervalue += .5
        if self.metervalue  > self.metermax:
            self.metervalue = self.metermax
        self.meter.update(self.x, self.y, (self.metervalue,10), (r,g,b))
        self.meter.draw(self.surface)
        return self.metervalue

    def check(self):
        
        collidersum = 0
        
        for i in range(len(self.bush)):
            rectollide = pygame.sprite.collide_rect(self.bush[i],self.hero)
            collision = pygame.sprite.collide_mask(self.bush[i], self.hero)
            
            if rectollide:
                if collision:
                    collidersum +=1
            
        if collidersum > 0:
            self.hidden = True
        else:
            self.hidden = False
        
        return self.hidden
        
# this class is the (now deprecated) stealth meter. 
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

class leveltimer(object):
    def __init__(self, surface, time = 60):
        self.time = time
        
        # 15 different increments of the timer.
        self.increments = self.time / 15
        self.timerobj = timer()
        self.timerobj.logtime()
        self.surface = surface
        
    def draw(self):
        # checks the time, draws the hourglass. If time is left return true, if time has elapsed then return false.
        self.timelapsed = self.timerobj.timelapsed()
        
        if self.timelapsed > self.time:
            return False
        
        self.timedivision = self.timelapsed / self.increments
        
        imagetoshow = int(self.timedivision)
        self.surface.blit(glasses[imagetoshow], (700,0))
        
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
            
            

class effect(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image, facing):
        
        # Call the parent class (Sprite) constructor
        super(effect,self).__init__()
        self.decide = image
        self.facing = facing
        if self.decide == 0:
            self.image = pursesmall
        if self.decide == 1:
            self.image = pipsmall
        if self.decide == 2:
            self.image = flasksmall
            
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.tick = float(0)
        self.busy = True
    
    def sinwave(self,tick):
        y = math.sin(math.radians(self.tick))

        test = y * 40

        return test
    
    def active(self):
        return self.busy
  
    def update(self,x,y):

        length = 100
        distscaler = float(self.tick) / 188

        if self.facing == "right":
            distance = x + (length * distscaler)
        else:
            distance = x - (length * distscaler)
        adjust = y -(self.sinwave(self.tick))
        
        self.rect.center = distance,adjust
        
        if self.tick < 188:
            self.tick += 20
        
        if self.tick >= 188:
            self.busy = False

# the following class handles the location of items.
class itemFrame(object):
    # it asks for the position on screen to draw, the screen object to draw to and the score object to tell it when new loot is added.
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
        
        self.state = 0
        
        
    def use(self,hero):
        
        if len(self.holdloot) > 0 and self.state == 0:

            toploot = self.holdloot.pop()
            
            usedimage = toploot.use()
            
            herorect,herofacing = hero.getrect()
            
            self.startposx,self.startposy = herorect.center
            
            self.state = 1
            
            self.sprite = effect(self.startposx,self.startposy,usedimage,herofacing)
            
            self.usedsprite = pygame.sprite.LayeredUpdates()
            
            self.usedsprite.add(self.sprite)
            
            self.throw()
            
    def throw(self):

        self.sprite.update(self.startposx,self.startposy)
        
        if self.sprite.active() == False:

            self.state = 0
        
    def roll(self):
       if self.rolling == True:
            self.surface.blit(itembubble, (self.lootx+10,self.looty-142))
            self.surface.blit(self.lootimage, (self.lootx+10,self.looty-142))
            print("made it to rolling")
            self.holdloot.append(self.newloot)
            self.rolling = False

    def new(self,location):
        self.lasttime = pygame.time.get_ticks()
        self.rolling = True
        self.lootx, self.looty = location
        self.newloot = Loot()
        self.lootimage = self.newloot.getimage()
        self.lootvalue = self.newloot.get(2)
        self.score.add(self.lootvalue)
        self.getsound = pygame.mixer.Sound("assets/get.ogg")
        self.getsound.play()
        
    def additem(self, item):
        print("added item")
        self.items.append(item)

        
    
    def draw(self):
        if self.rolling:
            self.roll()
          
        self.x,self.y = self.location
        self.surface.blit(itemframe, (self.x,self.y))
        if len(self.holdloot) > 0:
            toploot = self.holdloot[-1]
            topimage = toploot.getimage()
            self.surface.blit(topimage, (self.x+26,self.y+26))
            
        if self.state == 1:
            self.throw()
            self.usedsprite.draw(self.surface)
            
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
        
        # create an empty set of values for the object
        self.info = (0,0,0,0,0)
        
        # set the state of creation at 0
        self.state = 0
        
        # run the decision function that determines the attributes of the item
        self.decide()

    def use(self):
        return self.determine
        
    def getinfo(self):
        return self.info
    
    def get(self, i):
        value = string = self.info[i]
        return value
    
    def getimage(self):
        string = str(self.info[4])

        image = pygame.image.load(string)
        return image
        
    def decide(self):

        # create a random number between 0 and 70
        decideint = random.randint(0,70)
        
        #place the random number in a class attribute
        self.decideint = decideint
        
        # Filter the result into a set of possible outcomes
        if decideint >= 0 and decideint <= 50:
            # set the item ID
            self.determine = 0
            
            self.info = loots[0]
            self.state = 1
            
        if decideint >= 51 and decideint <= 60:
            #set the item ID
            self.determine = 1
            
            self.info = loots[1]
            self.state = 1
            
        if decideint >= 61 and decideint <= 70:
            # set the item ID
            self.determine = 2
            
            self.info = loots[2]
            self.state = 1
        
    def draw(self):
        pass
        
