import pygame
from assets import get_parametro

pygame.mixer.init()

MASTER_VOL = get_parametro("Audio", "Vol._Maestro", float)
MUSIC_VOL  = get_parametro("Audio", "Vol._Musica", float) * MASTER_VOL
SFX_VOL    = get_parametro("Audio", "Vol._Efectos", float) * MASTER_VOL

sonido_campana = None
sonido_alarma  = None
sonido_tictac  = None
sonido_boton   = None
sonido_bien    = None
sonido_mal     = None

def cargar_sonidos():
    global sonido_campana, sonido_alarma, sonido_tictac, sonido_boton, sonido_bien, sonido_mal
    pygame.mixer.music.set_volume(MUSIC_VOL)
    pygame.mixer.music.load("recursos/musica.ogg")
    pygame.mixer.music.play(-1)

    sonido_campana = pygame.mixer.Sound("recursos/campana.mp3")
    sonido_alarma  = pygame.mixer.Sound("recursos/alarma.mp3")
    sonido_tictac  = pygame.mixer.Sound("recursos/tictac.mp3")
    sonido_boton   = pygame.mixer.Sound("recursos/boton.mp3")
    sonido_bien    = pygame.mixer.Sound("recursos/bien.mp3")
    sonido_mal     = pygame.mixer.Sound("recursos/mal.mp3")

    sonido_campana.set_volume(SFX_VOL)
    sonido_alarma.set_volume(SFX_VOL)
    sonido_tictac.set_volume(SFX_VOL)
    sonido_boton.set_volume(SFX_VOL)
    sonido_bien.set_volume(SFX_VOL)
    sonido_mal.set_volume(SFX_VOL)

def actualizar_volumen(master, music, sfx):
    pygame.mixer.music.set_volume(music * master)
    sonido_campana.set_volume(sfx * master)
    sonido_alarma.set_volume(sfx * master)
    sonido_tictac.set_volume(sfx * master)
    sonido_boton.set_volume(sfx * master)
    sonido_bien.set_volume(sfx * master)
    sonido_mal.set_volume(sfx * master)

def sfx(nombre: str):
    match nombre:
        case "campana":
            sonido_campana.play()
        case "alarma":
            sonido_alarma.play()
        case "tictac":
            sonido_tictac.play()
        case "boton":
            sonido_boton.play()
        case "bien":
            sonido_bien.play()
        case "mal":
            sonido_mal.play()
        case _:
            print(f"Sonido {nombre} no existe")
