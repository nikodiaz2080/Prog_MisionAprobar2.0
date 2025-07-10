import json
import pygame

from assets import get_parametro, get_imagen, dibujar_texto
from audio import sfx

NEGRO  = get_parametro("Colores", "Negro", tuple)
BLANCO = get_parametro("Colores", "Blanco", tuple)
AZUL   = get_parametro("Colores", "Azul", tuple)

ANCHO, ALTO = get_parametro("General", "Resolucion", tuple)
ESCALAR = (ANCHO + ALTO) / 2

def cargar_partidas():
    try:
        with open("partidas.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return sorted(datos, key=lambda x: x["puntos"], reverse=True)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def mostrar_top10(pantalla, fuente, clock, fps):
    img_fondo = get_imagen("recursos/config_fondo.png", (ANCHO, ALTO))

    partidas = cargar_partidas()
    partidas = partidas[:10]
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    sfx("boton")
                    corriendo = False

        pantalla.blit(img_fondo, (0, 0))

        titulo = "TOP 10"
        rect_titulo = fuente.get_rect(titulo)
        x_titulo = (ANCHO - rect_titulo.width) // 2
        y_titulo = 50
        dibujar_texto(pantalla, x_titulo, y_titulo, titulo, fuente, AZUL, NEGRO)

        y_offset = y_titulo + rect_titulo.height + 40
        for i, partida in enumerate(partidas):
            texto = f"{i+1}. {partida['nombre']} - {partida['puntos']} pts - {partida['fecha']}"
            rect_texto = fuente.get_rect(texto)
            x_texto = (ANCHO - rect_texto.width) // 2
            dibujar_texto(pantalla, x_texto, y_offset, texto, fuente, BLANCO, NEGRO)
            y_offset += rect_texto.height + 10

        instrucciones = "ESC o ENTER para volver"
        rect_instr = fuente.get_rect(instrucciones)
        x_instr = (ANCHO - rect_instr.width) // 2
        dibujar_texto(pantalla, x_instr, ALTO - 50, instrucciones, fuente, BLANCO, NEGRO)

        pygame.display.flip()
        clock.tick(fps)
