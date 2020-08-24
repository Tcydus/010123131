
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

        self.string = string
        self.stack = self.Stack()
        self.precedence = {'!':3, '&':2, '+':1} 
        self.posfix_list = []
        self.preorder_list = []
        self.inorder_list = []
        self.postorder_list = []
       
        self.expression_tree = None
        
        
        
    

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
        
   
 
            

    def inOrderTraversal(self):
        self.inOrder(self.expression_tree)
        print()
    def postOrderTraversal(self):
        self.postOrder(self.expression_tree)
        print()



if __name__ == "__main__":
    expression = ['!(1+1)', '!(!(0+I0&1))', '(I0+!I1+!(I2))&(!I0+I1+I2)', '!(I0&I1)+!(I1+I2)', '(((I0&I1&!I2)+!I1)+I3)']


# for string in expression:
    string = expression[0]

    bool_express = Tree(string)

    bool_express.infixToPostfix()
    bool_express.postfixToExpressionTree()

   
    print("\noutcame")
    print() 
    




        