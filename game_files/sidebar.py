import pygame
pygame.init()

class Sidebar:
    og_img = pygame.image.load("images/wood.png")
    showing = True
    align = 0.8
    def __init__(self,screen):
        self.screen = screen
        self.xpos = self.screen.get_width()*self.align
        self.ypos = 0
        self.scale = (0,0)
        self.img = self.og_img.copy()
        self.resize(self.screen)

    def resize(self,screen):
        self.screen = screen
        self.xpos = self.screen.get_width() * self.align
        self.scale = ((self.screen.get_width()-self.xpos)/self.og_img.get_width(),self.screen.get_height() / self.og_img.get_height(),)
        self.img = pygame.transform.scale_by(self.og_img, self.scale)

    def draw(self):
        self.screen.blit(self.img,(self.xpos,self.ypos))
