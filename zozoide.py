import pygame
import time
import random
import pygame_menu
import os

pygame.init()

# TODO : le set repeat doit dependre de la difficulte
pygame.key.set_repeat(40,30)

base_color = (225,106,114)

infoObject = pygame.display.Info()

surfaceW = infoObject.current_w # screen width (1000 sur mon Lenovo)
surfaceH = infoObject.current_h # screen heigth (800 sur mon Lenovo)

surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#surface = pygame.display.set_mode((surfaceW, surfaceH))

pygame.display.set_caption("ZoZoïDe")

player_name = ""
current_max_score = 0

# declaration of useful global variables
rematch = False

diff = 1
last_diff = 1
difficulty_changed = False
nb_tour_max = 20

is_menu = True

# init mixer to play a song during the game
pygame.mixer.init()

# global game management
game_finished = False

# init of turns made
nb_tour = 0

espace_between_cond_start = int(surfaceH/2)

# dimensions zozoide
zoidW = int(surfaceW/8)
zoidH = int(surfaceH/10)

# dimension condom at start
condWstart = int(surfaceW/32)
condHstart = int(surfaceH/12)

# init of speed (of condoms) variable
speed = 1.5

def get_player_name(name):
    global player_name
    player_name = name

def surface_init():
    surface.fill(base_color)
    pygame.display.update()



def set_difficulty(value, difficulty):
    global diff, last_diff, nb_tour_max, difficulty_changed

    diff = difficulty

    if (last_diff != diff):
        difficulty_changed = True

    last_diff = diff

    if (diff == 1):
        nb_tour_max = 20
    elif (diff == 2):
        nb_tour_max = 23
    elif (diff == 3):
        nb_tour_max = 26
    elif (diff == 4):
        nb_tour_max = 29


def start_the_game():
    global is_menu
    is_menu = False

def backgr():
    surface.fill(base_color)

# creating global menu
menu = pygame_menu.Menu(surfaceH / 2, surfaceW / 2, 'Zozoide', theme=pygame_menu.themes.THEME_GREEN)
menu.add_text_input('Nom : ', default='', onchange=get_player_name)
menu.add_selector('Difficulté : ', [('Facile', 1), ('Moyen', 2), ('Difficile', 3), ('Très difficile', 4)],
                      onchange=set_difficulty)
menu.add_button('Jouer', start_the_game)
menu.add_button('Quitter', pygame_menu.events.EXIT)

def display_menu():
    global menu

    # waiting for user to set informations in menu
    while True:

        backgr()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if (menu.is_enabled()):
            menu.update(events)
            menu.draw(surface)

        if not is_menu:
            break

        pygame.display.update()


# fonctions de fin de jeu

def creaTexteObjs (texte, font):
    texteSurface = font.render(texte,True, (255, 255, 255))
    return texteSurface, texteSurface.get_rect()

def msgAccueil (texte):
    petitTexte = pygame.font.Font('data\police\BradBunR.ttf', int(surfaceW/30))

    petitTexteSurf, petitTexteRect = creaTexteObjs(texte, petitTexte )
    petitTexteRect.center = surfaceW/2, ((surfaceH/2) + 50)
    surface.blit(petitTexteSurf, petitTexteRect)

    pygame.display.update()

def display_score():
    txt_size = pygame.font.Font('data\police\BradBunR.ttf', 20)
    petitTexteSurf, petitTexteRect = creaTexteObjs \
        ("Max Score : "+str(current_max_score)+"/"+str(nb_tour_max), txt_size)
    petitTexteRect.center = (int(surfaceW/20),int(surfaceH/70))
    surface.blit(petitTexteSurf, petitTexteRect)

    pygame.display.update()


def msgSurface (texte):
    GOTexte = pygame.font.Font('data\police\BradBunR.ttf', 150)
    petitTexte = pygame.font.Font('data\police\BradBunR.ttf', 20)

    titreTexteSurf, titreTexteRect = creaTexteObjs(texte, GOTexte)
    titreTexteRect.center = surfaceW/2, ((surfaceH/2)-50)
    surface.blit(titreTexteSurf, titreTexteRect)

    petitTexteSurf, petitTexteRect = creaTexteObjs\
        ("appuyer sur espace pour rejouer, Echap pour quitter ou M pour retourner au menu", petitTexte )
    petitTexteRect.center = surfaceW/2, ((surfaceH/2) + 50)
    surface.blit(petitTexteSurf, petitTexteRect)

    pygame.display.update()

    # on update le max score avant de reset les variables de jeu
    update_score()

    global x_zoid, y_zoid, nb_tour, speed, espace_between_cond_start, condWstart, condHstart
    # reinit de toutes les variables de jeu

    nb_tour = 0

    espace_between_cond_start = int(surfaceH/2)

    # dimension condom at start
    condWstart = int(surfaceW/32)
    condHstart = int(surfaceH/12)

    # init of speed (of condoms) variable
    speed = 1.5
    x_zoid = surfaceW / 2 - surfaceW / 3
    y_zoid = surfaceH / 2 - surfaceH / 8

    touch_down = False

    global current_max_score

    while(not touch_down):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    current_max_score = read_score()
                    
                    touch_down = True

                    surface.fill(base_color)
                    pygame.display.update()

                    pygame.mixer.music.load("data\sounds\zozoide_song.mp3")
                    pygame.mixer.music.play()
                    
                    break

                if event.key == pygame.K_m:
                    touch_down = True
                    global is_menu, rematch
                    is_menu = True
                    rematch = True
                    display_menu()
                    pygame.mouse.set_visible(False)
                    current_max_score = read_score()
                    break


                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                    break

def victoire():

    surface.fill(base_color)
    msgSurface("Victoire!")


def gameOver():

    pygame.mixer.music.load("data\sounds\game_over_sound.wav")
    pygame.mixer.music.play()

    surface.fill(base_color)
    if (y_zoid < -50):
        surface.blit(zoid_dead, (x_zoid, y_zoid+20))
    elif (y_zoid > surfaceH - 100):
        surface.blit(zoid_dead, (x_zoid, y_zoid -30))
    else :
        surface.blit(zoid_dead, (x_zoid, y_zoid))
    msgSurface("Splash!")


def defaite():
    surface.fill(base_color)
    msgSurface("Defaite!")



# put condom images on the font
def condoms(i_u, i_d, x_cond_d, y_cond_d, x_cond_u, y_cond_u):

    surface.blit(lcond_d[i_d], (x_cond_d, y_cond_d))
    surface.blit(lcond_u[i_u], (x_cond_u, y_cond_u))


# DEBUT DE LEXECUTION DU JEU

# on commence par afficher le menu
display_menu()

pygame.mouse.set_visible(False)

# on gere le fichier des scores avec le nom entre par le user
# le fichier est organisé comme suit :

# Name1 : Name1, Facile : meilleur_score_facile (-1 si pas tenté), Moyen : meilleur_score_moyen, Difficile : meilleur_score_difficile, Impossible : meilleur_score_impossible

def update_score():
    with open("data\scores\scores.txt", 'a+') as score:
        if (player_name != ""):  # l'utilisateur a entré un nom

            if(os.path.getsize("data\scores\scores.txt") == 0): # fichier vide

                score.write("Name : " + player_name + ", ")
                if (diff == 1):
                    score.write("Facile : " + str(nb_tour) + " ")
                else:
                    score.write("Facile : 0 ")
                if (diff == 2):
                    score.write("Moyen : " + str(nb_tour) + " ")
                else:
                    score.write("Moyen : 0 ")
                if (diff == 3):
                    score.write("Difficile : " + str(nb_tour) + " ")
                else:
                    score.write("Difficile : 0 ")
                if (diff == 4):
                    score.write("Impossible : " + str(nb_tour) + " \n")
                else:
                    score.write("Impossible : 0 \n")

            else : # fichier non vide
                # on cherche si le nom entré existe déjà dans le fichier
                score.seek(0,0)
                lines = score.readlines()
                to_seek = "Name : "+player_name+", "
                file_content = ""
                nom_trouve = False

                # on cherche si le nom existe
                for line in lines:
                    if (to_seek in line): # le nom existe déjà
                        val_scores = [int(d) for d in line.split() if d.isdigit()]
                        nom_trouve = True
                        if (diff == 1):
                            if (val_scores[0] < nb_tour):
                                line = line.replace("Facile : "+str(val_scores[0]), "Facile : "+str(nb_tour))
                        elif (diff == 2):
                            if (val_scores[1] < nb_tour):
                                line = line.replace("Moyen : "+str(val_scores[1]), "Moyen : "+str(nb_tour))
                        elif (diff == 3):
                            if (val_scores[2] < nb_tour):
                                line = line.replace("Difficile : "+str(val_scores[2]), "Difficile : "+str(nb_tour))
                        elif (diff == 4):
                            if (val_scores[3] < nb_tour):
                                line = line.replace("Impossible : "+str(val_scores[3]), "Impossible : "+str(nb_tour))

                    file_content = file_content + line

                if (not nom_trouve):
                    # le nom n'existe pas : on l'ajoute à la fin, avec le score
                    score.seek(0, 2)
                    score.write("Name : " + player_name + ", ")
                    if (diff == 1):
                        score.write("Facile : "+str(nb_tour)+" ")
                    else:
                        score.write("Facile : 0 ")
                    if (diff == 2):
                        score.write("Moyen : "+str(nb_tour)+" ")
                    else:
                        score.write("Moyen : 0 ")
                    if (diff == 3):
                        score.write("Difficile : "+str(nb_tour)+" ")
                    else:
                        score.write("Difficile : 0 ")
                    if (diff == 4):
                        score.write("Impossible : "+str(nb_tour)+" \n")
                    else:
                        score.write("Impossible : 0 \n")

                else: # le nom a ete trouve
                    score.truncate(0)
                    score.write(file_content)


def read_score():
    with open("data\scores\scores.txt", 'a+') as score:
        score.seek(0, 0)
        lines = score.readlines()
        to_seek = "Name : " + player_name + ", "

        # on cherche si le nom existe
        for line in lines:
            if (to_seek in line):  # le joueur existe
                val_scores = [int(d) for d in line.split() if d.isdigit()]
                return val_scores[diff-1]
        # le joueur n'existe pas : le max score est 0 pour l'instant
        return 0


# maintenant que les variables de jeu ont ete set, on construit la liste des obstacles

# images creating, loading and storing
zoid = pygame.image.load('data\images\spermat5.jpg').convert()
zoid = pygame.transform.scale(zoid, (zoidW, zoidH))

x_zoid = surfaceW/2 - surfaceW/3
y_zoid = surfaceH/2 - surfaceH/8

lcond_u = []
lcond_d = []
lcond_sizes = []

cond_u_img = pygame.image.load('data\images\condom_up.jpg').convert()
cond_d_img = pygame.image.load('data\images\condom_down.jpg').convert()

ovule_img = pygame.image.load('data\images\ovule.jpg').convert()
ovule = pygame.transform.scale(ovule_img, (surfaceW, surfaceH))

for i in range(nb_tour_max):
    cond_d = pygame.transform.scale(cond_d_img, (condWstart+5*i, condHstart+15*i))
    cond_u = pygame.transform.scale(cond_u_img, (condWstart+5*i, condHstart+15*i))
    lcond_u = lcond_u + [cond_u]
    lcond_d = lcond_d + [cond_d]
    lcond_sizes = lcond_sizes + [[condWstart+5*i, condHstart+15*i]]

zoid_dead = pygame.image.load('data\images\sperm_dead.jpg').convert()
zoid_dead = pygame.transform.scale(zoid_dead, (zoidW, zoidH))

# creating base font of the game
surface_init()

msgAccueil("Utilise les flèches Haut et Bas pour déplacer le spermatozoide !")
time.sleep(2)

current_max_score = read_score()

pygame.mixer.music.load("data\sounds\zozoide_song.mp3")
pygame.mixer.music.play()

pygame.mouse.set_visible(False)

# boucle principale
while (not game_finished):

    # on recree la liste des preservatifs si le joueur change de niveau
    if rematch:
        rematch = False
        if difficulty_changed:
            lcond_u = []
            lcond_d = []
            lcond_sizes = []
            for i in range(nb_tour_max):
                cond_d = pygame.transform.scale(cond_d_img, (condWstart + 5 * i, condHstart + 15 * i))
                cond_u = pygame.transform.scale(cond_u_img, (condWstart + 5 * i, condHstart + 15 * i))
                lcond_u = lcond_u + [cond_u]
                lcond_d = lcond_d + [cond_d]
                lcond_sizes = lcond_sizes + [[condWstart + 5 * i, condHstart + 15 * i]]

        pygame.mixer.music.load("data\sounds\zozoide_song.mp3")
        pygame.mixer.music.play()

    for j in range(nb_tour_max):

        if rematch:
            break

        decalage = random.randint(0, int(surfaceW/3))

        top_bot_mid = random.randint(0, 2)
        i_cond_d = -1
        i_cond_u = -1

        # TODO : ajouter un niveau "IMPOSSIBLE"
        # le spermatozoide doit passer en bas
        if (top_bot_mid == 0):
            i_cond_u = random.randint(int(4*nb_tour_max/5), nb_tour_max - 1)
            i_cond_d = random.randint(0, int(nb_tour_max/3))
        # le spermatozoide doit passer au milieu
        elif (top_bot_mid == 1):
            i_cond_u = random.randint(int(nb_tour_max/3), int(2*nb_tour_max/3))
            i_cond_d = random.randint(int(nb_tour_max/3), int(2*nb_tour_max/3))
        # le spermatozoide doit passer en haut
        elif (top_bot_mid == 2):
            i_cond_d = random.randint(int(4*nb_tour_max/5), nb_tour_max - 1)
            i_cond_u = random.randint(0, int(nb_tour_max/3))


        if ((decalage % 2) == 0):
            x_cond_d = surfaceW - lcond_sizes[i_cond_d][0] - decalage
            x_cond_u = surfaceW - lcond_sizes[i_cond_u][0]
        else:
            x_cond_u = surfaceW - lcond_sizes[i_cond_u][0] - decalage
            x_cond_d = surfaceW - lcond_sizes[i_cond_d][0]

        y_cond_d = 0
        y_cond_u = surfaceH - lcond_sizes[i_cond_u][1]

        nb_tour += 1
        speed += 0.15

        # add ovule at the end (nb_tour = nb_tour_max)
        if (nb_tour == nb_tour_max):
            surface.fill(base_color)
            surface.blit(zoid, (x_zoid, y_zoid))
            x_ov = surfaceW
            y_ov = 0
            surface.blit(ovule, (x_ov, y_ov))

            pygame.mixer.music.load("data\\sounds\\victory_sound.wav")
            pygame.mixer.music.play()
            while (x_ov > 0):
                surface.blit(ovule, (x_ov, y_ov))
                pygame.display.flip()
                x_ov -= 1
            victoire()
            break

        while (x_cond_u > 0 or x_cond_d > 0):

            y_move_zoid = 0

            surface.fill(base_color)
            surface.blit(zoid, (x_zoid, y_zoid))
            condoms(i_cond_u, i_cond_d, x_cond_d, y_cond_d, x_cond_u, y_cond_u)
            display_score()
            pygame.display.flip()

            x_cond_d -= speed
            x_cond_u -= speed

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        y_move_zoid = -20
                    if event.key == pygame.K_DOWN:
                        y_move_zoid = 20

            y_zoid = y_zoid + y_move_zoid


            # gestion collisions spermatozoide/preservatifs

            # collision avec les bords de la fenetre
            if (y_zoid < -20 or y_zoid+zoidH-50 > surfaceH):
                gameOver()
                break

            # collision avec le preservatif du haut
            if ((y_zoid + 20 < lcond_sizes[i_cond_d][1]) and (x_zoid+zoidW-20 > x_cond_d)):
                if (x_zoid < x_cond_d + lcond_sizes[i_cond_d][0]):
                    gameOver()
                    break

            # collision avec le preservatif du bas
            if ((y_zoid+zoidH-20 > surfaceH - lcond_sizes[i_cond_u][1]) and (x_zoid+zoidW+20 > x_cond_u)):
                if (x_zoid < x_cond_u + lcond_sizes[i_cond_u][0]):
                    gameOver()
                    break

pygame.quit()
quit()
