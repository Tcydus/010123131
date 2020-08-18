

from Circle_pygame import Circle
from Line_pygame import Line

import pygame
from pygame.locals import *


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
        self.caltree = None
        self.string = string
        self.stack = self.Stack()
        self.precedence = {'!':3, '&':2, '+':1} 
        self.posfix_list = []
        self.preorder_list = []
        self.inorder_list = []
        self.postorder_list = []
        self.zoom = 1
        self.fontsize = 32 * self.zoom
        # self.font = pygame.font.Font('freesansbold.ttf', self.fontsize)
        self.r_node = 35
        self.line_lenght = 10
        self.line_linewidth = 5
        self.circle_linewidth = 5
        self.text_color = (0,0,255)
        self.circle_color = (0,0,255)
        self.line_color = (0,0,255)
        self.base_multiple = 2
        self.add_exponent_multiple = 2
        self.expression_tree = None
        self.screen = None
        self.scr_w = None
        self.scr_h = None
        
        
    def setPygameScreen(self,scr_w, scr_h,screen):
        self.scr_w = scr_w
        self.scr_h = scr_h
        self.screen = screen
    
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

                    # if op == '!' and (self.stack.isEmpty() or self.stack.peek() == '!') or (c == self.string[-1]  and operant_char != ''):   
                    if c == self.string[-1] and operant_char != '':
                        check_len = True
                        self.posfix_list.append(operant_char) 
                        operant_char = ''

                    self.posfix_list.append(op) 

                if  ((not self.stack.isEmpty()) and self.stack.peek() != '('): 
                    return -1
                else: 
                    self.stack.pop() 
            else: 
                if c != '!' and operant_char != '' :
                    check_len = False


                while(not self.stack.isEmpty() and self.lessThan(c)): 
                    op = self.stack.pop()

                    if op == '!' and operant_char != '' :   
                        check_len = True
                        len_var = 0
                        self.posfix_list.append(operant_char) 
                        operant_char = ''

                    self.posfix_list.append(op) 

                    while not self.stack.isEmpty() and self.stack.peek() == '!' :
                         self.posfix_list.append(self.stack.pop())
                     

                self.stack.push(c) 
            
            if  (check_len == False  or c == self.string[-1]) and operant_char != '' :
                check_len = True
                len_var = 0
                self.posfix_list.append(operant_char) 
                operant_char = ''


        
        while not self.stack.isEmpty(): 
            self.posfix_list.append(self.stack.pop()) 

        #print(self.posfix_list)
  
  
       
    def drawText(self,text,x,y):
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


    def checkLRAndDraw(self,text,position,circle,multiple):

        if position == 'left':
            line_theta = 135
        elif position == 'right':
            line_theta = 45

        line = Line(r = self.line_lenght, theta = line_theta, linewidth = self.line_linewidth,zoom = self.zoom,color = self.line_color)
        
        line.drawLineOnCircle(self.screen,circle,multiple,const_y_stop=100)

        circle2 = Circle(r = self.r_node,linewidth = self.circle_linewidth,zoom = self.zoom,color =self.circle_color)
        circle2.drawCircleOnLine(self.screen,line)

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

                x = self.scr_w//2
                y = int(0.1 * self.scr_h)

                circle = Circle(x,y, self.r_node,self.circle_linewidth,self.circle_color,self.zoom)
                circle.drawCircle(self.screen)
                self.drawText(text,x,y)
        
                self.drawTree(multiple//2 ,node.left,'left',circle) 
                self.drawTree(multiple//2 ,node.right,'right',circle) 
            
            else :
                
                circle2 = self.checkLRAndDraw(text,position,circle,multiple)

                self.drawTree(multiple//2 ,node.left,'left',circle2) 
                self.drawTree(multiple//2 ,node.right,'right',circle2) 
   


               
    
    def postfixToExpressionTree(self):
      
        for c in self.posfix_list:

            if c == '':
                continue
            
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
                node.left = b
                node.right = a
                self.stack.push(node)

        self.expression_tree  = self.stack.pop()
        return self.expression_tree

    def drawExpressionTree(self):
        depth  = self.maxDepth(self.expression_tree)
        multiple = pow(self.base_multiple, depth+self.add_exponent_multiple  ) 
        
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
    def inOrder(self,node):
        if type(node) == str :
            print(node,end = " ")
            self.preorder_list.append(node)
                    
  
        else: 
            if node.left :
                self.inOrder(node.left) 
            
            self.preorder_list.append(node.root)
            print(node.root,end = " ")
           
            if node.right:
                self.inOrder(node.right)  

    def postOrder(self,node):
        if type(node) == str :
            print(node,end = " ")
            self.preorder_list.append(node)
                    
  
        else: 
            if node.left :
                self.postOrder(node.left) 
            
            if node.right:
                self.postOrder(node.right) 

            self.preorder_list.append(node.root)
            print(node.root,end = " ")   
        
   

    



                    
    def notBitwise(self,input):
        if input == 0:
            return 1
        else:
            return 0
            
            
            

    def inOrderTraversal(self):
        self.inOrder(self.expression_tree)
        print()
    def postOrderTraversal(self):
        self.postOrder(self.expression_tree)
        print()

    def calculate(self):
        self.caltree = self.expression_tree
        # self.showAllEquation()
        self.calculateRecursive(self.caltree)


if __name__ == "__main__":
    expression = ['!(1+1)', '!(!(0+I0&1))', '(I0+!I1+!(I2))&(!I0+I1+I2)', '!(I0&I1)+!(I1+I2)', '(((I0&I1&!I2)+!I1)+I3)']


# for string in expression:
    string = expression[0]

    bool_express = Tree(string)

    bool_express.infixToPostfix()
    bool_express.postfixToExpressionTree()

   
    print("\noutcame")
    print() 
    




        
