import pygame as pg

class Player():
    def __init__(self, width, height):
        self.width = 30
        self.height = 30
        self.x_pos = width/2
        self.y_pos = height - self.height - 40
        self.drawing = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.direction = 0                                      # 0 = neutre // 1 = gauche // 2 = droite
        self.speed = 4
        self.drawing.x = width/2

        self.line = list()
        for i in range(-5,4):
            self.line.append(pg.Rect(self.x_pos - i*30 -15,200,1,height-200))
    def Move(self):
        if self.direction == 1:
            self.drawing.x += self.speed
            self.x_pos += self.speed
        elif self.direction == -1:
            self.drawing.x -= self.speed
            self.x_pos -= self.speed

    def Move_Vision_Box(self):
        for i in range(-5,4):
            self.line[i] = pg.Rect(self.x_pos - i*30 -15,50,1,height-50)
