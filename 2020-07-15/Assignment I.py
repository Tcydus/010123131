import math
import pygame 
from random import randint

scr_w,scr_h = 800,600
circle_amount = 2
circle_minsize,circle_maxsize = 22,30
circle_index = 0
running = True

class MyCircle:
    def __init__(self,x = 0,y = 0,r = 0,color = [0,0,0],x_move = 0,y_move = 0):
        self.__x = x
        self.__y = y
        self.__r = r
        self.__color = color
        self.__x_move = x_move
        self.__y_move = y_move

    def getX(self):
        return self.__x
    def getY(self):
        return self.__y
    def getR(self):
        return self.__r
    def getColor(self):
        return self.__color

    def checkOverlap(self,circle2):
        distance = math.sqrt((self.__x - circle2.__x)**2 + (self.__y - circle2.__y)**2 )
        if distance > abs(self.__r + circle2.__r) :
            return False
        return True

    def checkContainsPoint(self,point_x,point_y):
        if (point_x - self.__x)**2 + (point_y - self.__y)**2 <= (self.__r)**2:
            return True            
        return False

    def updatePosition(self):
        self.__x += self.__x_move
        self.__y += self.__y_move
        if self.collusionFrame():
            pass

    def collusionFrame(self,scr_w,scr_h):
        if (self.__x + self.__r >= scr_w) or (self.__y + self.__r >= scr_h):
            return True



    def __str__(self):
        return "Pos x :"+" "+ str(self.__x) + "\tPos y :"+" "+ str(self.__y) + "\tRadius :"+" "+ str(self.__r)+ "\tColor : " + str(self.__color)+ "\tDirection : ("+ str(self.__x_move) + "," + str(self.__y_move) +")"


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
        x_move = randint(-20,20)
        y_move  = randint(-20,20)


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

def drawCircle():
    for i in range (circle_amount):
        draw_circle = circle_objlist[i]
        color = draw_circle.getColor()
        x = draw_circle.getX()
        y = draw_circle.getY()
        r =draw_circle.getR()
    
        pygame.draw.circle( surface, color, (x,y), r )

def delBiggestCircle():
    for circle in circle_objlist:
        x_cursor,y_cursor = event.pos[0],event.pos[1]
        if  circle.checkContainsPoint(x_cursor,y_cursor) == True :
            if circle == circle_objlist[-1]:
                print(x_cursor,y_cursor)
                color = (255,255,255)
                x = circle.getX()
                y = circle.getY()
                r = circle.getR()

                del circle_objlist[-1]
                print("\n#################################################  Sorting  #################################################")
                print(len(circle_objlist),sep = '\n')
            
                pygame.draw.circle( surface, color, (x,y), r )







pygame.init()

pygame.display.set_caption('Assignment1') 

clock = pygame.time.Clock()
screen  = pygame.display.set_mode((scr_w, scr_h))
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )


circle_objlist = createCircle(circle_amount)   
print("\n#################################################  Sorting  #################################################")
print(*circle_objlist,sep = '\n')
drawCircle()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN :
            delBiggestCircle()

           

    screen.fill((255,255,255))
    screen.blit(surface, (0,0))
    pygame.display.flip()

pygame.quit()
