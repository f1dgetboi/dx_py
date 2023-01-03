import pygame, sys
import os

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
#screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
dirlist = []
for root, dirs, files in os.walk("projects", topdown=False):
        for name in dirs:
            dirlist.append(os.path.join(name))
fullscreen = False
FIRST_FRAME_X = 100
FIRST_FRAME_Y = 85


def create_window(width, height,background_colour,caption):
    global screen, bg_colour
    bg_colour = background_colour
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE,32)
    pygame.display.set_caption(str(caption))
    screen.fill(background_colour)
    pygame.display.flip()


class ui_object:
    def __init__(self,size_x,size_y,x_pos,y_pos,col):
        self.s_x = size_x
        self.s_y = size_y
        self.p_x = x_pos
        self.p_y = y_pos
        self.col = col

    def draw(self):
        pygame.draw.rect(screen, pygame.Color(self.col), pygame.Rect(self.p_x, self.p_y, self.s_x, self.s_y))
        #font = pygame.font.SysFont(None, 24)
        #img = font.render(self.text, True, (255,255,255))
        #screen.blit(img, (self.p_x, self.p_y))

class button(ui_object):

    def __init__(self,size_x,size_y,x_pos,y_pos,col,text,fontsize,f_col,font=None,childs=None):
        super().__init__(size_x,size_y,x_pos,y_pos,col)
        if childs is None :
            childs = []
        self.childs = childs
        self.text = text
        self.fontsize = fontsize
        if font is None :
            font = None
        self.font = font
        self.rect = pygame.Rect(self.p_x, self.p_y, self.s_x, self.s_y)
        self.clicked = False
        self.Hover = False
        self.f_col = f_col

    def add_child(self,nem):
        if nem not in self.childs:
            self.childs.append(nem)

    def remove_child(self,nem):
        if nem in self.childs:
            self.childs.remove(nem)
    
    
    def draw_b(self,text_offset_x,text_offset_y):
        pygame.draw.rect(screen, pygame.Color(self.col), self.rect)
        font = pygame.font.SysFont(None, self.fontsize)
        text = font.render(self.text, True, (self.f_col))
        screen.blit(text, (self.p_x + text_offset_x,self.p_y+text_offset_y))
          
    def check_state(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True


class image_button(button):
    def __init__(self,size_x,size_y,x_pos,y_pos,col,text,fontsize,f_col,font=None,childs=None,image=None):
        super().__init__(size_x,size_y,x_pos,y_pos,col,text,fontsize,f_col,font=None,childs=None)
        if image is None:
            image = None
        self.image = pygame.image.load(image)

    def draw_image(self):
        self.image = pygame.transform.scale(self.image, (self.s_x, self.s_y))
        self.rect = self.image.get_rect()
        self.rect.x = self.p_x
        self.rect.y = self.p_y
        screen.blit(self.image,(self.rect.x,self.rect.y))

create_project = button(200,40,10,840,(21,21,21),"Create Project",40,(255,255,255))

class frames(ui_object):
    def __init__(self,x_pos,y_pos):
        super().__init__(self,x_pos,y_pos)

    def create_frame(self):
        image_button(260,175,self.p_x,self.p_y,(0,255,0),"",50,(0,0,0),None,None,"image.png")
        button(290,220,self.p_x - 15,self.p_x - 15,(21,21,21),str(name),40,(255,255,255))
        button.draw_b(100,190)
        image_button.draw_image()       


def create_project_frame(x,y):
    image = image_button(260,175,x,y,(0,255,0),"",50,(0,0,0),None,None,"image.png")
    frame = button(290,220,x - 15,y - 15,(21,21,21),str(name),40,(255,255,255))
    frame.draw_b(100,190)
    image.draw_image()        
    i = len(dirlist)
    if i/4 == 0:
        e += 1
    print(i)

create_window(1280,720,(40, 40, 43),"siuu")
frame = frames(FIRST_FRAME_X,FIRST_FRAME_Y)

while True:
    for i in range(5):
        frame.draw(FIRST_FRAME_X + 1*15,FIRST_FRAME_Y + i*15)
    screen.fill(bg_colour)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONDOWN:
                print("pressed")
                #if image.rect.collidepoint(event.pos):
                    #print("i")
        if event.type == KEYDOWN:
            #print("x "+str(image.p_x) + " " + "y "+str(image.p_y) + "\n size x" + str(image.s_x) + "size y" + str(image.s_y))
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                """
                if event.key == K_DOWN:
                    image.p_y += 5
                if event.key == K_UP:
                    image.p_y -= 5
                if event.key == K_RIGHT:
                    image.p_x += 5
                if event.key == K_LEFT:
                    image.p_x -= 5
                if event.key == K_m:
                    image.s_x +=5
                if event.key == K_n:
                    image.s_x -=5
                if event.key == K_x:
                    image.s_y +=5
                if event.key == K_c:
                    image.s_y -=5
                """
            
                
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)


        create_project.draw_b(0,5)
        #create_project_frame(FIRST_FRAME_X,FIRST_FRAME_Y)
        pygame.display.update()
        mainClock.tick(60)



