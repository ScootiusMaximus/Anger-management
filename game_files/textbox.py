import pygame

class NiceTextbox:
    def __init__(self,screen,message,font,pos,textcol=(0,0,0),bgcol=None,center=True,tags=None):
        self.message = message
        self.font = font
        self.pos = pos
        self.textcol = textcol
        self.bgcol = bgcol
        self.centered = center
        self.tags = tags
        self.screen = screen
        self.text = None

        self.pressable = False
        self.textrect = pygame.Rect(0,0,0,0)
        self.pressed = False
        self.wasPressed = False

        self.update()

    def move_to(self,pos):
        self.pos = pos
        self.update()

    def update(self):
        self.text = self.font.render(str(self.message), True, self.textcol, self.bgcol)
        self.textrect = self.text.get_rect()
        self.textrect.center = self.pos

    def display(self):
        self.screen.blit(self.text, self.textrect)

    def is_pressed(self):
        mpos = pygame.mouse.get_pos()
        mousepress = pygame.mouse.get_pressed()[0]

        press = (pygame.Rect.colliderect(pygame.Rect(mpos[0],mpos[1],3,3),self.textrect)
                and self.pressable and mousepress and not self.wasPressed)
        self.wasPressed = mousepress
        return press

    def is_hover(self):
        mpos = pygame.mouse.get_pos()
        return pygame.Rect.colliderect(pygame.Rect(mpos[0],mpos[1],3,3),self.textrect) and self.pressable

    def set_message(self,message):
        self.message = message
        self.update()

    def set_textcol(self,col):
        self.textcol = col
        self.update()

    def set_bgcol(self,col):
        self.bgcol = col
        self.update()

class Pressable:
    def __init__(self,xpos,ypos,width,height,mode=1,center=False):
        '''mode 1 - hover to press
        mode 2 - click to press'''
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.mode = mode
        self.center = center

        self.pressable = True
        self.wasPressed = False
        self.rect = [0,0,0,0]
        self.move_to(xpos,ypos)

    def move_to(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        if self.center:
            self.rect = [xpos - self.width // 2, ypos - self.height // 2, self.width, self.height]
        else:
            self.rect = [xpos, ypos, self.width, self.height]

    def pressed(self):
        press = False
        left, right, up, down = False, False, False, False

        mousepress = pygame.mouse.get_pressed()[0]
        mpos = pygame.mouse.get_pos()
        if mpos[0] > self.rect[0]:
            left = True
        if mpos[0] < self.rect[0] + self.rect[2]:
            right = True
        if mpos[1] > self.rect[1]:
            up = True
        if mpos[1] < self.rect[1] + self.rect[3]:
            down = True

        if self.mode == 1:
            press = up and down and left and right

        elif self.mode == 2:
            press = up and down and left and right and mousepress

        elif self.mode == 3:

            press = (pygame.Rect.colliderect(pygame.Rect(mpos[0], mpos[1], 3, 3),
                pygame.Rect(self.xpos,self.ypos,self.width,self.height))
                     and self.pressable and mousepress and not self.wasPressed)
            self.wasPressed = mousepress
        return press

class Button(Pressable):
    def __init__(self,screen,xpos,ypos,image,mode=2,center=False):
        self.image = image
        self.screen = screen
        super().__init__(xpos,ypos,image.get_width(),image.get_height(),mode,center)

    def draw(self):
        if self.center:
            xmod = self.image.get_width()//2
            ymod = self.image.get_height()//2
        else:
            xmod = 0
            ymod = 0

        self.screen.blit(self.image,(self.xpos-xmod,self.ypos-ymod))