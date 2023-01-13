import pygame

import cv2
import numpy as np

pygame.init()
screen = pygame.display.set_mode((300, 300), pygame.RESIZABLE)
clock = pygame.time.Clock()

cap = cv2.VideoCapture("test.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
class ui_object:
    def __init__(self,size_x,size_y,x_pos,y_pos,col,name):
        self.s_x = size_x
        self.s_y = size_y
        self.p_x = x_pos
        self.p_y = y_pos
        self.col = col
        self.name = name
        self.rect = pygame.Rect(self.p_x, self.p_y, self.s_x, self.s_y)

    def draw(self):
        pygame.draw.rect(screen, pygame.Color(self.col), self.rect)

    def transformScaleKeepRatio(self, size):
        iwidth = self.rect.w
        iheight = self.rect.h
        scale = min(size[0] / iwidth, size[1] / iheight)
        #scale = max(size[0] / iwidth, size[1] / iheight)
        new_size = (round(iwidth * scale), round(iheight * scale))
        self.rect = pygame.Rect(self.p_x, self.p_y,size[0] // 2, size[1] // 2)

def transformScaleKeepRatio(image, size):
    iwidth, iheight = image.get_size()
    scale = min(size[0] / iwidth, size[1] / iheight)
    #scale = max(size[0] / iwidth, size[1] / iheight)
    new_size = (round(iwidth * scale), round(iheight * scale))
    scaled_image = pygame.transform.smoothscale(image, new_size) 
    image_rect = scaled_image.get_rect(center = (size[0] // 2, size[1] // 2))
    return scaled_image, image_rect

def get_opencv_img_res(opencv_image):
    height, width = opencv_image.shape[:2]
    return width, height

def convert_opencv_img_to_pygame(opencv_image):
    
    rgb_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB).swapaxes(0, 1)
    pygame_image = pygame.surfarray.make_surface(rgb_image)

    return pygame_image

background = pygame.image.load('image.png').convert_alpha()
scaled_bg, bg_rect = transformScaleKeepRatio(background, screen.get_size())

rec = ui_object(400,300,100,200,(255,255,255),"text")

run = True
while run == True:
    clock.tick(100)
    ret, frame = cap.read()
    pygame_image = convert_opencv_img_to_pygame(frame)

    if cv2.waitKey(int(fps)) == ord('q'):
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            #scaled_bg, bg_rect = transformScaleKeepRatio(background, screen.get_size())
            rec.transformScaleKeepRatio(screen.get_size())
    screen.fill((127, 127, 127))
    screen.blit(pygame_image, (0, 0))
    screen.blit(scaled_bg, bg_rect)
    
    pygame.draw.rect(screen, pygame.Color(255,0,0), pygame.Rect(5, 5, 10, 20))
    rec.draw()
    pygame.display.flip()

pygame.quit()
exit()