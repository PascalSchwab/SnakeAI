import pygame
from snake import Snake
from food import Food
from text import Text
from const import WHITE, WIDTH, HEIGHT, FRAME_PER_SECOND, AI_FPS

class Game:
    def __init__(self, title: str):
        self.__init_pygame(title)

        self.clock = pygame.time.Clock()
        self.running = False
        self.snake = Snake()
        self.food = Food(self.snake)

        self.score = 0

        self.frame_iteration = 0

    def start(self):
        self.running = True

        while self.running:
            # Check Input
            for event in pygame.event.get():
                self.checkInput(event)
                self.snake.checkInput(event)
            
            # Update
            self.update()

            # Render
            self.display.fill(self.background_color)
            self.render()
            pygame.display.update()

            # Tick Speed
            self.clock.tick(FRAME_PER_SECOND)

        pygame.quit()
        quit()

    def play_step(self, action):
        self.frame_iteration += 1

        reward = 0
        game_over = False
        
        self.snake.move_by_action(action)
        self.snake.body.insert(0, [self.snake.x, self.snake.y])
        if self.is_colliding(self.snake.x, self.snake.y) or self.frame_iteration > 100 * len(self.snake.body):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        if self.snake.x == self.food.x and self.snake.y == self.food.y:
            self.score += 1
            reward = 10
            self.frame_iteration = 0
            self.food.respawn(self.snake)
        else:
            self.snake.body.pop()

        self.display.fill(self.background_color)
        self.render()
        pygame.display.update()

        self.clock.tick(AI_FPS)
        return reward, game_over, self.score
        

    def __init_pygame(self, title):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(title)
        self.background_color = WHITE
        self.display.fill(self.background_color)
        pygame.display.update()

    def stop(self):
        self.running = False

    def restart(self):
        self.score = 0
        self.frame_iteration = 0
        self.snake.respawn()
        self.food.respawn(self.snake)

    def update(self):
        self.snake.update()

        # Eat Food
        if self.snake.x == self.food.x and self.snake.y == self.food.y:
            self.food.respawn(self.snake)
            self.score += 1
        else:
            self.snake.body.pop()

        if self.is_colliding(self.snake.x, self.snake.y):
            self.restart()

    def render(self):
        self.snake.render(self.display)
        self.food.render(self.display)

    def checkInput(self, event):
        if event.type == pygame.QUIT:
            self.stop()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.stop()
            if event.key == pygame.K_r:
                self.restart()

    def is_colliding(self, x: int, y: int):
        # Touching Body
        for block in self.snake.body[1:]:
            if x == block[0] and y == block[1]:
                return True
        # Out of bounds
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return True
        return False