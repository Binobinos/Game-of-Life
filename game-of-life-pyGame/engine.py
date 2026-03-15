import pygame
from renderer import Renderer
pygame.init()


class Engine:

    def __init__(self):
        self.run = True
        self.renderer = Renderer()

    def update(self):
        """Основной цикл"""
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.renderer.update()

        pygame.quit()
