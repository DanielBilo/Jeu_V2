import random as rd
import pygame as pg

class Enemy():
    def __init__(self, width, height):
        self.screen_width = width
        self.screen_height = height
        rd.seed()
        self.width = 30
        self.height = 30
        self.x_pos = rd.randint(0, self.screen_width - self.width)
        self.y_pos = 0-self.height                       #crée le bloc au dessus de l'écran quand il spawn
        self.speed = 4
        self.drawing = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def Move(self):
        self.y_pos += self.speed
        self.drawing.y += self.speed
