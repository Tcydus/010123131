import pygame
from pygame.locals import *
from circle_pygame import Circle
from line_pygame import Line

class DrawTree():
    def __init__(self,tree_node):
        self.screen = None
        self.width = None
        self.height = None
        self.tree_node = tree_node
    
        self.zoom = None
        self.fontsize = None
        self.font = None
        self.line_linewidth = None
        self.circle_linewidth = None

        self.TEXT_COLOR = (0,0,255) 
        self.CIRCLE_COLOR = (0,0,255)
        self.LINE_COLOR = (0,0,255)
        self.BASE_MULTIPLE = 2
        self.ADD_EXPONENT_MULTIPLE = 2
        self.LINE_LENGHT = 10
        self.R_NODE = 35
       
        
        self.zoom = 1
        self.set_scale(self.zoom)

        


    def set_pygame_screen(self,width,height,screen_obj):
        self.width = width
        self.height = height
        self.screen = screen_obj
        
    def set_scale(self,zoom):
        self.zoom = zoom
        self.fontsize = int(32 * self.zoom)
        self.font = pygame.font.Font('freesansbold.ttf', self.fontsize)
        self.line_linewidth = int(5 * self.zoom)
        self.circle_linewidth = int(5 * self.zoom)
    
    
    def set_tree(self,tree_node):
        self.tree_node = tree_node


    def draw_lr(self,text,position,circle,multiple):

        if position == 'left':
            line_theta = 135
        elif position == 'right':
            line_theta = 45

        line = Line(r = self.LINE_LENGHT, theta = line_theta, linewidth = self.line_linewidth,zoom = self.zoom,color = self.LINE_COLOR)
        
        line.drawLineOnCircle(self.screen,circle,multiple,const_y_stop=100)

        circle2 = Circle(r = self.R_NODE,linewidth = self.circle_linewidth,zoom = self.zoom,color =self.CIRCLE_COLOR)
        circle2.drawCircleOnLine(self.screen,line)

        self.draw_text(text,circle2.x,circle2.y)
        return circle2

    def recursive_draw(self,multiple,node,position = 'root',circle = None): 

        if type(node) == str :

            text = node
            self.draw_lr(text,position,circle,multiple)

  
        elif node: 


            text = node.root
            if position == 'root' :

                x = self.width//2
                y = int(0.1 * self.height)

                circle = Circle(x,y, self.R_NODE,self.circle_linewidth,self.CIRCLE_COLOR,self.zoom)
                circle.drawCircle(self.screen)
                self.draw_text(text,x,y)
        
                self.recursive_draw(multiple//2 ,node.left,'left',circle) 
                self.recursive_draw(multiple//2 ,node.right,'right',circle) 
            
            else :
                
                circle2 = self.draw_lr(text,position,circle,multiple)

                self.recursive_draw(multiple//2 ,node.left,'left',circle2) 
                self.recursive_draw(multiple//2 ,node.right,'right',circle2) 
    
    def draw(self):
        depth  = self.max_depth(self.tree_node)
        multiple = pow(self.BASE_MULTIPLE, depth+self.ADD_EXPONENT_MULTIPLE  ) 
        
        self.recursive_draw(multiple,self.tree_node)

    def max_depth(self,node): 
        if node is None : 
            return 0 
        elif type (node) == str :
            return 1
        else : 
            l_depth = self.max_depth(node.left) 
            r_depth = self.max_depth(node.right) 
    
            if (l_depth > r_depth): 
                return l_depth+1
            else: 
                return r_depth+1
    
    def draw_text(self,text,x,y):
        text_surface = self.font.render(text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)



if __name__ == "__main__":
    Tree = DrawTree()
    Tree.pygame_screen = (1020,720)