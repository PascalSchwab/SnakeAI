from const import MAX_MEMORY, LEARNING_RATE, BLOCK_SIZE, BATCH_SIZE
import torch
import random
import numpy as np
from collections import deque
from model import Model
from trainer import Trainer
from direction import Direction
from point import Point
from game import Game

class QAgent():
    def __init__(self):
        self.game_count = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Model(11, 256, 3)
        self.trainer = Trainer(self.model, LEARNING_RATE, self.gamma)

    def is_collision(self, point: Point, game: Game):
        return game.is_colliding(point.x, point.y)

    def get_state(self, game: Game):
        head = Point(game.snake.x, game.snake.y)
        point_left = Point(head.x-BLOCK_SIZE, head.y)
        point_right = Point(head.x+BLOCK_SIZE, head.y)
        point_up = Point(head.x, head.y-BLOCK_SIZE)
        point_down = Point(head.x, head.y+BLOCK_SIZE)

        is_direction_left = game.snake.direction == Direction.LEFT
        is_direction_right = game.snake.direction == Direction.RIGHT
        is_direction_up = game.snake.direction == Direction.UP
        is_direction_down = game.snake.direction == Direction.DOWN

        state = [
            (is_direction_right and self.is_collision(point_right, game)) or
            (is_direction_left and self.is_collision(point_left, game)) or
            (is_direction_up and self.is_collision(point_up, game)) or
            (is_direction_down and self.is_collision(point_down, game)),

            (is_direction_up and self.is_collision(point_right, game)) or
            (is_direction_down and self.is_collision(point_left, game)) or
            (is_direction_left and self.is_collision(point_up, game)) or
            (is_direction_right and self.is_collision(point_down, game)),

            (is_direction_down and self.is_collision(point_right, game)) or
            (is_direction_up and self.is_collision(point_left, game)) or
            (is_direction_right and self.is_collision(point_up, game)) or
            (is_direction_left and self.is_collision(point_down, game)),

            is_direction_left,
            is_direction_right,
            is_direction_up,
            is_direction_down,

            game.food.x < game.snake.x,
            game.food.x > game.snake.x,
            game.food.y < game.snake.y,
            game.food.y > game.snake.y
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        final_move = [0, 0, 0]
        state0 = torch.tensor(state, dtype=torch.float)
        prediction = self.model(state0)
        move = torch.argmax(prediction).item()
        final_move[move] = 1

        return final_move