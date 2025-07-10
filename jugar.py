import pygame
import csv
import random
import textwrap
import json

from datetime import datetime
from assets import get_parametro, get_imagen, dibujar_texto
from audio import sfx
from eventos import monitorear_eventos

NEGRO  = get_parametro("Colores", "Negro", tuple)
GRIS  = get_parametro("Colores", "Gris", tuple)
BLANCO = get_parametro("Colores", "Blanco", tuple)
AZUL   = get_parametro("Colores", "Azul", tuple)

ANCHO, ALTO = get_parametro("General", "Resolucion", tuple)
ESCALAR = (ANCHO + ALTO) / 2

def cargar_preguntas(dificultad):
    with open("preguntas.csv", encoding="utf-8") as archivo:
        preguntas = [ fila for fila in csv.DictReader(archivo) if fila["dificultad"] == dificultad ]
    random.shuffle(preguntas)
    return preguntas

def siguiente_dificultad(actual):
    orden = ["Facil", "Medio", "Dificil"]
    i = orden.index(actual)
    return orden[(i + 1) % len(orden)]

def comprobar_aciertos(vidas, aciertos, comodin, tiempo_restante, tiempo_general, dificultad):
    if aciertos >= get_parametro(dificultad, "Aciertos_Consecutivos", int):
        vidas += 1
        aciertos = 0
        comodin = True
        if tiempo_general:
            tiempo_restante += get_parametro(dificultad, "Sumar_Tiempo", int) * 1000
            
    return vidas, aciertos, comodin, tiempo_restante

def dividir_texto(texto, max_caracteres=35):
    return textwrap.wrap(texto, width=max_caracteres)

def guardar_partida(nombre, puntos):
    datos = []
    try:
        with open("partidas.json", "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if contenido:
                datos = json.loads(contenido)
            else:
                datos = []
    except (FileNotFoundError, json.JSONDecodeError):
        datos = []

    datos.append({
        "nombre": nombre,
        "puntos": puntos,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open("partidas.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def mostrar_final(pantalla, fuente, puntos, victoria=False):
    if victoria:
        msg_final = ["¡Has ganado, bien jugado!", f"Puntos finales: {puntos}"]
    else:
        msg_final = ["¡Has perdido, buen intento!", f"Puntos finales: {puntos}"]
        
    for i, texto in enumerate(msg_final):
        text_rect = fuente.get_rect(texto)
        x = (ANCHO - text_rect.width) // 2
        y = ALTO // 3 + i * (text_rect.height + 20)
        color = BLANCO if i == 0 else AZUL
        dibujar_texto(pantalla, x, y, texto, fuente, color, NEGRO)

def pedir_nombre(pantalla, fuente, fondo, puntos):
    nombre = ""
    escribiendo = True

    while escribiendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip():
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    char = evento.unicode
                    if char.isalnum() or char.isspace():
                        nombre += char

        pantalla.blit(fondo, (0, 0))
        mostrar_final(pantalla, fuente, puntos)

        mensaje = "Ingrese su nombre:"
        text_rect = fuente.get_rect(mensaje)
        x_msg = (ANCHO - text_rect.width) // 2
        y_msg = ALTO // 2
        dibujar_texto(pantalla, x_msg, y_msg, mensaje, fuente, BLANCO, NEGRO)

        nombre_rect = fuente.get_rect(nombre)
        x_nombre = (ANCHO - nombre_rect.width) // 2
        y_nombre = y_msg + text_rect.height + 20
        dibujar_texto(pantalla, x_nombre, y_nombre, nombre, fuente, AZUL, NEGRO)

        pygame.display.flip()

    return nombre.strip()

def jugar(pantalla, fuente, clock, fps):
    img_fondo = get_imagen("recursos/jugar_fondo.png", (ANCHO, ALTO))
    img_boton = get_imagen("recursos/boton.png", (ESCALAR*.40, ESCALAR*.10))
    boton_ancho, boton_alto = img_boton.get_size()

    dificultad = get_parametro("Juego", "Dificultad", str)
    vidas = get_parametro(dificultad, "Vidas_Iniciales", int)
    preguntas = cargar_preguntas(dificultad)

    puntos = 0
    aciertos_seguidos = 0
    comodin_pasar = True
    
    tiempo_general = get_parametro("Juego", "Tiempo_General", str).capitalize() == "Si"

    if tiempo_general:
        tiempo_limite = get_parametro(dificultad, "tiempo_segundos", int) * 1000
        inicio_tiempo = pygame.time.get_ticks()
        poco_tiempo = False

    while vidas > 0:
        if not preguntas:
            dificultad = siguiente_dificultad(dificultad)
            preguntas = cargar_preguntas(dificultad)

        if not tiempo_general:
            tiempo_limite = get_parametro(dificultad, "tiempo_segundos", int) * 1000
            inicio_tiempo = pygame.time.get_ticks()
            poco_tiempo = False

        pantalla.blit(img_fondo, (0, 0))

        p = preguntas.pop()
        opciones = [p["respuesta1"], p["respuesta2"], p["respuesta3"], p["respuesta_correcta"]]
        opcion_correcta = p["respuesta_correcta"]
        random.shuffle(opciones)

        opcion_seleccionada = 0
        rects_opciones = []
        contestada = False

        while not contestada:
            tiempo_restante = tiempo_limite - (pygame.time.get_ticks() - inicio_tiempo)
            segundos = max(0, tiempo_restante // 1000)

            if segundos == 4 and not poco_tiempo:
                sfx("tictac")
                poco_tiempo = True

            if segundos <= 0:
                sfx("alarma")
                sfx("mal")
                if not tiempo_general:
                    puntos -= get_parametro(dificultad, "puntos_por_desacierto", int)
                    aciertos_seguidos = 0
                    poco_tiempo = False
                    vidas -= 1
                else:
                    vidas = 0
                contestada = True
                continue
            
            rects_opciones.clear()
            pantalla.blit(img_fondo, (0, 0))

            lineas = dividir_texto(p["pregunta"])

            for pos_x, linea in enumerate(lineas):
                rect_linea = fuente.get_rect(linea)
                x_linea = (ANCHO - rect_linea.width) // 2
                y_linea = ESCALAR*.15 + pos_x * (rect_linea.height + 5)
                dibujar_texto(pantalla, x_linea, y_linea, linea, fuente, BLANCO, NEGRO)

            for i, opcion in enumerate(opciones):
                x = (ANCHO - boton_ancho) // 2
                y = ALTO // 2.8 + i * (boton_alto + 20)

                color = AZUL if i == opcion_seleccionada else BLANCO

                pantalla.blit(img_boton, (x, y))
                rect_opcion = fuente.get_rect(opcion)
                text_x = x + (boton_ancho // 2) - rect_opcion.width // 2
                text_y = y + (boton_alto // 2) - rect_opcion.height // 2
                dibujar_texto(pantalla, text_x, text_y, opcion, fuente, color, NEGRO)

                rects_opciones.append(pygame.Rect(x, y, boton_ancho, boton_alto))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_p] and comodin_pasar:
                sfx("boton")
                comodin_pasar = False
                contestada = True
                continue

            comodin_texto = "Tecla P: Omitir pregunta" if comodin_pasar else "Comodín usado"
            comodin_color = BLANCO if comodin_pasar else GRIS
            
            dibujar_texto(pantalla, 40, ALTO - 160, comodin_texto, fuente, comodin_color, NEGRO)
            dibujar_texto(pantalla, 40, ALTO - 120, f"Tiempo: {segundos}", fuente, BLANCO, NEGRO)
            dibujar_texto(pantalla, 40, ALTO - 80, f"Vidas: {vidas}", fuente, BLANCO, NEGRO)
            dibujar_texto(pantalla, 40, ALTO - 40, f"Puntos: {puntos}", fuente, BLANCO, NEGRO)

            opcion_seleccionada, accion = monitorear_eventos(opciones, opcion_seleccionada, rects_opciones, True)

            match accion:
                case "Volver":
                    return
                case _ if accion == opcion_correcta:
                    sfx("bien")
                    puntos += get_parametro(dificultad, "puntos_por_acierto", int)
                    aciertos_seguidos += 1
                    vidas, aciertos_seguidos, comodin_pasar, inicio_tiempo = comprobar_aciertos(vidas, aciertos_seguidos, comodin_pasar, inicio_tiempo, tiempo_general, dificultad)
                    contestada = True
                case _ if accion is not None:
                    sfx("mal")
                    puntos -= get_parametro(dificultad, "puntos_por_desacierto", int)
                    vidas -= 1
                    aciertos_seguidos = 0
                    contestada = True

            pygame.display.flip()
            clock.tick(fps)

    img_fondo = get_imagen("recursos/config_fondo.png", (ANCHO, ALTO))
    nombre = pedir_nombre(pantalla, fuente, img_fondo, puntos)
    guardar_partida(nombre, puntos)

    pygame.display.flip()
    