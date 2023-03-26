import pygame
import random
import numpy as np
from Agent import *
from Constants import *


def create_walls():
    global walls
    walls = []
    for i in range(N_WALLS):
        new_wall =[random.randint(0, N-1), random.randint(0, N-1)]
        walls.append(new_wall)


def create_agents():
    global agents, pursuiters, evaders
    agents = []

    # Create Pursuiters
    for i in range(N_PURSUITERS):
        [x,y] = walls[0]    # Initialize x and y. 
        while [x, y] in walls:
            # Make sure (x, y) is not a wall.
            x = random.randint(0, N-1)
            y = random.randint(0, N-1)

        player1 = Pursuiter(x, y, N, walls)
        agents.append(player1)

    # Create Evaders
    for i in range(N_EVADERS):
        [x,y] = walls[0]    # Initialize x and y. 
        while [x, y] in walls:
            # Make sure (x, y) is not a wall.
            x = random.randint(0, N-1)
            y = random.randint(0, N-1)

    #     player1 = Evader(x, y, N, walls)
    #     agents.append(player1)


##########################################################


create_walls()
create_agents()


while not game_over:

    # Reset grid
    Agent.GRID = np.zeros((N,N), dtype=object)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True


    actions = ["up", "down", "left", "right"]


    # Draw the game board
    WINDOW.fill(BLACK)

    pursuiter_poisitions = []

    for player in agents:

        # Save coordinates or kill
        if player.type == "pursuiter":
            pursuiter_poisitions.append([player.x, player.y])
        elif player.type == "evader" and [player.x, player.y] in pursuiter_poisitions:
            agents.remove(player)

        # Pick an action
        action_index = random.randint(0,3)
        action = actions[action_index]

        player.move(action)


    for player in agents:
        Agent.GRID[player.x, player.y] = player

    
    for player in agents:
        player.update_FOV()

        # Draw the field of view
        pygame.draw.rect(WINDOW, GRAY,(player.x*CELL_SIZE, player.FOV[0]*CELL_SIZE, CELL_SIZE, (player.FOV[1]-player.FOV[0]+1)*CELL_SIZE))
        pygame.draw.rect(WINDOW, GRAY,(player.FOV[2]*CELL_SIZE, player.y*CELL_SIZE, (player.FOV[3]-player.FOV[2]+1)*CELL_SIZE, CELL_SIZE))


    
    for player in agents:
        # I am doing this in a separate loop, so that the field of view does not cover another player.
        
        # Draw player
        pygame.draw.rect(WINDOW, player.color, (player.x*CELL_SIZE, player.y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for wall in walls:
        pygame.draw.rect(WINDOW, BLUE, (wall[0]*CELL_SIZE, wall[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))


    # Update the display
    pygame.display.update()

    # Set the game's frame rate
    clock.tick(FREQUENCY)

# Clean up Pygame
pygame.quit()

