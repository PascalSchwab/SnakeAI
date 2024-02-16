import pygame
import random
from const import RED, BLOCK_SIZE, WIDTH, HEIGHT
from snake import Snake

class Food:
    def __init__(self, snake: Snake):
        self.respawn(snake)

    def respawn(self, snake: Snake):
        r_x = random.randint(0, WIDTH-1)
        r_y = random.randint(0, HEIGHT-1)
        self.x = r_x - r_x % BLOCK_SIZE
        self.y = r_y - r_y % BLOCK_SIZE
        if [self.x, self.y] in snake.body:
            self.respawn(snake)

    def update(self):
        pass

    def render(self, display):
        pygame.draw.rect(display, RED, [self.x, self.y, BLOCK_SIZE, BLOCK_SIZE])