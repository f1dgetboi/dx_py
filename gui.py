import pygame, sys
import os
from pathlib import Path
from moviepy.editor import VideoFileClip, TextClip
import re
import cv2

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

dirlist = []

for root, dirs, files in os.walk("projects", topdown=False):
        for name in dirs:
            dirlist.append(os.path.join(name))

fullscreen = False
FIRST_FRAME_X = 120
FIRST_FRAME_Y = 85
font = pygame.font.SysFont(None, 32)
state = 1
middle_frame_state = False
def add_subtitles(video_file, subtitles_file):
    video = VideoFileClip(video_file)
    subtitles = TextClip(subtitles_file, fontsize=24, color='white')
    final_video = video.set_audio(subtitles)
    final_video.write_videofile("output.mp4")
    print('Subtitles added successfully!')

#add_subtitles('ok.mp4', 'subtitles.srt')
def create_text(fontsize,col,x,y,t):
    font = pygame.font.SysFont(None, fontsize)
    text = font.render(t, True, (col))
    screen.blit(text, (x,y))

def create_window(width, height,background_colour,caption):
    global screen, bg_colour,WIDTH,HEIGHT
    WIDTH = width
    HEIGHT = height
    bg_colour = background_colour
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF |pygame.RESIZABLE)
    pygame.display.set_caption(str(caption))
    screen.fill(background_colour)
    pygame.display.flip()

class ui_object():
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

class error_text:
    def __init__(self,error,alpha):
        if alpha == 255 or alpha < 0:
            self.alpha = 255
        else:
            self.alpha = alpha
        if self.alpha == 255 or self.alpha < 0:
            self.y = 20
        self.font = pygame.font.SysFont(None, 50)
        self.textsurface = font.render(error, True, (255, 0, 0))
    
    def draw(self):
        self.alpha -= 4
        self.y += .5         
        self.textsurface.set_alpha(self.alpha)
        screen.blit(self.textsurface,(WIDTH/2,self.y))

    def update(self):
        if self.alpha < 0:   
            self.alpha = 255
            self.y = 20
            return False
        else: 
            return True
    
class button(ui_object):

    def __init__(self,size_x,size_y,x_pos,y_pos,col,text,fontsize,f_col,font=None,linewidth=None,childs=None):
        super().__init__(size_x,size_y,x_pos,y_pos,col)
        if childs is None :
            self.childs = []
        self.childs.append(childs)
        self.text = text
        self.fontsize = fontsize
        if font is None :
            font = None
        if linewidth == None :
            linewidth = None
        self.linewidth = linewidth
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
        if self.linewidth is not None:
            pygame.draw.rect(screen, pygame.Color(255,255,255),pygame.Rect(self.p_x, self.p_y, self.s_x + self.linewidth, self.s_y+ self.linewidth))
        pygame.draw.rect(screen, pygame.Color(self.col), self.rect)
        font = pygame.font.SysFont(None, self.fontsize)
        text = font.render(self.text, True, (self.f_col))
        screen.blit(text, (self.p_x + text_offset_x,self.p_y+text_offset_y))
          
    def check_state(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True


class image_button(button):
    def __init__(self,size_x,size_y,x_pos,y_pos,col,text,fontsize,f_col,font=None,childs=None,image=None):
        super(image_button,self).__init__(size_x,size_y,x_pos,y_pos,col,text,fontsize,f_col,font=None,childs=None)
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

class frames():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y  
        self.z = z 
        self.image = image_button(260,175,self.x,self.y,(0,255,0),"",50,(0,0,0),None,None,"image.png")
        self.rect = pygame.Rect(self.x, self.y, 290, 220)

    def create_project_frame(self):
        image = image_button(260,175,self.x,self.y,(0,255,0),"",50,(0,0,0),None,None,"image.png")
        frame = button(290,220,self.x - 15,self.y - 15,(21,21,21),dirlist[self.z],40,(255,255,255))
        frame.draw_b(100,190)
        image.draw_image()        

class TextBox:
    def __init__(self, x, y, width, height, font, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.color = (255, 255, 255)  # White
        self.text = text
        self.scroll = 10
        self.cursor = True
        self.cursor_timer = 0
        self.cursor_interval = 500  # milliseconds

        # Pre-render the text to improve performance
        self.text_surface = self.font.render(text, True, (0, 0, 0))  # Black text with per-pixel alpha blending
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Handle key press events
            if event.key == pygame.K_BACKSPACE:
                # If the user pressed the backspace key, remove the last character from the text
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                # If the user pressed the enter key, return True to signal that the user is finished inputting text
                return True
            else:
                # If the user pressed any other key, add it to the text
                self.text += event.unicode

            # Update the pre-rendered text
            self.text_surface = self.font.render(self.text, True, (0, 0, 0))  # Black text with per-pixel alpha blending
            self.text_rect = self.text_surface.get_rect()
            self.text_rect.center = self.rect.center
            self.cursor_timer = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.cursor_timer > self.cursor_interval:
            self.cursor = not self.cursor
            self.cursor_timer = pygame.time.get_ticks()

    def draw(self, surface):
        # Render the textbox
        pygame.draw.rect(surface, self.color, self.rect)

        # Render the text
        surface.blit(self.text_surface, self.text_rect)
        if self.cursor:
            cursor_height = self.font.size("A")[1]
            cursor_x = self.text_rect.right
            cursor_y = self.text_rect.top + (self.text_rect.height - cursor_height) / 2
            pygame.draw.line(surface, (0, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

class menu():
    def __init__(self,size_x,size_y,x_pos,y_pos,visibletext,child):
        self.childs = child
        self.w = size_x
        self.h = size_y
        self.x = x_pos
        self.y = y_pos
        self.clicked = False
        self.button = button(self.w,self.h,self.x,self.y,(43,43,43),visibletext,40,(255,255,255),font,3)
        self.button.p_x = self.x
        self.button.p_y = self.y
        self.button.s_x = self.w
        self.button.s_y = self.h
        self.options = []
        self.count = 0
        for i in self.childs:
            self.count += 1
            self.options.append(button(self.w,self.h,self.x , self.y + (self.h*self.count) + 3 ,(43,43,43),i,40,(255,255,255),font,3))
            pygame.draw.line(screen,pygame.Color(255,255,255),(self.x - self.w/2,self.y + self.h/2),(self.x + self.w/2,self.y + self.h/2),3)

    def handel_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(self.clicked)
            if self.button.rect.collidepoint(event.pos):
                if self.clicked:
                    self.clicked = False
                else:
                    self.clicked = True

    def draw(self):
        self.button.draw_b(0,0)
        if self.clicked == True:
            for i in self.options:
                i.draw_b(0,0)
            

class Video():
    def __init__(self,video_name,x,y,width,height):
        self.cap = cv2.VideoCapture(video_name)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x + 8,y + 8,width,height)
    

    def draw(self):
        ret, self.frame = self.cap.read()
        self.rgb_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB).swapaxes(0, 1)
        self.pygame_image = pygame.surfarray.make_surface(self.rgb_image)
        self.pygame_image = pygame.transform.scale(self.pygame_image, (self.width,self.height))
        cv2.waitKey(int(self.fps))
        pygame.draw.rect(screen,pygame.Color(22,22,22),pygame.Rect(self.x ,self.y,self.width + 16 ,self.height + 16))
        screen.blit(self.pygame_image, (self.x + 8, self.y + 8))

create_window(1280,720,(40, 40, 43),"siuu")
pop_up = button(500,250,WIDTH/2 - 100,HEIGHT/2,(40, 40, 43),"",40,(255,255,255))
win_white = button(500,25,WIDTH/2 - 100,HEIGHT/2,(255,255,255),"Create Project",30,(0,0,0))
pop_up_cancel = button(100,35,WIDTH/2 - 90,HEIGHT/2 + 200,(22,22,22),"cancel",45,(255,255,255))
pop_up_create = button(95,35,WIDTH/2 + 290,HEIGHT/2 + 200,(22,22,22),"create",45,(255,255,255))
textbox = TextBox(WIDTH/2 - 60 ,HEIGHT/2 + 100, 200, 32, font)
open_menu = menu(100,35,0,0 ,"Open",["Project","Video","Photo",])
tools_menu = menu(100,35,0,35 ,"Open",["Project","Video","Photo",])
video_frame = Video("test.mp4",WIDTH/2 - 135,HEIGHT/2 - 275,900,506)
video_frame_button = button(100,40,WIDTH/2 - 135,43,(55,55,55),"Video",45,(255,255,255),font,3)
mediapool_button = button(170,40,WIDTH/2 - 32,43,(22,22,22),"Media Pool",45,(255,255,255),font,3)
p_up = False
f_group = []
error_list = [error_text("cant create project with same name",255)]
error_draw = []


def create_drop_shadow(rect):
    shadow_surface = pygame.Surface((rect.width + 3, rect.height + 3 ))
    shadow_surface.set_alpha(2)
    for i in range(-5, 4):
        for j in range(-5, 4):
            screen.blit(shadow_surface, (rect.x + i , rect.y + j))
    
def draw_background():
    pygame.draw.rect(screen,pygame.Color(22,22,22),pygame.Rect(0,40,WIDTH/2 - 140,1000))
    pygame.draw.line(screen,pygame.Color(255,255,255),(WIDTH/2 - 140,40),(WIDTH/2 - 140,1300),5)
    pygame.draw.rect(screen,pygame.Color(22,22,22),pygame.Rect(WIDTH/2 - 135,HEIGHT/2 + 200,916,540))
    pygame.draw.line(screen,pygame.Color(255,255,255),(WIDTH/2 - 140,HEIGHT/2 + 250),(1420,HEIGHT/2 + 250),5)
    pygame.draw.rect(screen,pygame.Color(22,22,22),pygame.Rect(1425,40,WIDTH/2 - 140,1000))
    pygame.draw.line(screen,pygame.Color(255,255,255),(1423,40),(1423,1000),5)
    pygame.draw.line(screen,pygame.Color(255,255,255),(0,41),(2000,41),3)

def draw_all():
    screen.fill(bg_colour)
    if state == 0:
        c = 0
        for i in dirlist:
            if c/5 == 0 and c != 0:
                if len(dirlist) > len(f_group):
                    f_group.append(frames(FIRST_FRAME_X ,FIRST_FRAME_Y + c*260 ,c))
            else:
                if len(dirlist) > len(f_group):
                    f_group.append(frames(FIRST_FRAME_X + c * 260 + 100 * c,FIRST_FRAME_Y ,c))
            c += 1
        
        for i in f_group:
            i.create_project_frame()
        create_project.draw_b(0,5)
        if p_up == True:
            create_drop_shadow(pop_up.rect)
            pop_up.draw_b(10,10)
            win_white.draw_b(10,2)
            pop_up_cancel.draw_b(0,2)
            pop_up_create.draw_b(0,2)
            create_text(40,(255,255,255),WIDTH/2 - 60 ,HEIGHT/2 + 60,"Name")
            textbox.draw(screen)
            textbox.update()
        for i in error_draw:
            if i.update() == False:
                error_draw.remove(i)
            i.draw()
    if state == 1:
        draw_background()
        open_menu.draw()
        video_frame_button.draw_b(5,5)
        mediapool_button.draw_b(5,5)
        
        video_frame.draw()
    #print(state)
    #create_project_frame(FIRST_FRAME_X,FIRST_FRAME_Y)
    pygame.display.update()
    

while True:

    draw_all()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONDOWN:
            open_menu.handel_event(event)
            if create_project.rect.collidepoint(event.pos):
                p_up = True
                #print("pressed")
            if state == 1 and mediapool_button.rect.collidepoint(event.pos) :
                middle_frame_state = True
                mediapool_button.col = (55,55,55)
                video_frame_button.col = (22,22,22)

            if state == 1 and video_frame_button.rect.collidepoint(event.pos):
                middle_frame_state = False
                video_frame_button.col = (55,55,55)
                mediapool_button.col = (22,22,22)

            if p_up == True and pop_up_cancel.rect.collidepoint(event.pos):
                p_up = False
                #print("pressed")
            if p_up == True and pop_up_create.rect.collidepoint(event.pos):
                newpath = Path("projects/" + textbox.text)
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                else:
                    error_draw.append(error_list[0])
                p_up = False
                state = 1
                for root, dirs, files in os.walk("projects", topdown=False):
                    for name in dirs:
                        if name not in dirs:
                            dirlist.append(os.path.join(name))
    

        if event.type == KEYDOWN:
            #print("x "+str(image.p_x) + " " + "y "+str(image.p_y) + "\n size x" + str(image.s_x) + "size y" + str(image.s_y))
            textbox.handle_event(event)
                

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
                
            if event.key == K_LALT and K_KP_ENTER:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)

            mainClock.tick(30)






