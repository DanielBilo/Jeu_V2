import pygame as pg
import sys
import random as rd
import os
from player import Player
from enemy import Enemy
#TEST

screen_width = 640   #define screen width
screen_height = 480  #define screen height
game_speed = 30 #game speed must be changed to make AI learn faster (30 is normal, 100 is faster)
count_to_new_virus = 0
virus_rate = 100
screen = pg.display.set_mode((screen_width, screen_height))
gen = 0
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


def eval_genomes(genomes, config):

    global count_to_new_virus
    global screen
    global gen

    players = []
    enemies = []
    nets = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player(screen_width,screen_height))
        ge.append(genome)

    score = 0
    clock = pg.time.Clock()

    run = True



    while run and len(players) > 0:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                quit()
                break


        for x, player in enumerate(players):
            ge[x].fitness +=1
            player.Move()

            data = Check_Vision(player, enemies)

            output = nets[players.index(player)].activate((player.x_pos, data[0], data[1], data[2],data[3],data[4],data[5],data[6],data[7],data[8]))

            if output[0] > 0.5:
                player.direction = 1
            elif output[0] < -0.5:
                player.direction = -1
            else:
                player.direction = 0

        screen.fill((0, 150, 255))
        draw_bg = pg.Rect(0, 0, screen_width, screen_height)
        screen.blit(img_bg, draw_bg)


        for x in range (0, len(players)):
            pg.draw.rect(screen, (150, 200, 20), players[x].drawing)

        count_to_new_virus += 1
        if(count_to_new_virus == virus_rate):
            count_to_new_virus = 0
            enemies.append(Enemy(screen_width, screen_height))
        if len(enemies) > 0:
            for x in range (0,len(enemies)):
                enemies[x].Move()
                screen.blit(img_virus, enemies[x].drawing)


        for x in range (0, len(players)):
            #players[x].Move_Vision_Box()
            Check_Vision(players[x], enemies)

            if CheckColision(players[x], enemies):
                start = 0
            #pg.quit()
            #sys.exit()

        pg.display.flip()                                       #Update L'écran au complet
        clock.tick(game_speed)                            #1 frame au 30 millisecondes (delaie l'update de pygame)



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
