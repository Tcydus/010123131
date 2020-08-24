from tree import Tree
from drawtree import DrawTree
from readfile import readText
import pygame
from pygame.locals import *

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





text_addr = r"Expression.txt"  #edit to path that you read Expression.txt.
save_addr = r"\picture"         #edit to path that you want to save picture.


expression = readText(text_addr)
pic_index = 0 




first_time = True
mouse_pressed = False

while is_running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            pic_index  = (pic_index +1) % len(expression)



            
    bool_express = Tree(expression[pic_index])


    bool_express.infixToPostfix()
    bool_express.postfixToExpressionTree()

    screen.fill(WHITE)

    pygame_drawtree = DrawTree(bool_express.expression_tree)
    pygame_drawtree.set_pygame_screen(scr_w,scr_h,screen)
    pygame_drawtree.set_scale(zoom)
    pygame_drawtree.draw()




    text_surface = font.render(expression[pic_index], True, BLUE)
    text_rect = text_surface.get_rect()
    text_rect.center = (0.5*scr_w, 0.8*scr_h)
    screen.blit(text_surface, text_rect)

    pygame.image.save(screen, save_addr+"\expression_"+str(pic_index)+".jpg")
    
    pygame.display.flip()

            
        
   


print('Done....')
