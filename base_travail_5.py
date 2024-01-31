# Example file showing a circle moving on screen
import pygame 
import random
from labyrinthe import Labyrinthe
from grid import Grid
from utils import Pos
from IO import InputHandler
from item import Item
import time

# pygame setup
pygame.init()

#constantes
tilesize = 32 # taille d'une tuile IG
size = (20, 10) # taille du monde
fps = 30 # fps du jeu
player_speed = 150 # vitesse du joueur
next_move = 0 #tic avant déplacement
filename='color.ini'
# color
color = {
    "ground_color" : "#EDDACF",
    "grid_color" : "#7F513D",
    "player_color" : "#9F715D",
    "wall_color" : "#000000",
    "exit_color" : "#FF0000",
    "cross_color" : "#00FFFF",
    "item_color" : "#FF7F00"  
}
def read_color_parameters(filename):
    with open(filename, 'r') as file:
        for line in file:
            # Ignorer les lignes vides ou celles commençant par #
            if not line.strip() or line.startswith('ini'):
                continue
            line = line[:-1]            
            # Diviser la ligne en clé et valeur
            key, value = map(str.strip, line.split('='))

            # Mettre à jour le dictionnaire Color si la clé existe
            if key in color:
                color[key] = value
                print(f"{key} mis à jour avec la valeur {value}")   

level = "data/laby-02.dat"

laby = Labyrinthe(size[0], size[1])
laby.load_from_file(level)
laby.set_color(color["wall_color"])

grid = Grid(size[0], size[1],tilesize)
grid.set_color(color["grid_color"])

screen = pygame.display.set_mode((size[0]*tilesize, size[1]*tilesize))
clock = pygame.time.Clock() 

running = True
dt = 0
show_grid = True
show_pos = False

keys= { "UP":0 , "DOWN":0, "LEFT":0, "RIGHT":0 }

player_pos = Pos(0,1)

# Appeler la fonction pour lire les paramètres de couleur
read_color_parameters('color.ini')

# Utilisation de la classe dans le programme principal
input_handler = InputHandler(keys)

#création item
item = Item(screen,tilesize,color["item_color"],2,4)
itemFound = False
DisplayMessage = False

#tour de boucle, pour chaque FPS
while running:    
    #
    #   Gestion des I/O  clavier / souris
    #
    keys, running, show_grid, show_pos = input_handler.event_Polling(keys, running, show_grid, show_pos)
    
    #
    # gestion des déplacements
    #

    next_move += dt
    if next_move>0:
        new_x, new_y = player_pos.x, player_pos.y
        if keys['UP'] == 1:
            new_y -=1
        elif keys['DOWN'] == 1:
            new_y += 1
        elif keys['LEFT'] == 1:
            new_x -=1
        elif keys['RIGHT'] == 1:
            new_x += 1

        # vérification du déplacement du joueur                                    
        if not laby.hit_box(new_x, new_y):
            player_pos.x, player_pos.y = new_x, new_y
            next_move -= player_speed
            if new_x == item.x and new_y == item.y:
                itemFound = True

        if show_pos:
            print("pos: ",player_pos)

    #
    # affichage des différents composants graphique
    #
    screen.fill(color["ground_color"])

    laby.draw(screen, tilesize)

    if show_grid:
        grid.draw(screen)

    pygame.draw.rect(screen, color["player_color"], pygame.Rect(player_pos.x*tilesize, player_pos.y*tilesize, tilesize, tilesize))
    
    #croix dans la dernière case
    pygame.draw.line(screen,color["cross_color"],((size[0]-1)*tilesize,(size[1]-2)*tilesize),(size[0]*tilesize,(size[1]-1)*tilesize),2)
    pygame.draw.line(screen,color["cross_color"],(size[0]*tilesize,(size[1]-2)*tilesize),((size[0]-1)*tilesize,(size[1]-1)*tilesize),2)
    
    # test triangle
    item.pos_item()
    # affichage des modification du screen_view
    pygame.display.flip()
    # gestion fps
    dt = clock.tick(fps)

    # Vérifier si le joueur est arrivé à la sortie
    if grid.arriver(player_pos.x, player_pos.y):
        if not DisplayMessage:
            if itemFound:
                print("arrivé avec 1 item, level validé")
                running = False
                time.sleep(5)
            else:
                print("arrivé sans item, level en attente de validation, rechercher le diamant")
            DisplayMessage = True
    else:
        DisplayMessage = False
pygame.quit()