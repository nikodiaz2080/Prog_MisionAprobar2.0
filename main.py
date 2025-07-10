import pygame
import pygame.freetype
import sys

from assets import get_imagen, get_parametro
from audio import cargar_sonidos, sfx
from menu import dibujar_menu
from jugar import jugar
from partidas_top import mostrar_top10
from config import dibujar_configuraciones

def main():
    pygame.init()
    pygame.freetype.init()

    pantalla = pygame.display.set_mode(get_parametro("General", "Resolucion", tuple))
    fuente = pygame.freetype.Font("recursos/fuente.ttf", get_parametro("General", "Tam_Letra", int))
    clock = pygame.time.Clock()
    fps = get_parametro("General", "Fps", int)

    pygame.display.set_caption("Preguntados")
    pygame.display.set_icon(get_imagen("recursos/icono.png"))
    cargar_sonidos()

    while True:
        opcion = dibujar_menu(pantalla, fuente, clock, fps)
        sfx("campana")
        match opcion:
            case "JUGAR":
                jugar(pantalla, fuente, clock, fps)
            case "TOP 10":
                mostrar_top10(pantalla, fuente, clock, fps)
            case "AJUSTES":
                dibujar_configuraciones(pantalla, fuente, clock, fps)
            case "SALIR":
                pygame.quit()
                sys.exit()
            case _:
                raise ValueError("Opcion de menu no existe")
        clock.tick(fps)

if __name__ == "__main__":
    main()