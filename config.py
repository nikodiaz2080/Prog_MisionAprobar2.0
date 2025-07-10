import pygame
import sys
import configparser

from assets import get_parametro, get_imagen, dibujar_texto
from audio import sfx, actualizar_volumen

NEGRO  = get_parametro("Colores", "Negro", tuple)
BLANCO = get_parametro("Colores", "Blanco", tuple)
AZUL   = get_parametro("Colores", "Azul", tuple)

ANCHO = get_parametro("General", "Resolucion", tuple)[0]
ALTO = get_parametro("General", "Resolucion", tuple)[1]

ESCALAR = (ANCHO + ALTO) / 2

config_items = [
    ("Juego", "Modo_Juego", str, ["Endless", "Por Preguntas", "Por Puntaje"]),
    ("Juego", "Dificultad", str, ["Facil", "Medio", "Dificil"]),
    ("Juego", "Tiempo_General", str, ["Si", "No"]),
    ("Audio", "Vol._Maestro", float, 0.1),
    ("Audio", "Vol._Musica", float, 0.1),
    ("Audio", "Vol._Efectos", float, 0.1)
]

def cambiar_opcion(valor_actual, opciones, direccion):
    indice = opciones.index(valor_actual)
    indice = (indice + direccion) % len(opciones)
    return opciones[indice]

def dibujar_configuraciones(pantalla, fuente, clock, fps):
    img_fondo = get_imagen("recursos/config_fondo.png", (get_parametro("General", "Resolucion", tuple)))
    img_boton = get_imagen("recursos/boton.png", (ESCALAR*.50, ESCALAR*.10))
    boton_ancho, boton_alto = img_boton.get_size()
    
    seleccion = 0
    valores   = {}
    config    = configparser.ConfigParser()
    config.read("settings.ini")

    for seccion, clave, tipo, paso in config_items:
        valor = get_parametro(seccion, clave, tipo)
        valores[(seccion, clave)] = valor

    ANCHO, ALTO = pantalla.get_size()

    while True:
        pantalla.blit(img_fondo, (0, 0))
        for evento in pygame.event.get():
            match evento.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                case pygame.KEYDOWN:
                    match evento.key:
                        case pygame.K_UP:
                            sfx("boton")
                            seleccion = (seleccion - 1) % len(config_items)
                        case pygame.K_DOWN:
                            sfx("boton")
                            seleccion = (seleccion + 1) % len(config_items)
                        case pygame.K_LEFT | pygame.K_RIGHT:
                            sfx("campana")
                            seccion, clave, tipo, control = config_items[seleccion]
                            valor_actual = valores[(seccion, clave)]
                            if tipo is float:
                                direccion = -1 if evento.key == pygame.K_LEFT else 1
                                valor_actual = valor_actual + (direccion * control)
                                valor_actual = round(min(1.0, max(0.0, valor_actual)), 2)
                            else:
                                direccion = -1 if evento.key == pygame.K_LEFT else 1
                                valor_actual = cambiar_opcion(valor_actual, control, direccion)
                            valores[(seccion, clave)] = valor_actual

                        case pygame.K_ESCAPE:
                            for (seccion, clave), valor in valores.items():
                                config[seccion][clave] = str(valor)
                            with open("settings.ini", "w") as file:
                                config.write(file)
                            return

        master = valores[("Audio", "Vol._Maestro")]
        music  = valores[("Audio", "Vol._Musica")]
        sfxvol = valores[("Audio", "Vol._Efectos")]
        actualizar_volumen(master, music, sfxvol)

        for i, (seccion, clave, tipo, _) in enumerate(config_items):
            valor_campo = valores[(seccion, clave)]
            if tipo is float:
                valor_campo = f"{int(float(valor_campo)*100)}%"
            texto = f"{clave.replace('_', ' ')}: {valor_campo}"

            x = (ANCHO - boton_ancho) // 2
            y = ALTO // 7 + i * (boton_alto + 20)

            color = AZUL if i == seleccion else BLANCO

            pantalla.blit(img_boton, (x, y))
            rect_texto = fuente.get_rect(texto)
            text_x = x + (boton_ancho // 2) - rect_texto.width // 2
            text_y = y + (boton_alto // 2) - rect_texto.height // 2
            dibujar_texto(pantalla, text_x, text_y, texto, fuente, color, NEGRO)

        instrucciones = ["ESC: Guardar y Salir", "Izq/Der: Cambiar", "Arriba/Abajo: Navegar"]
        for i, texto in enumerate(instrucciones):
            dibujar_texto(pantalla, 40, ALTO - 50 * (i + 1), texto, fuente, BLANCO, NEGRO)

        pygame.display.flip()
        clock.tick(fps)
