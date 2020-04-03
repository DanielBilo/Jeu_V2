import pygame as pg
import sys
import random as rd
#From Virus_python import Ennemie

screen_width = 640   #define screen width
screen_height = 480  #define screen height

def main():

    player1 = Player()

    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True


        # Control de tout le clavier
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:  #to move left.
            player1.direction = 2
        elif keys[pg.K_d]: #to move right
            player1.direction = 1
        else:
            player1.direction = 0

        player1.Move()


        screen.fill((40, 40, 40))                       #couleur backgroud
        pg.draw.rect(screen, (150, 200, 20), player1.drawing)      #??? besoin d'être dans la loop??? c'est quoi

        pg.display.flip()                               #Update L'écran au complet
        clock.tick(30)                                  #1 frame au 30 millisecondes (delaie l'update de pygame)

class Player():
    def __init__(self):
        global screen_width
        global screen_height
        self.pos_x = screen_width/2
        self.pox_y = screen_height/2
        self.width = 20
        self.height = 20
        self.drawing = pg.Rect(screen_width/2, screen_height/2, self.width, self.height)
        self.direction = 0 # 0 = neutre // 1 = gauche // 2 = droite
        self.speed = 4

    def Move(self):
        if self.direction == 1:
            self.drawing.x += self.speed
        elif self.direction == 2:
            self.drawing.x -= self.speed



if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()


class Enemy():
    def __init__(self):
        rd.seed()
        self.enemy = rd.randint(100,540)
        #corona = pg.circle(300, 20, 20, 20)

    def update():
        pg.draw.circle(screen, (255, 10, 10), (enemy, 20, 20, 20))
