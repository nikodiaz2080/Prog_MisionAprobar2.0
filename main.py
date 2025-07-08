import pygame
import sys
#import json

from config import ANCHO, ALTO, FPS
from menu import mostrar_menu
from jugar import jugar
from jugar import mostrar_top10
from config import configuracion


pygame.init()
pygame.mixer.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Preguntados")

clock = pygame.time.Clock()

# bucle principal
while True:
    # mostrar_menu devuelve la opción elegida o None si aún no eligió
    opcion = mostrar_menu(pantalla)
    if opcion == "jugar":
        jugar(pantalla)

    elif opcion == "top10":
        mostrar_top10()
        input("Presione ENTER para continuar...")
    elif opcion == "configuracion":
         configuracion(pantalla)
        # abrir configuración
    elif opcion == "salir":
        pygame.quit()
        sys.exit()

    clock.tick(FPS)
