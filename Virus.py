import pygame as pg
import sys
import random as rd
import os
#TEST

screen_width = 640   #define screen width
screen_height = 480  #define screen height
game_speed = 30 #game speed must be changed to make AI learn faster (30 is normal, 100 is faster)
count_to_new_virus = 0
virus_rate = 100
screen = pg.display.set_mode((screen_width, screen_height))
clock = pg.time.Clock()
start = 0
done = False
nPlayers = ''



img_virus = None
img_bg = None

def TextObj(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,idlecolor,activecolor):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(screen, activecolor,(x,y,w,h))

        if click[0] == 1:
            return True
    else:
        pg.draw.rect(screen, idlecolor,(x,y,w,h))


    smallText = pg.font.SysFont("cominnercolorsansms",20)
    textSurf, textRect = TextObj(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)
    return False

#BackGround = Background('background.png', [0,0])


def main():

    global count_to_new_virus
    global start
    global done

    player1 = Player()
    enemies = []


    while not done:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                try:
                    sys.exit()
                except:
                    print(sys.exc_info()[0])
                    pg.display.quit()
                pg.quit()
                os._exit(os.EX_OK)


        if(not done):
            MainMenu()
        #print(done)
        while start:
            #run(config_path)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    start = 0
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
                start = 0


            player1.Move()
            screen.fill((0, 150, 255))
            draw_bg = pg.Rect(0, 0, screen_width, screen_height)
            screen.blit(img_bg, draw_bg)
            pg.draw.rect(screen, (150, 200, 20), player1.drawing)
            player1.Move_Vision_Box()
            for i in range(0,9):
                pg.draw.rect(screen, (150, 200, 20), player1.line[i])
            count_to_new_virus += 1
            if(count_to_new_virus == virus_rate):
                count_to_new_virus = 0
                enemies.append(Enemy())
            if len(enemies) > 0:
                for x in range (0,len(enemies)):
                    enemies[x].Move()
                    screen.blit(img_virus, enemies[x].drawing)
            if CheckColision(player1, enemies):
                start = 0
                #pg.quit()
                #sys.exit()
            Check_Vision(player1, enemies)
            pg.display.flip()                                       #Update L'écran au complet
            clock.tick(game_speed)                            #1 frame au 30 millisecondes (delaie l'update de pygame)

class Player():
    def __init__(self):
        global screen_width
        global screen_height
        self.width = 30
        self.height = 30
        self.x_pos = screen_width/2
        self.y_pos = screen_height - self.height - 40
        self.drawing = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.direction = 0                                      # 0 = neutre // 1 = gauche // 2 = droite
        self.speed = 4

        self.line = list()
        for i in range(-5,4):
            self.line.append(pg.Rect(self.x_pos - i*30 -15,200,1,screen_height-200))


    def Move(self):
        if self.direction == 1:
            self.drawing.x += self.speed
            self.x_pos += self.speed
        elif self.direction == -1:
            self.drawing.x -= self.speed
            self.x_pos -= self.speed

    def Move_Vision_Box(self):
        for i in range(-5,4):
            self.line[i] = pg.Rect(self.x_pos - i*30 -15,50,1,screen_height-50)


class Enemy():
    def __init__(self):
        global screen_width
        global screen_height
        rd.seed()
        self.width = 30
        self.height = 30
        self.x_pos = rd.randint(0, screen_width - self.width)
        self.y_pos = 0-self.height                       #crée le bloc au dessus de l'écran quand il spawn
        self.speed = 1
        self.drawing = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def Move(self):
        if self.y_pos > screen_height:
            del self
        else:
            self.y_pos += self.speed
            self.drawing.y += self.speed
        #self.hitbox(self.x_pos +10, self.y_pos+10, 10, 10)

def CheckColision(player, enemy):
    for x in range (0,len(enemy)):
        if  (player.x_pos < (enemy[x].x_pos + enemy[x].width) and
            player.x_pos + player.width > enemy[x].x_pos and
            enemy[x].y_pos + enemy[x].height > screen_height - player.height - 40 and
            enemy[x].y_pos <= screen_height - 40):
            return True
    return False

def Check_Vision(player, enemy):
    table = [0,0,0,0,0,0,0,0,0]
    for i in range (0, len(enemy)):
        #if True:
        for j in range (-4,5):
            pos = player.x_pos + j*30 + 15
            if (pos in range(enemy[i].x_pos, enemy[i].x_pos + 30)) and (enemy[i].y_pos in range(50,screen_height)):
                table[j+4] = (enemy[i].y_pos)/480
            else:
                pass

    return table



def MainMenu():
    global nPlayers


    screen.fill((0, 150, 255))
    largeTextFont = pg.font.Font('freesansbold.ttf',90)
    smallTextFont = pg.font.Font("freesansbold.ttf",20)

    textSurfb1, textRectb1 = TextObj("Virus Invaders", largeTextFont)
    textRectb1.center = (screen_width/2, screen_height/2-100)
    screen.blit(textSurfb1, textRectb1)

    if button("Start", 150,300,100,50,(0,200,0),(0,255,0)):    #(msg,x,y,w,h,idlecolor,activecolor:
        global start
        start = 1

    if button("nb. Players: ", 350,300,200,50, (0,0,200), (0,0,255)):
        end = 0
        nPlayers = ''
        while not end:
            for event in pg.event.get():
                print('in for')
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        end = 1
                    elif event.key == pg.K_BACKSPACE:
                        nPlayers = nPlayers[:-1]
                    else:
                        nPlayers += event.unicode

    textSurfb2, textRectb2 = TextObj(nPlayers, smallTextFont)
    textRectb2.center = (500, 325)
    screen.blit(textSurfb2, textRectb2)


    pg.display.update()
    clock.tick(15)




def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)



#if __name__ == '__main__':
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward.txt')
img_virus = pg.image.load(local_dir + '/virus_1.png')
img_bg = pg.image.load(local_dir + '/background.png')
pg.init()
main()
#sys.exit()
