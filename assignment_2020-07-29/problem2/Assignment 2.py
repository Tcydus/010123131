import pygame
import pygame.camera
from pygame.locals import *
import sys

def open_camera( frame_size=(1280,720),mode='RGB'):
    pygame.camera.init()
    list_cameras = pygame.camera.list_cameras()
    print( 'Member of cameras found: ', len(list_cameras) )
    if list_cameras:
        # use the first camera found
        camera = pygame.camera.Camera(list_cameras[0], frame_size, mode )
        return camera 
    return None 

scr_w, scr_h = 1280,720

pygame.init()
camera = open_camera()

if camera:
    camera.start()
else:
    print('Cannot open camera')
    sys.exit(-1)

screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption('Assignment 2') 

surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )


img = None
is_running = True 
draw_first = True
GREEN = (0,255,0)

M,N = 2,3                           # assign max column and max row
all_block = M*N
rect_list = [None] * all_block      # list that hold a original rectangle 
rect2_list = [None] * all_block     # list that hold a swap rectangle 
m_downcol,m_downrow,index_downrect = None,None,None

rw, rh = scr_w//M, scr_h//N



class Rect:
    '''
        This class holding value to draw a rectangle
    '''
    def __init__(self,x_start,y_start,rw,rh):
        self.x_start = x_start
        self.y_start = y_start
        self.rw = rw
        self.rh = rh
    def useRect(self):
        return (self.x_start, self.y_start,self.rw, self.rh)

    

def checkColRow(x,y):
    '''
    function that find column and row by 
    division and floor x by block width and division and floor y by block height
    '''
    global rw, rh
    return x//rw,y//rh

def findIndex(col,row):
    '''
    function that find index of rectangular object list
    by multiple col by N(max row) and adding row

    if M(max column) = 2 N(max row) = 3 rectangle index will be
        | 0 | 3 |
        | 1 | 4 |
        | 2 | 5 |
    '''
    
    global N
    return col*N + row


while is_running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
            
        elif e.type == pygame.MOUSEBUTTONDOWN:
            # find a row and column that you drag
            m_downcol,m_downrow = checkColRow(e.pos[0],e.pos[1])

            # find an index of rectangle that you drag
            index_downrect = findIndex(m_downcol,m_downrow)
           


        elif e.type == pygame.MOUSEBUTTONUP:
            # find a row and column that you drop  
            m_upcol,m_uprow = checkColRow(e.pos[0],e.pos[1])

            # find an index of rectangle that you drop
            index_uprect = findIndex(m_upcol,m_uprow)

            # swap rectangle between a mouse drag rectangle and a mouse drop rectangle
            rect2_list[index_uprect],rect2_list[index_downrect] = \
            rect2_list[index_downrect],rect2_list[index_uprect]

        

    img = camera.get_image()
    if img is None:
        continue

    img_rect = img.get_rect()
    img_w, img_h = img_rect.w, img_rect.h

 
    index_rect_list = 0
    
    for i in range(M):
        for j in range(N):

            if draw_first :
                # create a rectangle object
                myrect = Rect(i*rw, j*rh, rw, rh)    

                # assign a rectangle object into list 
                # at first rect2_list = rect1_list (when you didn't swap any rectangle)
                rect_list[index_rect_list] = myrect
                rect2_list[index_rect_list] = myrect

            # get a set of value in rectangle object list into variable
            rect_pos = rect_list[index_rect_list].useRect() 
            rect_area = rect2_list[index_rect_list].useRect()

            # draw green rectangle line
            pygame.draw.rect( img, GREEN, rect_area,1) 

            # blit image rectangle area at rectangle positon
            surface.blit( img, rect_pos,rect_area)
            
            # update all index rectangle list
            index_rect_list += 1

    
    # disable command that create rectangle object into list 
    draw_first = False
    

    # write the surface to the screen and update the display
    screen.blit( surface, (0,0) )
    pygame.display.flip()

# close the camera
camera.stop()

print('Done....')