# Example file showing a circle moving on screen
import pygame 
import random
from labyrinthe import Labyrinthe
from grid import Grid
from utils import Pos
from IO import InputHandler
from item import Item
from alien import Alien
from chargeur import ConfigLoader
import configparser
import time

# pygame setup
pygame.init()
param={}
loader=ConfigLoader("conf.ini")

param["Version"]=loader.get_value("general","version",int)

param["Auteur"]=loader.get_value("general","author",str)

param["size_x"] = loader.get_value("general", "size_x", int)

param["size_y"] = loader.get_value("general", "size_y", int)

tilesize = loader.get_value("general", "tilesize", int)

level = loader.get_value("map", "level")

array_pos_alien = loader.get_value("aliens", "array_pos_alien",tuple,tuple_delimiter=":",value_delimiter=",")

array_pos_item = loader.get_value("items", "array_pos_item",tuple,tuple_delimiter=":",value_delimiter=",")

ground_color=loader.get_value("color","ground_color",str)
grid_color=loader.get_value("color","grid_color",str)
head_color=loader.get_value("color","head_color",str)
body_color=loader.get_value("color","body_color",str)
wall_color=loader.get_value("color","wall_color",str)
cross_color=loader.get_value("color","cross_color",str)
item_color=loader.get_value("color","item_color",str)
alien_color=loader.get_value("color","alien_color",str)

items = []
aliens = []



#constantes
#tilesize = tile # taille d'une tuile IG
size = (param["size_x"], param["size_y"]) # taille du monde
fps = 30 # fps du jeu
player_speed = 150 # vitesse du joueur
next_move = 0 #tic avant déplacement
filename='color.ini'

laby = Labyrinthe(size[0], size[1])
laby.load_from_file(level)
laby.set_color(wall_color)

grid = Grid(size[0], size[1],tilesize)
grid.set_color(grid_color)

screen = pygame.display.set_mode((size[0]*tilesize, size[1]*tilesize))


clock = pygame.time.Clock() 

running = True
dt = 0
show_grid = True
show_pos = False

direction = "UP"

player_pos=(5,9)
player_pos2=(4,9)
snake=[player_pos,player_pos2]
# Utilisation de la classe dans le programme principal
input_handler = InputHandler()

#création items
for i in range(len(array_pos_item)):
    if not laby.hit_box(array_pos_item[i][0],array_pos_item[i][1]):
        items.append(Item(screen,tilesize,item_color,array_pos_item[i][0],array_pos_item[i][1]))


itemFound = False
DisplayMessage = False

#tour de boucle, pour chaque FPS
while running:    
    #
    #   Gestion des I/O  clavier / souris
    #
    direction, running, show_grid, show_pos = input_handler.event_Polling(direction, running, show_grid, show_pos)
    
    #
    # gestion des déplacements
    #

    next_move += dt
    if next_move>0:
        new_x, new_y = player_pos[0], player_pos[1]
        if direction == 'UP':
            new_y -=1
        elif direction == 'DOWN':
            new_y += 1
        elif direction == 'LEFT':
            new_x -=1
        elif direction == 'RIGHT':
            new_x += 1

        # vérification du déplacement du joueur                                    
        if not laby.hit_box(new_x, new_y):
            player_pos = new_x, new_y
            next_move -= player_speed            

            for j in range (len(array_pos_item)):
                if new_x == array_pos_item[j][0] and new_y == array_pos_item[j][1]:
                    itemFound = True
            
        snake.insert(0,player_pos)

        if len(snake) > 2:
            snake.pop()

        if itemFound :
            snake.insert(0,player_pos)
            itemFound=False

    #
    # affichage des différents composants graphique
    #
    screen.fill(ground_color)

    laby.draw(screen, tilesize)

    if show_grid:
        grid.draw(screen)

        

    for tile in snake:        
        pygame.draw.rect(screen, (0, 255, 0), (tile[0] * tilesize, tile[1] * tilesize, tilesize, tilesize))     
    if show_pos:
        print("pos: ",player_pos)
    
    # test items
    for elt in items:
        elt.pos_item()
    
    #test aliens
    for ali in aliens:
         ali.pos_alien()      
    
    
    # affichage des modification du screen_view
    pygame.display.flip()
    # gestion fps
    dt = clock.tick(fps)

    # Vérifier si le joueur est arrivé à la sortie
pygame.quit()