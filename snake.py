from const import BLUE, BLOCK_SIZE
from direction import Direction
import pygame
import numpy as np

class Snake:
    def __init__(self):
        self.respawn()
    
    def respawn(self):
        self.x = 100
        self.y = 50
        self.direction: Direction = Direction.RIGHT
        self.change_to_dir: Direction = self.direction
        self.body = [[100, 50], [90, 50], [80, 50], [70, 50]]

    def update(self):
        # Two keys at the same time
        if self.change_to_dir == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        if self.change_to_dir == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        if self.change_to_dir == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        if self.change_to_dir == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT

        # Move snake
        if self.direction == Direction.UP:
            self.y -= 10
        if self.direction == Direction.DOWN:
            self.y += 10
        if self.direction == Direction.LEFT:
            self.x -= 10
        if self.direction == Direction.RIGHT:
            self.x += 10

        self.body.insert(0, [self.x, self.y])

    def render(self, display):
        for position in self.body:
            pygame.draw.rect(display, BLUE, [position[0], position[1], BLOCK_SIZE, BLOCK_SIZE])

    def checkInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.change_to_dir = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                self.change_to_dir = Direction.RIGHT
            elif event.key == pygame.K_UP:
                self.change_to_dir = Direction.UP
            elif event.key == pygame.K_DOWN:
                self.change_to_dir = Direction.DOWN

    def move_by_action(self, action):
        clock_dir = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        current_dir_index = clock_dir.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):   # Straight
            self.change_to_dir = clock_dir[current_dir_index]
        elif np.array_equal(action, [0, 1, 0]): # Right turn
            next_dir_index = (current_dir_index+1) % 4
            self.change_to_dir = clock_dir[next_dir_index]
        elif np.array_equal(action, [0, 0, 1]): # Left turn 
            next_dir_index = (current_dir_index - 1) % 4
            self.change_to_dir = clock_dir[next_dir_index]
        self.direction = self.change_to_dir

        if self.direction == Direction.UP:
            self.y -= 10
        if self.direction == Direction.DOWN:
            self.y += 10
        if self.direction == Direction.LEFT:
            self.x -= 10
        if self.direction == Direction.RIGHT:
            self.x += 10