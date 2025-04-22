import pygame

pygame.init()

class Image_Loader:
    bg = pygame.image.load("images/background.png")
    def __init__(self,width,height):
        self.w = width
        self.h = height
        self.background = self.transform(self.bg)

    def transform(self,img):
        return pygame.Surface.convert(pygame.transform.scale_by(img,(self.w/img.get_width(),self.h/img.get_height())))


