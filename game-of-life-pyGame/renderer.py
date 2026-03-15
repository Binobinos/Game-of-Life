"""file: renderer.py"""
from display import Display
import pygame

class Renderer:

    def __init__(self):
        self.display = Display()
        self.screen = pygame.display.set_mode((self.display.WIDTH, self.display.HEIGHT))

    def update(self):
        """рендер"""
        self.screen.fill((255, 255, 255))
        pygame.display.flip()