import pygame
from grid import Grid

class Game:
    def __init__(self):
        self.time = 0
        self.maxlayer = 0
        self.grid = Grid(self.maxlayer)

    def handle_click(self, mouse_pos, ui_manager):
        self.grid.handle_click(mouse_pos, ui_manager)

    def print(self, screen):
        self.grid.print(screen)

    def reset(self):
        self.grid = Grid(self.maxlayer)

    def set_maxlayer(self, layer_count):
        self.maxlayer = layer_count
        self.grid = Grid(self.maxlayer)
