
import pygame
from pygame.locals import *
import math

class Circle:
    def __init__(self, x = 0, y = 0, r = 0, linewidth = 0, color = (0,0,0) , zoom  = 1 ):
        self.x = x
        self.y = y
        self.color = color

        self.zoom = zoom
        self.r = int(r *zoom)

        self.linewidth  = linewidth
    
    def drawCircle(self,screen):
 
        pygame.draw.circle( screen, self.color, (self.x,self.y), self.r,self.linewidth )

        # pygame.draw.circle( screen, self.color, (self.x,self.y), self.r,self.linewidth )

    def drawCircleOnLine(self,screen,line):
        self.x += int(line.x_stop + self.r*math.cos(math.radians(line.theta)))
        self.y += int(line.y_stop + self.r*math.sin(math.radians(line.theta)))
        self.drawCircle(screen)



if __name__=="__main__":
    print('Test debugging')
