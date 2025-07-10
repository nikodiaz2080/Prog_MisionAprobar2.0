import pygame

from assets import get_imagen, get_parametro, dibujar_texto
from eventos import monitorear_eventos

AZUL = get_parametro("Colores", "Azul", tuple)
BLANCO = get_parametro("Colores", "Blanco", tuple)
NEGRO = get_parametro("Colores", "Negro", tuple)

ANCHO = get_parametro("General", "Resolucion", tuple)[0]
ALTO = get_parametro("General", "Resolucion", tuple)[1]

ESCALAR = (ANCHO + ALTO) / 2

def dibujar_menu(pantalla, fuente, clock, fps):
    img_fondo = get_imagen("recursos/menu_fondo.png", get_parametro("General", "Resolucion", tuple))
    img_boton = get_imagen("recursos/boton.png", (ESCALAR*.40, ESCALAR*.10))
    img_circulo = get_imagen("recursos/rueda1.png", (ESCALAR*.30, ESCALAR*.30))
    img_centro  = get_imagen("recursos/rueda2.png", (ESCALAR*.25, ESCALAR*.25))

    boton_ancho, boton_alto = img_boton.get_size()

    opciones = ["JUGAR", "TOP 10", "AJUSTES", "SALIR"]
    opcion_seleccionada = 0
    rects_opciones = []
    angulo = 0
    
    while True:
        pantalla.blit(img_fondo, (0, 0))
        opcion_seleccionada, accion = monitorear_eventos(opciones, opcion_seleccionada, rects_opciones, False)

        if accion:
            return accion
    
        rects_opciones.clear()
        for i, opcion in enumerate(opciones):
            x = (ANCHO - boton_ancho) // 2
            y = ALTO // 2.5 + i * (boton_alto + 20)
            
            color = AZUL if i == opcion_seleccionada else BLANCO
            rect_texto = fuente.get_rect(opcion)

            text_x = x + (boton_ancho // 2) - rect_texto.width // 2
            text_y = y + (boton_alto // 2) - rect_texto.height // 2

            pantalla.blit(img_boton, (x, y))
            dibujar_texto(pantalla, text_x, text_y, opcion, fuente, color, NEGRO)

            rects_opciones.append(pygame.Rect(x, y, boton_ancho, boton_alto))
        
        centro = (ANCHO // 2, ALTO // 5)
        angulo = animar_circulo(pantalla, angulo, img_circulo, img_centro, centro)

        pygame.display.flip()
        clock.tick(fps)

def animar_circulo(pantalla, angulo, img_circulo, img_centro, centro, velocidad=0.5):
    # Rotar la imagen del círculo y centrarla
    circulo_rotado = pygame.transform.rotate(img_circulo, angulo)
    rect_circulo = circulo_rotado.get_rect(center=centro)
    pantalla.blit(circulo_rotado, rect_circulo)

    # Dibujar la imagen central encima
    rect_centro = img_centro.get_rect(center=centro)
    pantalla.blit(img_centro, rect_centro)

    # Actualizar ángulo
    return (angulo + velocidad) % 360
