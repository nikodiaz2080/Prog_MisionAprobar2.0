import pygame
import configparser

def get_parametro(seccion, clave, tipo):
    config = configparser.ConfigParser()
    config.read("settings.ini")
    
    if seccion not in config:
        raise ValueError(f"Seccion [{seccion}] no encontrada")
    if clave not in config[seccion]:
        raise ValueError(f"Clave '{clave}' no encontrada en [{seccion}]")
    
    parametro = config[seccion][clave]

    match tipo:
        case x if x is str:
            return parametro
        case x if x is int:
            return int(parametro)
        case x if x is float:
            return float(parametro)
        case x if x is tuple:
            return tuple(int(s.strip()) for s in parametro.split(","))
        case _:
            raise ValueError(f"Tipo de dato '{tipo}' no existe")

def get_imagen(ruta, resolucion=None):
    imagen = pygame.image.load(ruta).convert_alpha()
    if resolucion:
        imagen = pygame.transform.smoothscale(imagen, resolucion)
    return imagen

def dibujar_texto(pantalla, x, y, texto, fuente, color, borde, grosor=2):
    for dx in range(-grosor, grosor+1):
        for dy in range(-grosor, grosor+1):
            fuente.render_to(pantalla, (x+dx, y+dy), texto, borde)
    fuente.render_to(pantalla, (x, y), texto, color)
