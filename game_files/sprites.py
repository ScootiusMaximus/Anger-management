import pygame
pygame.init()

class Sprite:
    SCALE = 5
    img = None
    width = 0
    height = 0
    needsDel = False
    name = "sprite"
    col = (0,0,0)
    def __init__(self,screen,xpos,ypos,center=True):
        self.screen = screen
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = 0
        self.yvel = 0
        self.center = center

    def draw(self):
        if self.center:
            self.screen.blit(self.img,(self.xpos-self.width//2,self.ypos-self.height//2))
        else:
            self.screen.blit(self.img,(self.xpos,self.ypos))

    def tick(self):
        self.xpos += self.xvel
        self.ypos += self.yvel

    def get_rect(self):
        return pygame.Rect(self.xpos,self.ypos,self.width,self.height)

    def __str__(self):
        return f"Sprite {self.name} pos ({self.xpos},{self.ypos})"

class Fist(Sprite):
    img = pygame.image.load("images/fist.png")
    name = "fist"
    pressed = False
    def __init__(self, screen, xpos, ypos):
        super().__init__(screen, xpos, ypos)
        self.img = pygame.transform.scale_by(self.img, self.SCALE)
        self.width, self.height = self.img.get_size()
        self.col = self.img.get_at((self.width//2,self.height//2))

class Glass(Sprite):
    img = pygame.image.load("images/glass.png")
    name = "glass"
    def __init__(self,screen,xpos,ypos):
        super().__init__(screen,xpos,ypos)
        self.img = pygame.transform.scale_by(self.img,self.SCALE)
        self.width, self.height = self.img.get_size()
        self.col = self.img.get_at((self.width // 2, self.height // 2))

class Clock(Sprite):
    img = pygame.image.load("images/clock.png")
    name = "clock"
    def __init__(self,screen,xpos,ypos):
        super().__init__(screen,xpos,ypos)
        self.img = pygame.transform.scale_by(self.img,self.SCALE)
        self.width, self.height = self.img.get_size()
        self.col = self.img.get_at((self.width // 2, self.height // 2))

class Apple(Sprite):
    img = pygame.image.load("images/apple.png")
    name = "apple"
    def __init__(self,screen,xpos,ypos):
        super().__init__(screen,xpos,ypos)
        self.img = pygame.transform.scale_by(self.img,self.SCALE)
        self.width, self.height = self.img.get_size()
        self.col = self.img.get_at((self.width // 2, self.height // 2))
