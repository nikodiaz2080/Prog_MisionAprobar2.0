import pygame
from assets import cargar_imagen
import sys

ANCHO = 400
ALTO = 800

FPS = 60

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 120, 215)


def configuracion(pantalla):
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Comic Sans MS", 16, bold=True)

    fondo = cargar_imagen("recursos/fondo.png", (ANCHO, ALTO))

    volumen = pygame.mixer.music.get_volume()  # entre 0.0 y 1.0
    porcentaje = int(volumen * 100)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return  # volver al menú
                elif evento.key == pygame.K_UP:
                    if porcentaje < 100:
                       porcentaje += 10
                       pygame.mixer.music.set_volume(porcentaje / 100)
                elif evento.key == pygame.K_DOWN:
                    if porcentaje > 0:
                       porcentaje -= 10
                       pygame.mixer.music.set_volume(porcentaje / 100)

        pantalla.blit(fondo, (0, 0))
        texto = fuente.render("Pantalla de Configuración (ESC para volver)", True, BLANCO)
        rect1 = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        pantalla.blit(texto, rect1)

        vol_texto = fuente.render(f"Volumen: {porcentaje}%", True, BLANCO)
        rect2 = vol_texto.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
        pantalla.blit(vol_texto, rect2)

        pygame.display.flip()
        reloj.tick(FPS)