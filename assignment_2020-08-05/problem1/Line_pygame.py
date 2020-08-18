
import pygame
from pygame.locals import *
import math

class Line():
    def __init__(self,x_start = 0,y_start =0,r = 0,theta = 0,linewidth = 0,color = (0,0,0),zoom = 1):
        self.x_start = x_start
        self.y_start = y_start
        self.r = r
        self.theta = theta

        self.color = color

        self.zoom = zoom
        
        self.x_stop = x_start + int(r * math.cos(math.radians(theta)) )
        self.y_stop = y_start + int(r * math.sin(math.radians(theta)) )
        self.linewidth  = linewidth
        

    def drawLine(self,screen):
        pygame.draw.line(screen, self.color , (self.x_start, self.y_start),(self.x_stop,self.y_stop), self.linewidth )

        # pygame.draw.line(screen, self.color , (self.x_start, self.y_start),(self.x_stop,self.y_stop), self.linewidth )
    
    def drawLineOnCircle(self,screen,circle,multiple,const_x_stop = 0,const_y_stop = 0):
        self.x_start = circle.x + int(circle.r * math.cos(math.radians(self.theta)) )
        self.y_start = circle.y + int(circle.r * math.sin(math.radians(self.theta)) )
        self.x_stop = self.x_start + (int(multiple*self.r * math.cos(math.radians(self.theta)) )  + const_x_stop) *self.zoom
        self.y_stop = self.y_start + (int(self.r * math.sin(math.radians(self.theta)) )           + const_y_stop) *self.zoom 
        self.drawLine(screen)
        