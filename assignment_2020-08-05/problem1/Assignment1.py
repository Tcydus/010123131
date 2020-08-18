from Tree_pygame import Tree
from Readfile import readText
import pygame
from pygame.locals import *
import time
pygame.init()


scr_w, scr_h = 1400,500
screen = pygame.display.set_mode((scr_w, scr_h))

pygame.display.set_caption('Assignment 1') 
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )
font = pygame.font.Font('freesansbold.ttf', 32)

zoom = 0.38

is_running = True

GREEN = (0,255,0)
BLUE  = (0,0,255)
RED   = (255,0,0)
WHITE = (255,255,255)





text_addr = r"D:\Desktop_D\Kmutnb_Cpre\Software\2020-08-05\problem1\Expression.txt"
save_addr = r"D:\Desktop_D\Kmutnb_Cpre\Software\2020-08-05\problem1\picture"

expression = readText(text_addr)




first_time = True

while is_running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
            
    if first_time :
        first_time = False
        pic_index = 1
        for string in expression:
            
            bool_express = Tree(string)
            bool_express.setPygameScreen(scr_w,scr_h,screen)

            bool_express.infixToPostfix()
            bool_express.postfixToExpressionTree()

            screen.fill(WHITE)

            bool_express.setZoom(zoom)

            bool_express.drawExpressionTree()



            text_surface = font.render(string, True, BLUE)
            text_rect = text_surface.get_rect()
            text_rect.center = (0.5*scr_w, 0.8*scr_h)
            screen.blit(text_surface, text_rect)

            pygame.image.save(screen, save_addr+"\expression_"+str(pic_index)+".jpg")
            
            pygame.display.flip()
            pic_index +=1
            time.sleep(2)
            
        
   


print('Done....')