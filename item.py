import pygame

class Item:
    def __init__(self,screen,tilesize,color):
        self.screen = screen
        self.tile = tilesize
        self.color = color


    def pos_item(self,x,y,screen,tilesize,color):
        pygame.draw.polygon(screen,color,[((x-0.5)*tilesize,(y-1)*tilesize),((x-1)*tilesize,y*tilesize),((x)*tilesize,y*tilesize)],2)
