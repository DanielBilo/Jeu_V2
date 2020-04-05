import pygame as pg
import sys
import random as rd
#From Virus_python import Ennemie
#TEST

screen_width = 640   #define screen width
screen_height = 480  #define screen height
game_speed = 30 #game speed must be changed to make AI learn faster (30 is normal, 100 is faster)

img_virus = pg.image.load('virus_1.png')
img_bg = pg.image.load('background.png')

#BackGround = Background('background.png', [0,0])


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

        #for enn in enemies:
        #    if player1.colliderect(enn):
        #        done = True
        # Control de tout le clavier
        keys = pg.key.get_pressed()
        release_p = 0
        if keys[pg.K_a]:  #to move left.
            player1.direction = -1
        elif keys[pg.K_d]: #to move right
            player1.direction = 1
        else:
            player1.direction = 0
        if keys[pg.K_p]:
            exit()
            quit()

        player1.Move()

        screen.fill((0, 150, 255))
        draw_bg = pg.Rect(0, 0, screen_width, screen_height)                       #couleur backgroud besoin d'être dans la loop?
        screen.blit(img_bg, draw_bg)

        pg.draw.rect(screen, (150, 200, 20), player1.drawing)


        if len(enemies) > 0:
            for x in range (0,len(enemies) - 1):
                enemies[x].Move()
                screen.blit(img_virus, enemies[x].drawing)

        if CheckColision(player1, enemies):
            pg.quit()
            sys.exit()

        pg.display.flip()                                       #Update L'écran au complet
        clock.tick(game_speed)                                  #1 frame au 30 millisecondes (delaie l'update de pygame)

class Player():
    def __init__(self):
        global screen_width
        global screen_height
        self.width = 20
        self.height = 20
        self.x_pos = screen_width/2
        self.y_pos = screen_height - self.height - 40
        self.drawing = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.direction = 0                                      # 0 = neutre // 1 = gauche // 2 = droite
        self.speed = 4

    def Move(self):
        if self.direction == 1:
            self.drawing.x += self.speed
            self.x_pos += self.speed
        elif self.direction == -1:
            self.drawing.x -= self.speed
            self.x_pos -= self.speed
        #self.hitbox(self.x_pos +10, self.y_pos+10, 10, 10)

class Enemy():
    def __init__(self):
        global screen_width
        global screen_height
        rd.seed()
        self.width = 30
        self.height = 30
        self.x_pos = rd.randint(0, screen_width - self.width)
        self.y_pos = rd.randint(-5000, 0-self.height)                       #crée le bloc au dessus de l'écran quand il spawn
        self.speed = 5
        self.drawing = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def Move(self):
        if self.y_pos > screen_height:
            rd.seed()
            self.y_pos = rd.randint(-5000, 0-self.height)
            self.drawing.y = self.y_pos
        else:
            self.y_pos += self.speed
            self.drawing.y += self.speed
        #self.hitbox(self.x_pos +10, self.y_pos+10, 10, 10)


def CheckColision(player, enemy):
    for x in range (0,len(enemy)-1):
        if  (player.x_pos < (enemy[x].x_pos + enemy[x].width) and
            player.x_pos + player.width > enemy[x].x_pos and
            enemy[x].y_pos + enemy[x].height > screen_height - player.height and
            enemy[x].y_pos <= screen_height):
            return True
    return False
            #print("collision")


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()
