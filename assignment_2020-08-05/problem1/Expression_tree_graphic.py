
'''
Can display expression tree only tree depth <= 4 
'''

import pygame
from pygame.locals import *
import sys
import math 

pygame.init()

# scr_w, scr_h = 1280,720
scr_w, scr_h = 1400,1000
screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption('Assignment 1') 

surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

zoom = 0.6

is_running = True
GREEN = (0,255,0)
WHITE = (255,255,255)


class Circle:
    def __init__(self,x =0,y = 0,r =0,linewidth = 0,zoom  = 1):
        self.x = x
        self.y = y

        self.zoom = zoom
        self.r = int(r *zoom)

        self.linewidth  = linewidth
    
    def drawCircle(self):
        pygame.draw.circle( screen, GREEN, (self.x,self.y), self.r,self.linewidth )

    def drawCircleOnLine(self,line):
        self.x += int(line.x_stop + self.r*math.cos(math.radians(line.theta)))
        self.y += int(line.y_stop + self.r*math.sin(math.radians(line.theta)))
        self.drawCircle()


class Line():
    def __init__(self,x_start = 0,y_start =0,r = 0,theta = 0,linewidth = 0,zoom = 1):
        self.x_start = x_start
        self.y_start = y_start
        self.r = r
        self.theta = theta

        self.zoom = zoom
        
        self.x_stop = x_start + int(r * math.cos(math.radians(theta)) )
        self.y_stop = y_start + int(r * math.sin(math.radians(theta)) )
        self.linewidth  = linewidth
        

    def drawLine(self):
        pygame.draw.line(screen, GREEN, (self.x_start, self.y_start),(self.x_stop,self.y_stop), self.linewidth )
    
    def drawLineOnCircle(self,circle,multiple,const_x_stop = 0,const_y_stop = 0):
        self.x_start = circle.x + int(circle.r * math.cos(math.radians(self.theta)) )
        self.y_start = circle.y + int(circle.r * math.sin(math.radians(self.theta)) )
        self.x_stop = self.x_start + (int(multiple*self.r * math.cos(math.radians(self.theta)) )  + const_x_stop) *self.zoom
        self.y_stop = self.y_start + (int(self.r * math.sin(math.radians(self.theta)) )           + const_y_stop) *self.zoom 
        self.drawLine()
        


class Tree:

    class Stack:
        def __init__(self):
            self.items = []

        def isEmpty(self):
            return self.items == []

        def push(self, item):
            self.items.append(item)

        def pop(self):
            return self.items.pop()

        def peek(self):
            return self.items[-1]

        def size(self):
            return len(self.items)

    
    class Node:

        def __init__(self, root):
            self.left = None
            self.right = None
            self.root = root


    def __init__(self,string):
        self.string = string
        self.stack = self.Stack()
        self.precedence = {'!':3, '&':2, '+':1} 
        self.posfix_list = []
        self.preorder_list = []
        self.zoom = 1
        self.fontsize = 32 * self.zoom
        self.font = pygame.font.Font('freesansbold.ttf', self.fontsize)
        self.r_node = 35
        self.line_lenght = 10
        self.line_linewidth =5
        self.circle_linewidth = 5
        self.expression_tree = None
        
    
    def setZoom(self,zoom):
        self.zoom = zoom
        self.fontsize = int(32 * self.zoom)
        self.font = pygame.font.Font('freesansbold.ttf', self.fontsize)
        self.line_linewidth = int(5*zoom)
        self.circle_linewidth = int(5*zoom)
    

    def isOperator(self, c):
        return (c == '&') or (c == '+') or (c == '!')
    
    def isOperand(self, c): 
        if len(c) == 1:
            return c.isalpha() or c.isnumeric() 
        else:
            return not self.isOperator(c)

    


    def isBracket(self,c):
        return (c == '(') or (c == ')')
        
    def lessThan(self, i): 
        try: 
            a = self.precedence[i] 
            b = self.precedence[self.stack.peek()] 
            # return a  <= b 
            return a < b
        except KeyError:  
            return False
    
    def lenNode(self):
            return len(self.posfix_list) 
    
    def infixToPostfix(self):    

        operant_char = ''
        len_var = 0
        check_len = True
        i,j = 0,0

        for c in self.string :

            if c == ' ':
                continue

            elif self.isOperand(c): 
                
                operant_char += c
                
                if check_len :
                    len_var += 1
                
              
            elif c  == '(': 
                self.stack.push(c) 

            elif c == ')': 
                while( (not self.stack.isEmpty()) and self.stack.peek() != '('): 
                    op = self.stack.pop()

                    if op == '!' and (self.stack.isEmpty() or self.stack.peek() == '!') :   
                        check_len == True
                        self.posfix_list.append(operant_char) 
                        operant_char = ''

                    self.posfix_list.append(op) 

                if  ((not self.stack.isEmpty()) and self.stack.peek() != '('): 
                    return -1
                else: 
                    self.stack.pop() 
            else: 
                if c != '!':
                    check_len = False


                while(not self.stack.isEmpty() and self.lessThan(c)): 
                    op = self.stack.pop()

                    if op == '!' and (self.stack.isEmpty() or self.stack.peek() in '!(') :   
                        check_len == True
                        self.posfix_list.append(operant_char) 
                        operant_char = ''

                    self.posfix_list.append(op) 

                    while not self.stack.isEmpty() and self.stack.peek() == '!' :
                         self.posfix_list.append(self.stack.pop())
                  


                    

                self.stack.push(c) 
            
            if len(operant_char) == len_var and check_len == False and operant_char != '':

                check_len == True
                self.posfix_list.append(operant_char) 
                operant_char = ''


        
        while not self.stack.isEmpty(): 
            self.posfix_list.append(self.stack.pop()) 
  
        print ("".join(self.posfix_list))
    
    def drawText(self,text,x,y):
        text_surface = self.font.render(text, True, GREEN)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)


    def checkLRAndDraw(self,text,position,circle,multiple):

        if position == 'left':
            line_theta = 135
        elif position == 'right':
            line_theta = 45

        line = Line(r = self.line_lenght, theta = line_theta, linewidth = self.line_linewidth,zoom = self.zoom)
        line.drawLineOnCircle(circle,multiple,const_y_stop=100)

        circle2 = Circle(r = self.r_node,linewidth = self.circle_linewidth,zoom = self.zoom)
        circle2.drawCircleOnLine(line)

        self.drawText(text,circle2.x,circle2.y)
        return circle2

    def drawTree(self,multiple,node,position = 'root',circle = None): 

        if type(node) == str :
            self.preorder_list.append(node)
            text = node
            self.checkLRAndDraw(text,position,circle,multiple)

  
        elif node: 

            self.preorder_list.append(node.root)
            text = node.root
            if position == 'root' :

                x = scr_w//2
                y = int(0.1 * scr_h)

                circle = Circle(x,y, self.r_node,self.circle_linewidth,self.zoom)
                circle.drawCircle()
                self.drawText(text,x,y)
        
                self.drawTree(multiple//2 ,node.left,'left',circle) 
                self.drawTree(multiple//2 ,node.right,'right',circle) 
            
            else :
                
                circle2 = self.checkLRAndDraw(text,position,circle,multiple)

                self.drawTree(multiple//2 ,node.left,'left',circle2) 
                self.drawTree(multiple//2 ,node.right,'right',circle2) 
   



               
    
    def postfixToExpressionTree(self):
        for c in self.posfix_list:
            
            if self.isOperand(c): 
                self.stack.push(c)
            
            elif c == '!' :
                a = self.stack.pop()
                node = self.Node(c)
                node.left = a
                self.stack.push(node)

            elif self.isOperator(c):
                a = self.stack.pop()
                b = self.stack.pop()
                node = self.Node(c)
                node.left = a
                node.right = b
                self.stack.push(node)

        self.expression_tree  = self.stack.pop()
        return self.expression_tree

    def drawExpressionTree(self):
        depth  = self.maxDepth(self.expression_tree)
        multiple = pow(2.3, depth +2 ) 
        
        self.drawTree(multiple,self.expression_tree)

    def maxDepth(self,node): 
        if node is None : 
            return 0 
        elif type (node) == str :
            return 1
        else : 
            l_depth = self.maxDepth(node.left) 
            r_depth = self.maxDepth(node.right) 
    
            if (l_depth > r_depth): 
                return l_depth+1
            else: 
                return r_depth+1
        
           
    
    

expression = ['A+!A + B & A',\
            '(!I0&I1 + !I2 & I3)',\
            '((I2+I3)& (I1+I0) + !(I1&I2))',\
            '!!I0+!!I1 ',\
            '!I0+I1+I2'
            ]


expression_index = 4





first_time = True

while is_running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
            
        if e.type == pygame.MOUSEBUTTONDOWN:
            scroll_up = 4
            scroll_down = 5
            if e.button == scroll_up:
                
                zoom += 0.05

            elif e.button == scroll_down:
                
                if zoom <= 0.2:
                    zoom = 0.2
                else:
                    zoom -= 0.05

            zoom = round(zoom,2)
        
           
    
    if first_time :
        first_time = False
       
        bool_express = Tree(expression[expression_index])
        bool_express.infixToPostfix()

        bool_express.postfixToExpressionTree()
        
    screen.fill(WHITE)
    bool_express.setZoom(zoom)
    bool_express.drawExpressionTree()

        
    pygame.display.flip()


print('Done....')
