
import pygame
import random
import numpy as np
from Constants import *


class Agent():
    GRID = 0

    def __init__(self, x: int, y: int, N: int, walls: list):
        self.x = x                  # The x coordinate of the agent
        self.y = y                  # The y coordinate of the agent
        self.walls = walls          # A list of wall coordinates
        self.N = N                  # Grid high/ width
        self.FOV = [0,0,0,0]        # Field of view. [upper, lower, left, right]
        self.grid = None
        self.observation = []
        self.knowledge = np.ones((N,N))

    def move(self, action):
        # Handle player movement
        if action == "up" and self.y > 0:
            if [self.x, self.y-1] not in self.walls:
                self.y -= 1
        elif action == "down" and self.y < self.N-1:
            if [self.x, self.y+1] not in self.walls:
                self.y += 1
        elif action == "left" and self.x > 0:
            if [self.x-1, self.y] not in self.walls:
                self.x -= 1
        elif action == "right" and self.x < self.N-1:
            if [self.x+1, self.y] not in self.walls:
                self.x += 1


    def update_FOV(self):
        # Update field of view

        upper, lower = self.y, self.y
        left, right = self.x, self.x
        

        # Propagate upwards
        while [self.x, upper - 1] not in self.walls and upper > 0:
            upper = upper - 1

        # Propagate downwards
        while [self.x, lower + 1] not in self.walls and lower < self.N - 1:
            lower = lower + 1

        # Propagate left
        while [left -1, self.y] not in self.walls and left >= 1:
            left = left - 1

        # Propagate right
        while [right + 1, self.y] not in self.walls and right < self.N - 1:
            right = right + 1

        self.FOV = [upper, lower, left, right]

        vertical_vision_field = Agent.GRID[self.x, upper: lower]
        horizontal_vision_field = Agent.GRID[left:right, self.y]

        # Merges all the vision into one list, and removes the agent itself.
        vision = np.concatenate((vertical_vision_field, horizontal_vision_field))
        vision = vision[vision != self]

        self.update_observation(vision)

    
    def update_observation(self, vision):
        # Updates the observation, i.e which agents this agent sees.
        
        self.observation = [] # Reset observations        

        # If the agent finds other agents, they are appended to self.observation
        agents_seen = [] #gustav
        print(self.knowledge.transpose()) #had to transpose it for it to align with the game 
        print(self.FOV)
        print("\n")

        for object in vision: 
            if isinstance(object, Agent):
                print(object.type)
                agents_seen.append(object) #gustav
                self.observation.append(object)
                print(object.type, object.x, object.y)
                self.convert_adjacent_to_ones()
                self.clear_vision()
                self.knowledge[object.x, object.y] = 1
            else:
                self.convert_adjacent_to_ones()
                self.clear_vision()

        number_of_evaders = 1;
        # if len(agents_seen) == number_of_evaders: #gotta differ between evaders and pursuers
        #     self.clear_knowledge(agents_seen)
#prob onödig men idk kanske behövs
    # def knowledge_update(self, object, vision):
    #     if isinstance(object, Agent):
    #         self.knowledge[object.x, object.y] = 1
    #         self.convert_adjacent_to_ones()
    #         self.clear_vision()
    #     else:
    #         self.convert_adjacent_to_ones()
    #         self.clear_vision()

    

    def convert_adjacent_to_ones(self):
        rows, cols = N,N
        ones = np.argwhere(self.knowledge == 1)
        for i, j in ones:
            if i > 0 and self.knowledge[i-1, j] == 0:
                self.knowledge[i-1, j] = 1
            if i < rows-1 and self.knowledge[i+1, j] == 0:
                self.knowledge[i+1, j] = 1
            if j > 0 and self.knowledge[i, j-1] == 0:
                self.knowledge[i, j-1] = 1
            if j < cols-1 and self.knowledge[i, j+1] == 0:
                self.knowledge[i, j+1] = 1  

    def clear_vision(self):
        self.knowledge[self.FOV[2]:self.FOV[3]+1, self.y] = 0
        self.knowledge[self.x, self.FOV[0]:self.FOV[1]+1] = 0
        # print(self.knowledge[self.FOV[0]:self.FOV[1], :])
#         print(self.knowledge[self.FOV[2]:self.FOV[3], :])
                
    
    def clear_knowledge(self, agents_position):
        np.zeros(self.knowledge)
        for agent in agents_position:
            self.knowledge[agent.x, agent.y] = 1

    def print_grid():
        print(Agent.GRID)


class Pursuiter(Agent):
    def __init__(self, x: int, y: int, N: int, walls: list):
        super().__init__(x, y, N, walls)
        self.color = (255,255,255)
        self.type = "pursuiter"

class Evader(Agent):
    def __init__(self, x: int, y: int, N: int, walls: list):
        super().__init__(x, y, N, walls)
        self.color = (255,100,100)
        self.type = "evader"