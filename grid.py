import pygame

class Grid:
    def __init__(self, x,y, tilesize):
        self.x = x
        self.y = y
        self.tilesize = tilesize

    def draw(self, screen, color):
        for i in range(1,self.x):
            pygame.draw.line(screen,color, (self.tilesize*i, 0), (self.tilesize*i, self.tilesize*self.x) )
        for i in range(0,self.y):
            pygame.draw.line(screen, color, (0, self.tilesize*i), (self.tilesize*self.x, self.tilesize*i) )