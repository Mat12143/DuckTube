# -------------------------------------------------------------- #
# Import
# -------------------------------------------------------------- #
import pyperclip
from threading import Thread
import pygame
from pygame.locals import *
import pytube
from moviepy import *
import os
from pathlib import Path
import urllib.request
from moviepy.video.io.VideoFileClip import VideoFileClip


# -------------------------------------------------------------- #
# Inizializzazione
# -------------------------------------------------------------- #
pygame.init()
pygame.font.init()

# -------------------------------------------------------------- #
# Primo Step Funzione
# -------------------------------------------------------------- #

def primo_step():
    global link, continua

    # Controlla la correttezza del link
    def link_check():
        global link, continua
        if link == "":
            link = "Niente da incollare!"
        elif link.find("https://www.youtube.com/watch?v=") == -1:
            link = "Link non valido! Prova con un altro"
        elif len(link) > 43:
            link = "Link troppo lungo!"
        else:
            continua = True

    crediti_page = pygame.image.load("./.data/img/credits.png")

    pygame.display.set_caption("DuckTube - Inserire il Link")

    sfondo = pygame.image.load("./.data/img/punto_1.png")

    font = pygame.font.Font("./.data/font/font.ttf", 18)

    incolla_img = pygame.image.load("./.data/img/incolla.png")

    continua_disabled = pygame.image.load("./.data/img/prossimo_disabled.png")
    continua_enabled = pygame.image.load("./.data/img/prossimo_enabled.png")

    mainLoop = True # per tenere la finestra aperta
    crediti = False # Per aprire il Pop-Up dei Crediti
    incolla = False # Per aprire il Pop-Up di Incolla
    continua = False
    link = "(Premi Ctrl + V o Premi il tasto destro per incollare)"  # il link
    screen = pygame.display.set_mode((960, 540), 0,0) # lo schermo

    while mainLoop:

        screen.blit(sfondo, (0,0))
        screen.blit(font.render(link, True, (150,150,150)), (165, 210))

        # stampo la pagina dei crediti se la variabile è True
        if crediti:
            screen.blit(crediti_page, (0,0))
            pygame.display.update()

        if continua:
            screen.blit(continua_enabled, (682, 200))
        else:
            screen.blit(continua_disabled, (682, 200))

        # Stampo la pop-up di incolla se la variabile è True
        if incolla:
            screen.blit(incolla_img, (incolla_x, incolla_y))

        events = pygame.event.get()
        for event in events:
            
            # Quit event
            if event.type == pygame.QUIT:
                mainLoop = False
            
            # Controllo se premo il mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:

                mx , my = pygame.mouse.get_pos()
   
                
                # Se premo il tasto sinistro
                if event.button == 1:
                    
                    # Se clicco sul pop-up allora incolla
                    if (incolla == True and (mx > incolla_x and my > incolla_y) and (mx < incolla_x + 160 and my < incolla_y + 35)):
                        incolla = False
                        link = pyperclip.paste()
                        link_check()
                    
                    # Se clicco fuori togli il pop-up di Incolla
                    if not ((mx > 150 and my > 205) and (mx < 676 and my < 250)):
                        incolla = False

                    # Pop-Up crediti zone
                    if crediti == False:
                        if (mx > 10 and my > 11) and (mx < 46 and my < 47):
                            crediti = True
                            pygame.display.set_caption("DuckTube - Crediti")

                    elif ((mx > 10 and my > 11) and (mx < 46 and my < 47) and crediti == True):
                        crediti = False
                        pygame.display.set_caption("DuckTube - Inserire il Link")

                    if continua:
                        if (mx > 682 and my > 200) and (mx < 815 and my < 245):
                            print("Cercando il file ...")
                            continua = False
                            mainLoop = False
                            secondo_step()

                # Controllo se sono nella barra e se premi tasto destro e mi preparo per far comparire il pop-up
                if event.button == 3:
                    if (mx > 150 and my > 205) and (mx < 676 and my < 250):
                        incolla = True
                        incolla_x, incolla_y = mx, my   

            # Se invece premo un tasto   
            elif event.type == pygame.KEYDOWN:

                key = pygame.key.get_pressed()

                # CTRL + V Check
                if key[pygame.K_LCTRL]:
                    if key[pygame.K_v]:
                        link = pyperclip.paste()
                        incolla = False
                        link_check()

        pygame.display.update()

def secondo_step():
    global formato

    pygame.init()
    pygame.font.init()
   
    screen = pygame.display.set_mode((960, 540), 0,0)
    pygame.display.set_caption("DuckTube - Seleziona il Formato")

    mainLoop = True
    crediti = False
    formato = ""
    continua = False

    sfondo = pygame.image.load("./.data/img/punto_2.png")
    crediti_page = pygame.image.load("./.data/img/credits.png")

    continua_disabled = pygame.image.load("./.data/img/prossimo_disabled.png")
    continua_enabled = pygame.image.load("./.data/img/prossimo_enabled.png")

    selected = pygame.image.load("./.data/img/selected.png")

    while mainLoop:
        
        
        screen.blit(sfondo, (0,0))

        if crediti:
            screen.blit(crediti_page, (0,0))

        if continua == False:
            screen.blit(continua_disabled, (414, 331))
        else:
            screen.blit(continua_enabled, (414, 331))

        if formato == "mp3":
            screen.blit(selected, (346, 179))
        elif formato == "mp4":
            screen.blit(selected, (510, 179))

        events = pygame.event.get()
        for event in events:
            
            # Quit event
            if event.type == pygame.QUIT:
                mainLoop = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx , my = pygame.mouse.get_pos()

                if event.button == 1:

                    if crediti == False:
                        if (mx > 10 and my > 11) and (mx < 46 and my < 47):
                            crediti = True
                            pygame.display.set_caption("DuckTube - Crediti")

                    elif ((mx > 10 and my > 11) and (mx < 46 and my < 47) and crediti == True):
                        crediti = False
                        pygame.display.set_caption("DuckTube - Inserire il Link")
                    
                    if continua:
                        if (mx > 414 and my > 331) and (mx < 547 and my < 377):
                            continua = False
                            mainLoop = False
                            terzo_step()
                    
                    if (mx > 330 and my > 180) and (mx < 463 and my < 302):
                        formato = "mp3"
                        continua = True
                    
                    if (mx > 515 and my > 180) and (mx < 648 and my < 302):
                        formato = "mp4"
                        continua = True

        pygame.display.update()


def terzo_step():

    global link, formato, errori, converto, errori_sistema, errore_testo, errore_internet

    screen = pygame.display.set_mode((960, 540), 0,0)
    pygame.display.set_caption("DuckTube - Scaricamento")

    sfondo = pygame.image.load("./.data/img/punto_3.png")
    crediti_page = pygame.image.load("./.data/img/credits.png")

    scaricamento_testo = pygame.image.load("./.data/img/scaricamento.png")
    fine_testo = pygame.image.load("./.data/img/file_fatto.png")
    bottoni =  pygame.image.load("./.data/img/punto_3_button.png")

    errore_testo = pygame.image.load("./.data/img/errore_testo.png")
    bottone_home = pygame.image.load("./.data/img/errore_button.png")

    loading_image = pygame.image.load("./.data/img/loading.png")

    mainLoop = True
    crediti = False
    errori = False
    converto = False
    errori_sistema = False
    errore_internet = False
    finito = False

    loading_rotation = 0

    thread1 = Thread(target=scarica, args=(link, formato))
    thread1.start()

    while mainLoop:

        if finito:
            screen.blit(pygame.image.load("./.data/img/fine.png"), (0,0))
        else:
            screen.blit(sfondo, (0,0))

        if crediti:
            screen.blit(crediti_page, (0,0))

        events = pygame.event.get()
        for event in events:
                
            # Quit event
            if event.type == pygame.QUIT:
                mainLoop = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx , my = pygame.mouse.get_pos()
    
                if event.button == 1:

                    if crediti == False:
                        if (mx > 10 and my > 11) and (mx < 46 and my < 47):
                            crediti = True
                            pygame.display.set_caption("DuckTube - Crediti")

                    elif ((mx > 10 and my > 11) and (mx < 46 and my < 47) and crediti == True):
                        crediti = False
                        pygame.display.set_caption("DuckTube - Scaricamento")

                    if errori == False:
                        if (mx > 337 and my > 281) and (mx < 450 and my < 355):
                            path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
                            os.system("C:\\Windows\\explorer.exe /n, /e, " + path_to_download_folder)

                        elif (mx > 510 and my > 281) and (mx < 583 and my < 355):
                            homePage()
                            mainLoop = False
                    
                    if (errore_internet == True or errori_sistema == True or errori == True):
                        if (mx > 444 and my > 276) and (mx < 517 and my < 350):
                            homePage()
                            mainLoop = False
                            

        alive = thread1.is_alive()

        if (alive == False and errori == False and errori_sistema == False and errore_internet == False):
            finito = True
            screen.blit(fine_testo, (248, 208))
            screen.blit(bottoni, (377, 289))
        elif errore_internet == True:
            screen.blit(pygame.image.load("./.data/img/no_internet.png"), (300, 190))
            screen.blit(bottone_home, (444, 276))
        elif errori_sistema:
            text = pygame.font.Font("./.data/font/font.ttf", 18).render(str("Errore: " + str(errore_testo)), True, (0,0,0))
            posizione = text.get_rect(center=(960/2, 400/2))
            screen.blit(text, posizione)
            screen.blit(bottone_home, (444, 276))
        elif converto:
            loading_rotation -= 3
            loading_image_rotated = pygame.transform.rotate(loading_image, loading_rotation)
            new_rect = loading_image_rotated.get_rect(center = loading_image.get_rect(topleft = (444, 277)).center)
            screen.blit(loading_image_rotated, new_rect)
            screen.blit(pygame.image.load("./.data/img/mp3_convert.png"), (294, 213))
        else:
            loading_rotation -= 3
            loading_image_rotated = pygame.transform.rotate(loading_image, loading_rotation)
            new_rect = loading_image_rotated.get_rect(center = loading_image.get_rect(topleft = (444, 277)).center)
            screen.blit(loading_image_rotated, new_rect.topleft)
            screen.blit(scaricamento_testo, (295, 208))

        pygame.display.flip()


# -------------------------------------------------------------- #
# Codice per scaricare il video
# -------------------------------------------------------------- #

def scarica(link, formato):

    global converto, errori_sistema, errore_testo, errore_internet

    try:
        urllib.request.urlopen("http://google.com")
    except:
        errore_internet = True
    else:
        
        path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))

        try:
            video = pytube.YouTube(str(link)).streams.first()
        except Exception as e:
            errori_sistema = True
            errore_testo = str(e)
        
        except Exception as e:
            errori_sistema = True
            errore_testo = str(e)
        else:
            print("Video Trovato!")
            titolo = video.title

            titolo_finito = ""

            for character in titolo:

                if character.isalnum():

                    titolo_finito += character
                
                else:
                    titolo_finito += " "

            try:
                video.download(path_to_download_folder, str(titolo_finito))
            except Exception as e:
                errore_testo = e
                errori_sistema = True

            if formato == "mp3":

                converto = True

                path_mp4 =  os.path.join(path_to_download_folder, titolo_finito + '.mp4')
                path_mp3 =  path_to_download_folder + '\\' + titolo_finito + '.mp3'

                print("Converto in mp3 ...")
                
                video = VideoFileClip(path_mp4)

                audio = video.audio
                audio.write_audiofile(path_mp3)
                audio.close()
                video.close()
                os.remove(path_mp4)


            
def homePage():

    screen = pygame.display.set_mode((960, 540), 0,0)
    pygame.display.set_caption("DuckTube - HomePage")

    home = pygame.image.load("./.data/img/home.png")
    crediti_page = pygame.image.load("./.data/img/credits.png")

    font = pygame.font.Font("./.data/font/font.ttf", 100)

    mainLoop = True
    crediti = False
    easter = 0

    while mainLoop:

        screen.blit(home, (0,0))

        if crediti:
            screen.blit(crediti_page, (0,0))
            screen.blit(font.render(str(lingua[0]), True, (0,0,0)), (940,520))
            pygame.display.update()

        events = pygame.event.get()
        for event in events:
            
            # Quit event
            if event.type == pygame.QUIT:
                mainLoop = False
            
            # Controllo se premo il mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:

                mx , my = pygame.mouse.get_pos()

                # Se non ho i crediti chiusi, aprili 
                if crediti == False:
                    if (mx > 10 and my > 11) and (mx < 46 and my < 47):
                        crediti = True
                        pygame.display.set_caption("DuckTube - Crediti")

                # Se ho i crediti aperti, chiudili 
                elif crediti == True:
                    if (mx > 10 and my > 11) and (mx < 46 and my < 47):
                        crediti = False
                        pygame.display.set_caption("DuckTube - HomePage")

                if easter < 10:
                    if (mx > 880 and my > 30) and (mx < 915 and my < 70):
                        easter += 1

                elif easter == 10:
                    print("EASTER EGG trovato!!!")

                elif crediti == False:
                    pass
                
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    mainLoop = False
                    primo_step()

        pygame.display.update()