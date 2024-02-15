import pygame

class Text:
    def __init__(self, message: str, x: int, y: int, color):
        self.font = pygame.font.SysFont(None, 30)
        self.message = self.font.render(message, True, color)
        self.color = color
        self.x = x
        self.y = y

    def render(self, display):
        display.blit(self.message, [self.x, self.y])