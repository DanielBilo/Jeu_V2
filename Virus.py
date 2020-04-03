import pygame as pg
import sys
import random as rd
#From Virus_python import Ennemie
#TEST

screen_width = 640   #define screen width
screen_height = 480  #define screen height

def main():

    player1 = Player()

    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()
    done = False
    enemies = []
    for x in range(30):
        enemies.append(Enemy())

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True


        # Control de tout le clavier
        keys = pg.key.get_pressed()
        release_p = 0
        if keys[pg.K_a]:  #to move left.
            player1.direction = 2
        elif keys[pg.K_d]: #to move right
            player1.direction = 1
        else:
            player1.direction = 0



        """#print ("key_p ", keys[pg.K_p])
        #print ("release ", release_p)
        if keys[pg.K_p] and release_p == 0:
            enemies.append(Enemy())
            release_p = 1

        elif keys[pg.K_p] == 0 and release_p == 1:
            release_p = 0
            print ("key_p ", keys[pg.K_p])
            print ("release ", release_p)"""

        player1.Move()

        screen.fill((40, 40, 40))                       #couleur backgroud besoin d'être dans la loop?
        pg.draw.rect(screen, (150, 200, 20), player1.drawing)

        if len(enemies) > 0:
            for x in range (0,len(enemies) - 1):
                enemies[x].Move()
                pg.draw.rect(screen, (150, 200, 20), enemies[x].drawing)

        CheckColision(player1, enemies)


        pg.display.flip()                               #Update L'écran au complet
        clock.tick(30)                                  #1 frame au 30 millisecondes (delaie l'update de pygame)

class Player():
    def __init__(self):
        global screen_width
        global screen_height
        self.width = 20
        self.height = 20
        self.x_pos = screen_width/2
        self.y_pos = screen_height - self.height
        self.drawing = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.direction = 0 # 0 = neutre // 1 = gauche // 2 = droite
        self.speed = 4

    def Move(self):
        if self.direction == 1:
            self.drawing.x += self.speed
            self.x_pos += self.speed
        elif self.direction == 2:
            self.drawing.x -= self.speed
            self.x_pos -= self.speed

class Enemy():
    def __init__(self):
        global screen_width
        global screen_height
        rd.seed()
        self.width = 100
        self.height = 100
        self.x_pos = rd.randint(0, screen_width - self.width)
        self.y_pos = rd.randint(-5000, 0-self.height)            #crée le bloc au dessus de l'écran quand il spawn
        self.speed = 5
        self.drawing = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)
        #corona = pg.circle(300, 20, 20, 20)

    def Move(self):
#        pg.draw.circle(screen, (255, 10, 10), (enemy, 20, 20, 20))
        self.y_pos += self.speed
        self.drawing.y += self.speed

def CheckColision(player, enemy):
    for x in range (0,len(enemy)-1):
        if  (player.x_pos < (enemy[x].x_pos + enemy[x].width) and
            player.x_pos + player.width > enemy[x].x_pos and
            enemy[x].y_pos + enemy[x].height > screen_height - player.height and
            enemy[x].y_pos <= screen_height):
            print("collision")
            print("other")



if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()
