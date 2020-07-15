################################################################
 # 6201012610061 
 # Coding for assignment 1
################################################################
import math
import pygame 
from random import randint

allcircle_list = []
target_index = 0

def checkOverlap(cir1_x,cir1_y,cir1_r,cir2_x,cir2_y,cir2_r):
    distance = math.sqrt((cir1_x-cir2_x)**2 + (cir1_y-cir2_y)**2)
    if distance > abs(cir1_r + cir2_r) :
        return False
    return True

def checkContainsPoint(point_x,point_y):
    global target_index
    index_cir = 0
    for circle in allcircle_list :
        circle_x = circle[0]
        circle_y = circle[1]
        circle_r = circle[2]
        if (point_x - circle_x)**2 + (point_y - circle_y)**2 <= (circle_r)**2:
            target_index = index_cir
            return True
            
        index_cir += 1
    return False
def checkBigCircle(circle_check):
    for i in range (len(allcircle_list)):
        if i == circle_check : 
            continue

        r_check = allcircle_list[circle_check][2]
        r_all =  allcircle_list[i][2]

        if r_all > r_check:
            return False

    return True


pygame.init()

pygame.display.set_caption('Assignment1') 

clock = pygame.time.Clock()
scr_w, scr_h = 800, 600
screen  = pygame.display.set_mode((scr_w, scr_h))
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

running = True

circle_amount = 10
counting =0
while running:
    
        # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if(checkContainsPoint(event.pos[0],event.pos[1]) == True):
                x = allcircle_list[target_index][0]
                y = allcircle_list[target_index][1]
                r = allcircle_list[target_index][2]
                
                if checkBigCircle(target_index) == True:
                    color = (255,255,255)
                    x = allcircle_list[target_index][0]
                    y = allcircle_list[target_index][1]
                    r = allcircle_list[target_index][2]
        
                    del allcircle_list[target_index]
                   
                    pygame.draw.circle( surface, color, (x,y), r )
                   
                    

    if counting < circle_amount:
        counting +=1

     
        clock.tick( 10 ) 
 
        red = randint(100,255)
        green = randint(100,255)
        blue = randint(100,255)   
        color = (red,green,blue)

        r = randint(10,20)
        x,y = randint(r,scr_w-r), randint(r,scr_h-r)
        circle_attr = [x,y,r]
        
       

        

        if(len(allcircle_list) == 0):
            allcircle_list.append(circle_attr)
            pygame.draw.circle( surface, color, (x,y), r )
        else :
            Overlap = True
            while (Overlap):
                counter_loop = 0
                for another_cir in allcircle_list:
                    counter_loop +=1
                    x_new = circle_attr[0]
                    y_new = circle_attr[1]
                    r_new = circle_attr[2]
                    x_another = another_cir[0]
                    y_another = another_cir[1]
                    z_another = another_cir[2]

                    if checkOverlap(x_new,y_new,r_new,x_another,y_another,z_another) == True:
                        r = randint(5,40)
                        x,y = randint(r,scr_w-r), randint(r,scr_h-r)
                        circle_attr = [x,y,r]
                        break
                    if counter_loop == len(allcircle_list):
                        Overlap = False
                        allcircle_list.append(circle_attr)
                        pygame.draw.circle( surface, color, (x,y), r )

                
        screen.fill((255,255,255))
        screen.blit(surface, (0,0))
        pygame.display.update()

    screen.fill((255,255,255))
    screen.blit(surface, (0,0))
    pygame.display.update()

pygame.quit()

