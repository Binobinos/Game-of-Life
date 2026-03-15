"""file: renderer.py"""
from display import Display
from game_scene.global_scene import Scene0

import pygame

class Renderer:

    def __init__(self):
        self.display = Display()
        self.screen = pygame.display.set_mode((self.display.WIDTH, self.display.HEIGHT))
        pygame.display.set_caption(self.display.window_name)
        self.text = Text(self.screen)
        self.scene0 = Scene0(self.display, self.screen, self.text)

    def update(self, dt, clock):
        """рендер"""
        self.screen.fill((0, 0, 0))
        self.scene0.render(dt, clock)
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

        match x:
            case "center":
                x = (self.screen.get_width() // 2) - (self._cache[key].width // 2)
            case "left":
                x = 0
            case "right":
                x = (self.screen.get_width()) - self._cache[key].width

        if y == "center":
            x = (self.screen.get_height()  // 2) - (self._cache[key].height // 2)
        self.screen.blit(self._cache[key], (x, y))

