import pygame
import time
from renderer import Renderer
pygame.init()


class Engine:

    def __init__(self):
        self.run = True
        self.renderer = Renderer()
        self.clock = pygame.Clock()
        self.dt = 0

    def delta_time(self):
        self.dt = self.clock.get_time() / 1000

    def update(self):
        """Основной цикл"""
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.renderer.update()

        pygame.quit()
