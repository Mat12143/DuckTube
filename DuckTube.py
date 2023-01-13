# DuckTube simple YT GUI Downloader 
# By Mat12143 and JackSP_

# Import modules
import pygame, json
from script.avvio_app import primo_step
import webbrowser

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Pygame screen settings
screen = pygame.display.set_mode((960, 540), 0,0)
pygame.display.set_caption("DuckTube - HomePage")

errore_file = False

# Controllo file
try:
    home = pygame.image.load("./.data/img/home.png")
    crediti_page = pygame.image.load("./.data/img/credits.png")
    font = pygame.font.Font("./.data/font/font.ttf", 100)
except FileNotFoundError:
    print("Errore! Mancano dei file!")
    errore_file = True
except Exception as e:
    print("Errore! " + str(e))
    errore_file = True

mainLoop = True
crediti = False
easter = 0

if errore_file == False:
    
    while mainLoop:
        # Mostro la home
        screen.blit(home, (0,0))

        if crediti:
            screen.blit(crediti_page, (0,0))
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

                if easter < 19:
                    if (mx > 370 and my > 56) and (mx < 550 and my < 266):
                        easter += 1

                if easter == 9:
                    pygame.mixer.music.load('./.data/sound/duck.mp3')
                    pygame.mixer.music.play(0)
                
                elif easter == 19:
                    webbrowser.open("https://www.youtube.com/watch?v=f2x4ZLYXp2I&t=15s")
                    easter = 0
                
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    mainLoop = False
                    primo_step()


        pygame.display.update()

