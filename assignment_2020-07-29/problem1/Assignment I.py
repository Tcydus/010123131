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
pygame.display.set_caption('Assignment1') 

surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )


img = None
is_running = True 
draw_first = True
else_flag = False

M,N = 3,3
all_block = M*N
rw, rh = scr_w//M, scr_h//N
alldel_list = [None] * all_block # hold all row & col list that you want to delete
alldel_list_index =0

def checkColRow(x,y):
    '''
    function that find column and row by 
    division and floor x by block width and division and floor y by block height
    '''
    global rw, rh
    return x//rw,y//rh


while is_running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
            
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if alldel_list[-1] == None : 
                
                del_col,del_row = checkColRow(e.pos[0],e.pos[1]) #get row and col position that you click
                del_list = [del_col,del_row] # create a list of that

                if del_list not in alldel_list: 
                    alldel_list[alldel_list_index] = del_list #put a del_list into all_dellist
                    alldel_list_index +=1 #update all_dellist index 
                # print(alldel_list)
            
    img = camera.get_image()
    if img is None:
        continue

    img_rect = img.get_rect()
    img_w, img_h = img_rect.w, img_rect.h

 
    surface.blit(img, (0,0)) 

    if alldel_list[-1] == None :
        for i in range(M):
            for j in range(N):

                draw_list = [i,j]  #create a list that hold a row & column want you want to draw

                if draw_list in alldel_list: 
                    continue                #didn't draw a black rect and green rect line
               
                # draw a green frame (tile)
                rect = (i*rw, j*rh, rw, rh)
                
                pygame.draw.rect(img,(0,0,0),rect,0)  #draw black rect
                pygame.draw.rect( img, (0,255,0), rect,1)  #draw green rect line
                surface.blit( img, rect, rect )
    

    # write the surface to the screen and update the display
    screen.blit( surface, (0,0) )
    pygame.display.flip()

# close the camera
camera.stop()

print('Done....')