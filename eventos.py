import pygame
import sys

from audio import sfx

def monitorear_eventos(items, item_select, rects_items, permitir_escape=False):
    accion = None

    for evento in pygame.event.get():
        match evento.type:
            case pygame.QUIT:
                pygame.quit()
                sys.exit()

            case pygame.KEYDOWN:
                match evento.key:
                    case pygame.K_UP:
                        sfx("boton")
                        item_select = (item_select - 1) % len(items)
                    case pygame.K_DOWN:
                        sfx("boton")
                        item_select = (item_select + 1) % len(items)
                    case pygame.K_RETURN:
                        sfx("boton")
                        accion = items[item_select]
                    case key if pygame.K_1 <= key <= pygame.K_9:
                        sfx("boton")
                        index = key - pygame.K_1
                        if index < len(items):
                            accion = items[index]
                    case pygame.K_ESCAPE if permitir_escape:
                        accion = "Volver"

            case pygame.MOUSEMOTION:
                for i, rect in enumerate(rects_items):
                    if rect.collidepoint(evento.pos):
                        item_select = i

            case pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    for i, rect in enumerate(rects_items):
                        if rect.collidepoint(evento.pos):
                            sfx("boton")
                            accion = items[i]

    return item_select, accion
