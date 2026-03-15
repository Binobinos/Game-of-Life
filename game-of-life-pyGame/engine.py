"""file: engine.py"""
import pygame
import time
from renderer import Renderer
pygame.init()


class Engine:

    def __init__(self):
        self.run = True
        self.renderer = Renderer()
        self.display = self.renderer.display

        #time
        self.clock = pygame.Clock()
        self.last_time = pygame.time.get_ticks()
        self.dt = 0

    def delta_time(self):
        self.dt = self.clock.get_time() / 1000

    def fps_tick(self):
        if self.display.FPS > 0:
            target_frame_time = 1.0 / self.display.FPS
            while True:
                now = time.perf_counter()
                remaining = target_frame_time - (now - self.last_time)
                if remaining <= 0:
                    break
            self.last_time = now
            self.clock.tick()

    def update(self):
        """Основной цикл"""
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.renderer.update()
            self.fps_tick()

        pygame.quit()
