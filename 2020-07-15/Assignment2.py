import math
import pygame 
from random import randint
from random import random
import sys

scr_w,scr_h = 800,600
circle_amount = 10
circle_minsize,circle_maxsize = 22,30
circle_index = 0
running = True

class MyCircle:
    def __init__(self,x = 0,y = 0,r = 0,color = [0,0,0],x_move = 0,y_move = 0):
        self.__x = x
        self.__y = y
        self.__r = r
        self.__mass = r * 10.0 
        self.__color = color
        self.__x_move = x_move
        self.__y_move = y_move

    def getX(self):
        return self.__x
    def getY(self):
        return self.__y
    def getR(self):
        return self.__r
    def getXMove(self):
        return self.__x_move
    def getYMove(self):
        return self.__y_move
    def getColor(self):
        return self.__color 
    
    def setX(self,x):
        self.__x = x   
    def setY(self,y):
        self.__y = y    
    def setR(self,r):
        self.__r = r   
    def setXMove(self,x_move):
        self.__x_move = x_move
    def setYMove(self,y_move):
        self.__y_move = y_move          
    def setColor(self):
        self.__color = color
        
    def getDistance(self,circle2):
        return math.sqrt((self.__x - circle2.__x)**2 + (self.__y - circle2.__y)**2 )

    def checkOverlap(self,circle2):
        distance = self.getDistance(circle2)
        if distance > abs(self.__r + circle2.__r) :
            return False
        return True

    def checkContainsPoint(self,point_x,point_y):
        if (point_x - self.__x)**2 + (point_y - self.__y)**2 <= (self.__r)**2:
            return True            
        return False

    def collusionScreenTop(self,screen_hight):
        if self.__y + self.__r  >= screen_hight  :
            return True
        return False

    def collusionScreenBottom(self):
        if self.__y - self.__r <= 0 :
            return True
        return False

    def collusionScreenRight(self,screen_width):
        if self.__x + self.__r  >= screen_width  :
            return True
        return False

    def collusionScreenLeft(self):
        if self.__x - self.__r <= 0 :
            return True
        return False

    #
    def collusionAnotherCircle(self,circle2):
        distance = self.getDistance(circle2)
        x_diff = self.__x - circle2.__x
        y_diff = self.__y - circle2.__y
        x_move,y_move = 0,0

        if x_diff < 0:
            if y_diff < 0:
                angle  = math.atan(y_diff / x_diff)
                x_move = -distance * math.cos(angle)
                y_move = -distance * math.sin(angle)
            elif y_diff > 0:
                angle  = math.atan(y_diff / x_diff)
                x_move = -distance * math.cos(angle)
                y_move = -distance * math.sin(angle)
        elif x_diff > 0:
            if y_diff < 0:
                angle  =  math.radians(180) + math.atan(y_diff / x_diff)
                x_move = -distance * math.cos(angle)
                y_move = -distance * math.sin(angle)
            elif y_diff > 0:
                angle  =  math.radians(-180) + math.atan(y_diff / x_diff)
                x_move = -distance * math.cos(angle)
                y_move = -distance * math.sin(angle)
        elif x_diff == 0:
            if y_diff < 0:
                angle = math.radians(-90)
            else:
                angle = math.radians(90)
            x_move = distance * math.cos(angle)
            y_move = distance * math.sin(angle)
        elif y_diff == 0:
            if x_diff > 0:
                angle = math.radians(0)
            else:
                angle = math.radians(180)
            x_move = distance * math.cos(angle)
            y_move = distance * math.sin(angle)
        
        self.__x_move = x_move
        self.__y_move = y_move

            



        

    # def collusionAnotherCircle(self,circle2):
    #     distance = self.getDistance(circle2)
    #     overlap_dist = ((distance - self.__r - circle2.__r) / 2)
    #     # print(distance,overlap_dist)

    #     # theta_2 = math.atan(circle2.__y/circle2.__x)
    #     # theta_1 = math.atan(self.__y/self.__x)
    #     # print(math.degrees(theta_1),math.degrees(theta_2))


    #     normal_x = (circle2.__x - self.__x)/ distance
    #     normal_y = (circle2.__y - self.__y)/ distance

    #     tangent_x = normal_x
    #     tangent_y = -normal_y

    #     dot_tangent_self    =  self.__x_move * tangent_x + self.__y_move * tangent_y
    #     dot_tangent_circle2 =  circle2.__x_move * tangent_x + circle2.__y_move * tangent_y

    #     dot_normal_self     =  self.__x_move * normal_x + self.__y_move * normal_y
    #     dot_normal_circle2  =  circle2.__x_move * normal_x + circle2.__y_move * normal_y

    #     momentum_self = (dot_normal_self * (self.__mass - circle2.__mass) + 2.0 * dot_normal_circle2 * circle2.__mass) / (self.__mass + circle2.__mass) 
    #     momentum_circle2 = (dot_normal_circle2 * (circle2.__mass - self.__mass) + 2.0 * dot_normal_self * self.__mass) / (self.__mass + circle2.__mass) 
   
        
    #     self.__x_move =  int(tangent_x * dot_tangent_self + normal_x * momentum_self)
    #     self.__y_move =  int(tangent_y * dot_tangent_self + normal_y * momentum_self)
    #     circle2.__x_move =  int(tangent_x * dot_tangent_circle2 + normal_x * momentum_circle2)
    #     circle2.__y_move =  int(tangent_y * dot_tangent_circle2 + normal_y * momentum_circle2)

    #     self.__x_move =  int(tangent_x * dot_tangent_self )
    #     self.__y_move =  int(tangent_y * dot_tangent_self )
    #     circle2.__x_move =  int(tangent_x * dot_tangent_circle2 )
    #     circle2.__y_move =  int(tangent_y * dot_tangent_circle2)

        


    #     self.__x -= int((overlap_dist/distance) * (self.__x - circle2.__x))
    #     self.__y -= int((overlap_dist/distance) * (self.__y - circle2.__y))
    #     circle2.__x += int((overlap_dist/distance) * (self.__x - circle2.__x))
    #     circle2.__y += int((overlap_dist/distance) * (self.__y - circle2.__y))
        

    def updatePosition(self,screen_width,screen_hight):
        self.__x += self.__x_move
        self.__y += self.__y_move

        if self.collusionScreenRight(screen_width):
            self.__x = screen_width - self.__r
            self.__x_move *=-1
           
        if self.collusionScreenLeft():
            self.__x = 0 + self.__r
            self.__x_move *=-1
       
        if self.collusionScreenTop(screen_hight):
            self.__y = screen_hight - self.__r
            self.__y_move *=-1

        if self.collusionScreenBottom():
            self.__y = 0 + self.__r   
            self.__y_move *=-1  

    



    def __str__(self):
        return "Pos x :"+" "+ str(self.__x) + "\tPos y :"+" "+ str(self.__y) + "\tRadius :"+" "+ str(self.__r)+ "\tColor : " + str(self.__color)+ "\t\tDirection : ("+ str(self.__x_move) + "," + str(self.__y_move) +")"


## https://www.w3resource.com/python-exercises/data-structures-and-algorithms/python-search-and-sorting-exercise-6.php#:~:text=Write%20a%20Python%20program%20to,one%20item%20at%20a%20time.
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
        # x_move,y_move = 0,0
        # while (x_move == 0) or (y_move == 0):
        #     x_move = randint(-20,20)
        #     y_move  = randint(-20,20) 
        x_move = 0.5*(random()+1.0)
        y_move = 0.5*(random()+1.0)

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
                print(x_cursor,y_cursor)
                color = (255,255,255)
                x = int(circle.getX())
                y = int(circle.getY())
                r = circle.getR()

                del circle_objlist[-1]
                print("\n#################################################  Sorting  #################################################")
                print(len(circle_objlist),sep = '\n')
            
                pygame.draw.circle( surface, color, (x,y), r )


def updateCircle():
    pass




pygame.init()

pygame.display.set_caption('Assignment1') 

clock = pygame.time.Clock()
screen  = pygame.display.set_mode((scr_w, scr_h))
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )


circle_objlist = createCircle(circle_amount)   
print("\n#################################################  Sorting  #################################################")
print(*circle_objlist,sep = '\n')
print("#############################################################################################################\n")
drawAllCircle()


def stopAnimate():
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN :
                delBiggestCircle()


while running:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN :
            delBiggestCircle()

    for i in range (len(circle_objlist)):

        draw_circle = circle_objlist[i]
   
        delCircle(draw_circle)
        
        draw_circle.updatePosition(scr_w,scr_h)

        for another_circle in circle_objlist:
            if another_circle == draw_circle : 
                continue 

            if draw_circle.checkOverlap(another_circle) == True:
                delCircle(another_circle)
                delCircle(draw_circle)

                draw_circle.collusionAnotherCircle(another_circle)

                drawCircle(another_circle)
                drawCircle(draw_circle)  

        color = draw_circle.getColor()
        x = int(draw_circle.getX())
        y = int(draw_circle.getY())
        r =draw_circle.getR()
    
        pygame.draw.circle( surface, color, (x,y), r ) 
  

    screen.fill((255,255,255))
    screen.blit(surface, (0,0))
    pygame.display.flip()

pygame.quit()





#print(c1.checkOverlap(c2))