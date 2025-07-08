import pygame
import sys

from config import ANCHO, ALTO, BLANCO, AZUL, FPS
from assets import cargar_imagen, cargar_sonido


def mostrar_menu(pantalla):
    fondo = cargar_imagen("recursos/fondo.png", (ANCHO, ALTO))
    icono = cargar_imagen("recursos/icono.png")
    pygame.display.set_icon(icono)

    imagen_boton = cargar_imagen("recursos/boton.png")
    boton_ancho, boton_alto = imagen_boton.get_size()

    img_circulo = cargar_imagen("recursos/rueda1.png", (200, 200))
    img_centro  = cargar_imagen("recursos/rueda2.png", (150, 150))

    # sonidos
    pygame.mixer.music.load("recursos/musica.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    sonido_boton = cargar_sonido("recursos/boton.mp3")

    # Fuente
    fuente = pygame.font.SysFont("Comic Sans MS", 32, bold=True)

    # Opciones del menú
    opciones = [("jugar", "Jugar"),
                ("top10", "Ver TOP 10"),
                ("configuracion", "Configuración"),
                ("salir", "Salir")]

    opcion_seleccionada = 0
    rects_opciones = []
    angulo = 0

    clock = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    sonido_boton.play()
                    return opciones[opcion_seleccionada][0]
            elif evento.type == pygame.MOUSEMOTION:
                pos = evento.pos
                for i, rect in enumerate(rects_opciones):
                    if rect.collidepoint(pos):
                        opcion_seleccionada = i
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    for i, rect in enumerate(rects_opciones):
                        if rect.collidepoint(evento.pos):
                            sonido_boton.play()
                            return opciones[i][0]

        pantalla.blit(fondo, (0, 0))
        rects_opciones.clear()

        # Animación superior
        angulo = animacion(pantalla, angulo, img_circulo, img_centro)

        # Dibujar botones con texto centrado
        for i, (clave, texto) in enumerate(opciones):
            x = (ANCHO - boton_ancho) // 2
            y = int(ALTO * 0.40) + i * (boton_alto + 30)

            color_texto = AZUL if i == opcion_seleccionada else BLANCO

            pantalla.blit(imagen_boton, (x, y))

            render = fuente.render(texto, True, color_texto)
            rect_texto = render.get_rect(center=(x + boton_ancho // 2, y + boton_alto // 2))
            pantalla.blit(render, rect_texto)

            rect_boton = pygame.Rect(x, y, boton_ancho, boton_alto)
            rects_opciones.append(rect_boton)

        pygame.display.flip()
        clock.tick(FPS)


def animacion(pantalla, angulo, img_circulo, img_centro):
    circulo_rotado = pygame.transform.rotate(img_circulo, angulo)
    rect_circulo = circulo_rotado.get_rect(center=(ANCHO // 2, ALTO // 5))
    pantalla.blit(circulo_rotado, rect_circulo)

    rect_centro = img_centro.get_rect(center=(ANCHO // 2, ALTO // 5))
    pantalla.blit(img_centro, rect_centro)

    return (angulo + 0.5) % 360
