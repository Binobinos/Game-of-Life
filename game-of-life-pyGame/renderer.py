"""file: renderer.py"""
from display import Display
import pygame

class Renderer:

    def __init__(self):
        self.display = Display()
        self.screen = pygame.display.set_mode((self.display.WIDTH, self.display.HEIGHT))
        self.text = Text(self.screen)

    def update(self):
        """рендер"""
        self.screen.fill((255, 255, 255))
        self.text.render()
        pygame.display.flip()


class Text:

    def __init__(self, screen):
        self.screen = screen
        self._cache = {}

    def render(self, font="Arial", text="None", color=(0, 0, 0), x=0, y=0, size=30):
        key = (text, color, font, size)
        if key not in self._cache:
            font = pygame.font.SysFont(font, size)
            text_surface = font.render(str(text), True, color)
            self._cache[key] = text_surface
        self.screen.blit(self._cache[key], (x, y))

