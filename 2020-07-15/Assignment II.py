import math
import pygame 
from random import randint
from random import random
import sys

scr_w,scr_h = 800,600
circle_amount = 10
circle_minsize,circle_maxsize = 10,20
circle_index = 0
running = True


class MyCircle:
    def __init__(self,x = 0,y = 0,r = 0,color = [0,0,0],x_move = 0,y_move = 0):
        self.x = x
        self.y = y
        self.r = r
        self.mass = r * 10.0 
        self.color = color
        self.x_move = x_move
        self.y_move = y_move

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getR(self):
        return self.r
    def getXMove(self):
        return self.x_move
    def getYMove(self):
        return self.y_move
    def getColor(self):
        return self.color 
    
    def setX(self,x):
        self.x = x   
    def setY(self,y):
        self.y = y    
    def setR(self,r):
        self.r = r   
    def setXMove(self,x_move):
        self.x_move = x_move
    def setYMove(self,y_move):
        self.y_move = y_move          
    def setColor(self):
        self.color = color
        
    def getDistance(self,circle2):
        return math.sqrt((self.x - circle2.x)**2 + (self.y - circle2.y)**2 )

    def checkOverlap(self,circle2):
        distance = self.getDistance(circle2)
        if distance > abs(self.r + circle2.r) :
            return False
        return True

    def checkContainsPoint(self,point_x,point_y):
        if (point_x - self.x)**2 + (point_y - self.y)**2 <= (self.r)**2:
            return True            
        return False

    def collusionScreenTop(self,screen_hight):
        if self.y + self.r  >= screen_hight  :
            return True
        return False

    def collusionScreenBottom(self):
        if self.y - self.r <= 0 :
            return True
        return False

    def collusionScreenRight(self,screen_width):
        if self.x + self.r  >= screen_width  :
            return True
        return False

    def collusionScreenLeft(self):
        if self.x - self.r <= 0 :
            return True
        return False

###########################################################

#Reference of collusionAnotherCircle method
## http://www.geometrian.com/programming/projects/index.php?project=Circle%20Collisions

###########################################################
    def collusionAnotherCircle(self,circle2):
        speed =  math.sqrt((self.x_move**2)+(self.y_move**2))
        x_diff = self.x - circle2.x
        y_diff = self.y - circle2.y
        x_move,y_move = 0,0

        if x_diff < 0:
            if y_diff < 0:
                angle  = math.atan(y_diff / x_diff)
                x_move = -speed * math.cos(angle)
                y_move = -speed * math.sin(angle)
            elif y_diff > 0:
                angle  = math.atan(y_diff / x_diff)
                x_move = -speed * math.cos(angle)
                y_move = -speed * math.sin(angle)
        elif x_diff > 0:
            if y_diff < 0:
                angle  =  math.radians(180) + math.atan(y_diff / x_diff)
                x_move = -speed * math.cos(angle)
                y_move = -speed * math.sin(angle)
            elif y_diff > 0:
                angle  =  math.radians(-180) + math.atan(y_diff / x_diff)
                x_move = -speed * math.cos(angle)
                y_move = -speed * math.sin(angle)
        elif x_diff == 0:
            if y_diff < 0:
                angle = math.radians(-90)
            else:
                angle = math.radians(90)
            x_move = speed * math.cos(angle)
            y_move = speed * math.sin(angle)
        elif y_diff == 0:
            if x_diff > 0:
                angle = math.radians(0)
            else:
                angle = math.radians(180)
            x_move = speed * math.cos(angle)
            y_move = speed * math.sin(angle)
        
        self.x_move = x_move
        self.y_move = y_move
            
        

    def updatePosition(self,screen_width,screen_hight):
        self.x += self.x_move
        self.y += self.y_move

        if self.collusionScreenRight(screen_width):
            self.x = screen_width - self.r
            self.x_move *=-1
           
        if self.collusionScreenLeft():
            self.x = 0 + self.r
            self.x_move *=-1
       
        if self.collusionScreenTop(screen_hight):
            self.y = screen_hight - self.r
            self.y_move *=-1

        if self.collusionScreenBottom():
            self.y = 0 + self.r   
            self.y_move *=-1  

    



    def __str__(self):
        return "Pos x :"+" "+ str(self.x) + "\tPos y :"+" "+ str(self.y) + "\tRadius :"+" "+ str(self.r)+ "\tColor : " + str(self.color)+ "\t\tDirection : ("+ str(self.x_move) + "," + str(self.y_move) +")"


###########################################################

#Reference of insertion sort function
## https://www.w3resource.com/python-exercises/data-structures-and-algorithms/python-search-and-sorting-exercise-6.php#:~:text=Write%20a%20Python%20program%20to,one%20item%20at%20a%20time.


###########################################################
def insertionSort(nlist):
   for index in range(1,len(nlist)):

     currentvalue = nlist[index]
     position = index

     while position>0 and nlist[position-1].getR()>currentvalue.getR():
         nlist[position]=nlist[position-1]
         position = position-1

     nlist[position]=currentvalue


def createCircle(amount):
    obj_list = []
    for create_circle in range(amount):
        red = randint(100,255)
        green = randint(100,255)
        blue = randint(100,255)   
        color = (red,green,blue)
        x_move,y_move = 0,0
        while (x_move == 0) or (y_move == 0):
            x_move = randint(-5,5)
            y_move  = randint(-5,5) 


        r = randint(circle_minsize,circle_maxsize)
        x,y = randint(r,scr_w-r), randint(r,scr_h-r)

        new_circle = MyCircle(x,y,r,color,x_move,y_move)

        if len(obj_list) == 0 :
            obj_list.append(new_circle)
        else:
            Overlap = True
            while Overlap:
                for obj in obj_list:
                    if obj.checkOverlap(new_circle):
                        r = randint(circle_minsize,circle_maxsize)
                        x,y = randint(r,scr_w-r), randint(r,scr_h-r)
                        new_circle = MyCircle(x,y,r,color,x_move,y_move)
                        break
                    if obj == obj_list[-1]:       
                        obj_list.append(new_circle)
                        Overlap = False
    insertionSort(obj_list)                    
    return obj_list

def drawAllCircle():
    for i in range (len(circle_objlist)):
        draw_circle = circle_objlist[i]
        color = draw_circle.getColor()
        x = draw_circle.getX()
        y = draw_circle.getY()
        r =draw_circle.getR()
    
        pygame.draw.circle( surface, color, (x,y), r )
    
def drawCircle(circle_obj,color = 'default'):

    if (color == 'default'):
        color = circle_obj.getColor()    
    x = int(circle_obj.getX())
    y = int(circle_obj.getY())
    r = circle_obj.getR()
    pygame.draw.circle( surface, color, (x,y), r ) 

def delCircle(circle_obj):
    drawCircle(circle_obj,(255,255,255)) 



def delBiggestCircle():
    for circle in circle_objlist:
        x_cursor,y_cursor = event.pos[0],event.pos[1]
        if  circle.checkContainsPoint(x_cursor,y_cursor) == True :
            if circle == circle_objlist[-1]:

                color = (255,255,255)
                x = int(circle.getX())
                y = int(circle.getY())
                r = circle.getR()

                del circle_objlist[-1]
                pygame.draw.circle( surface, color, (x,y), r )


pygame.init()

pygame.display.set_caption('Assignment2') 

clock = pygame.time.Clock()
screen  = pygame.display.set_mode((scr_w, scr_h))
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )


circle_objlist = createCircle(circle_amount)   
print("\n#################################################  Sorting  #################################################")
print(*circle_objlist,sep = '\n')
print("#############################################################################################################\n")

drawAllCircle()



while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN :
            delBiggestCircle()

    for circle in circle_objlist:
        delCircle(circle)
    for circle in circle_objlist:
        circle.updatePosition(scr_w,scr_h)
        drawCircle(circle)

    for circle_set1 in circle_objlist:
        for circle_set2 in circle_objlist:
            if circle_set1 == circle_set2 : 
                continue
            if circle_set1.checkOverlap(circle_set2) == True:
                circle_set1.collusionAnotherCircle(circle_set2)

    screen.fill((255,255,255))
    screen.blit(surface, (0,0))
    pygame.display.flip()

pygame.quit()




