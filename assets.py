import pygame

def cargar_imagen(path, tam=None):
    img = pygame.image.load(path).convert_alpha()
    if tam:
        img = pygame.transform.smoothscale(img, tam)
    return img

def cargar_sonido(path):
    return pygame.mixer.Sound(path)
