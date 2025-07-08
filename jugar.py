import pygame # para gráficos, sonidos, eventos.
import sys #para cerrar el juego correctamente con sys.exit().
import csv #lee las preguntas
import random # para mezclar el orden de las preguntas y respuestas
import json
from datetime import datetime

from config import ANCHO, ALTO, BLANCO, AZUL, NEGRO, FPS
from assets import cargar_imagen, cargar_sonido 

def guardar_puntaje(nombre, puntos):
    try:
        with open("partidas.json", "r", encoding="utf-8") as archivo:
            lista = json.load(archivo)
    except:
        lista = []

    nueva_partida = {
        "nombre": nombre,
        "puntaje": puntos,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    lista.append(nueva_partida)

    with open("partidas.json", "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, indent=4)


def cargar_preguntas(csv_path): # Esta va a mezcla el orden de las opciones de una sola pregunta, para que no estén siempre en el mismo orden.
    preguntas = [] # Crea una lista vacía donde se van a guardar todas las preguntas del juego
    with open(csv_path, encoding="utf-8") as f: #Abre el archivo CSV que contiene las preguntas # with se cierra automáticamente después de usarlo #
        reader = csv.DictReader(f) # para leer el archivo CSV y convertir cada fila en un diccionario
        for row in reader: # Recorre cada fila del archivo como un diccionario
            opciones = [  #Crea una lista de opciones posibles para mostrar al jugardor. 3 incorrectas y una correcta.
                row["respuesta1"],
                row["respuesta2"],
                row["respuesta3"],
                row["respuesta_correcta"]
            ]
            preguntas.append({           #agrga u nuevo eleemnto alfianl del diccionario
                "pregunta": row["pregunta"],
                "opciones": opciones,
                "correcta": row["respuesta_correcta"],
                "dificultad": row["dificultad"]
            })
    random.shuffle(preguntas) # Revuelve la lista preguntas entera para que no aparezcan siempre en el mismo orden
    return preguntas #  Devuelve toda la lista lista preguntas al que la llamó.


def preparar_pregunta(pregunta): # 4 opciones de una pregunta mezcla el orden y muestra en pantalla
    opciones = pregunta["opciones"].copy() #accede a la lista de respuestas
    random.shuffle(opciones) #mezcla el orden
    return opciones # función devuelve la lista mezclada para usarla en el juego.


def jugar(pantalla):
    comodines = {"pasar": True}  # Solo uno por ahora
    clock = pygame.time.Clock()
    fuente = pygame.font.SysFont("Comic Sans MS", 16, bold=True)

    # cargar imágenes
    fondo = cargar_imagen("recursos/fondo.png", (ANCHO, ALTO))
    boton_img = cargar_imagen("recursos/boton.png")
    boton_ancho, boton_alto = boton_img.get_size()

    # cargar sonidos
    sonido_bien = cargar_sonido("recursos/bien.mp3")
    sonido_mal  = cargar_sonido("recursos/mal.mp3")

    preguntas = cargar_preguntas("preguntas.csv")
    pregunta_idx = 0
    puntaje = 0
    vidas = 3

    seleccionada = -1
    feedback = ""
    feedback_timer = 0

    # preparar primera pregunta
    pregunta = preguntas[pregunta_idx]
    opciones = preparar_pregunta(pregunta)
    correcta = pregunta["correcta"]

    while True:
        pantalla.blit(fondo, (0, 0))
        # Mostrar comodines disponibles
        txt_comodin = fuente.render(f"Pasar: {'Sí' if comodines['pasar'] else 'No'}", True, BLANCO)
        pantalla.blit(txt_comodin, (10, 40))
        rects_opciones = []

        if pregunta_idx >= len(preguntas) or vidas <= 0:
            # Fin del juego: pedir nombre y guardar puntaje
            nombre = ""
            escribiendo = True

            while escribiendo:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_RETURN and len(nombre) >= 3:
                            guardar_puntaje(nombre, puntaje)
                            escribiendo = False
                        elif evento.key == pygame.K_p and comodines["pasar"]:
                             pregunta_idx += 1
                             comodines["pasar"] = False
                             break
                        elif evento.key == pygame.K_BACKSPACE:
                            nombre = nombre[:-1]
                        elif evento.unicode.isalpha() and len(nombre) < 10:
                            nombre += evento.unicode

                pantalla.blit(fondo, (0, 0))
                texto = fuente.render(f"Ingrese su nombre: {nombre}", True, BLANCO)
                rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
                pantalla.blit(texto, rect)

                aviso = fuente.render("ENTER para guardar", True, AZUL)
                rect2 = aviso.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
                pantalla.blit(aviso, rect2)

                pygame.display.flip()
                clock.tick(FPS)

            return  # <--- este return SOLO se ejecuta al finalizar el juego

        # Mostrar puntaje y vidas
        txt_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        pantalla.blit(txt_puntaje, (10, 10))
        txt_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
        pantalla.blit(txt_vidas, (ANCHO - 150, 10))

        # Mostrar pregunta
        render = fuente.render(pregunta["pregunta"], True, BLANCO)
        rect = render.get_rect(center=(ANCHO//2, 100))
        pantalla.blit(render, rect)

        # Mostrar opciones con botones
        for i, texto in enumerate(opciones):
            x = (ANCHO - boton_ancho) // 2
            y = 200 + i * (boton_alto + 20)
            color_texto = AZUL if i == seleccionada else BLANCO

            pantalla.blit(boton_img, (x, y))

            render_op = fuente.render(texto, True, color_texto)
            rect_op = render_op.get_rect(center=(x + boton_ancho//2, y + boton_alto//2))
            pantalla.blit(render_op, rect_op)

            rect_boton = pygame.Rect(x, y, boton_ancho, boton_alto)
            rects_opciones.append(rect_boton)

        # Mostrar feedback
        if feedback and pygame.time.get_ticks() - feedback_timer < 1000:
            color_fb = AZUL if feedback == "Correcto!" else (255, 0, 0)
            render_fb = fuente.render(feedback, True, color_fb)
            rect_fb = render_fb.get_rect(center=(ANCHO//2, ALTO//2 + 200))
            pantalla.blit(render_fb, rect_fb)
        elif feedback and pygame.time.get_ticks() - feedback_timer >= 1000:
            feedback = ""
            pregunta_idx += 1
            seleccionada = -1
            if pregunta_idx < len(preguntas):
                pregunta = preguntas[pregunta_idx]
                opciones = preparar_pregunta(pregunta)
                correcta = pregunta["correcta"]

        pygame.display.flip()

        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                elif evento.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    if feedback == "":
                        seleccionada = evento.key - pygame.K_1
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1 and feedback == "":
                    pos = evento.pos
                    for i, rect in enumerate(rects_opciones):
                        if rect.collidepoint(pos):
                            seleccionada = i

        # Evaluar respuesta
        if seleccionada != -1 and feedback == "":
            if opciones[seleccionada] == correcta:
                puntaje += 10
                feedback = "Correcto!"
                sonido_bien.play()
            else:
                vidas -= 1
                feedback = "Incorrecto!"
                sonido_mal.play()
            feedback_timer = pygame.time.get_ticks()

        clock.tick(FPS)

def mostrar_top10():
    try:
        with open("partidas.json", "r") as archivo:
            top10 = json.load(archivo)
    except FileNotFoundError:
        top10 = []

    print("=== TOP 10 ===")
    for idx, jugador in enumerate(top10[:10], 1):
        print(f"{idx}. {jugador['nombre']} - {jugador['puntaje']} pts - {jugador['fecha']}")
