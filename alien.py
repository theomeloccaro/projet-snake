import pygame

class Alien:
    def __init__(self,screen,tilesize,color,x,y,largeur):
        self.screen=screen
        self.tilesize=tilesize
        self.color= color
        self.x=x
        self.y=y
        self.largeur=largeur

    def pos_alien(self):
        pygame.draw.circle(self.screen,self.color,((self.x+0.5)*self.tilesize,(self.y+0.5)*self.tilesize),self.tilesize/2,self.largeur)

    
