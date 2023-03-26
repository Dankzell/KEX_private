import pygame
import random
import numpy as np
from Agent import *


# Initialize Pygames
pygame.init()


# Set up the game window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
N = 6
N_WALLS = N*N//10
CELL_SIZE = WINDOW_WIDTH/N
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Grid Game")

# Number of agents
N_PURSUITERS = 1
N_EVADERS = 1

# Game update frequency
FREQUENCY = 1

# Set up the colors
BLACK = (0, 20, 20)
WHITE = (255, 255, 255)
RED = (100, 0, 50)
BLUE = (0, 100, 100)
GRAY = (0,20*3/2,20*3/2)

# Set up the game loop
game_over = False
clock = pygame.time.Clock()