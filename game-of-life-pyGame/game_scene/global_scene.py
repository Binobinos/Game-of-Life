"""тестовый файл"""
import pygame

class Scene0:

    def __init__(self, display, screen, text):
        self.display = display
        self.screen = screen
        self.text = text

        self.screen_color = (255, 255, 255)

    def render(self, dt, clock):
        self.screen.fill(self.screen_color)
        self.text.render(text="Hello World")
        self.text.render(text="Game - Of - Life", x=500)