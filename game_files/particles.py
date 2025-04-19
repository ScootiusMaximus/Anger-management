import pygame
import random
import math

class Particle:
    needsDel = False
    frame = 0
    lastchange = 0
    def __init__(self,screen,xpos,ypos,maxframes=1,delay=100):
        self.screen = screen
        self.xpos = xpos
        self.ypos = ypos
        self.maxframes = maxframes
        self.delay = delay

    def tick(self,time):
        if time - self.lastchange > self.delay:
            self.frame += 1
            self.lastchange = time

        if self.frame > self.maxframes:
            self.needsDel = True

class Impact_Particle(Particle):
    def __init__(self,screen,xpos,ypos,col,size,spacing):
        super().__init__(screen,xpos,ypos,maxframes=7,delay=50)
        self.col = col
        self.size = size
        self.spacing = spacing

    def draw(self):
        points = []
        if self.frame == 0:
            points = [[0,0]]
        elif self.frame == 1:
            points = [[5,-5],[-5,-6],[9,-3],[-2,-10]]
        elif self.frame == 2:
            points = [[10,-8],[-10,-9],[18,-6],[-4,-19]]
        elif self.frame == 3:
            points = [[15,-10],[-15,-12],[27,-8],[-6,-27]]
        elif self.frame == 4:
            points = [[20,-12],[-19,-13],[34,-9],[-7,-32]]
        elif self.frame == 5:
            points = [[24,-10],[-22,-12],[38,-8],[-9,-27]]
        elif self.frame == 6:
            points = [[27,-8],[-25,-9],[41,-6],[-11,-19]]
        elif self.frame == 7:
            points = [[29,5],[-28,6],[43,3],[-12,10]]

        for item in points:
            pygame.draw.rect(self.screen,self.col,
        (self.xpos+(item[0]*self.spacing)-self.size//2,
            self.ypos+(item[1]*self.spacing)-self.size//2,self.size,self.size))

class Impact_Bits(Particle):
    def __init__(self,screen,xpos,ypos,col,size,vel,maxbits=10,minbits=3,gravity=1):
        super().__init__(screen,xpos,ypos,maxframes=1000,delay=2)
        self.col = col
        self.size = size
        self.gravity = gravity
        self.bits = []
        for _ in range(random.randint(minbits,maxbits)):
            angle = random.randint(180,360)
            xvel = vel * math.cos(math.radians(angle))
            yvel = vel * math.sin(math.radians(angle))
            self.bits.append([xpos,ypos,xvel,yvel,angle])

    def draw(self):
        for item in self.bits:
            item[0] += item[2]
            item[1] += item[3]
            item[3] += self.gravity
            pygame.draw.rect(self.screen,self.col,(item[0],item[1],self.size,self.size))
