import numpy as np
import pygame
import sys
from Gráfica.Button import Button
from Gráfica.Historial_Nonograma import NonogramHistory
from Gráfica.draw_text import draw_text
from Gráfica.Matriz_numeros import matriz_numeros
from Gráfica.Square import Square
from Lógica.nonograma_info import matriz_usuario
from Lógica.nonograma_info import is_solved
from Lógica.hints import get_col_hints
from Lógica.hints import get_row_hints
from Lógica.nonograma_info import matriz_solucion
from Lógica.nonograma_info import metadata_nonograma
from Lógica.archivos_npz import guardarNPZ
from Lógica.archivos_npz import cargarNPZ
from Lógica.time_to_minutes import time_to_minutes
import time

WINDOW_SCALE = 3
puzzle_size = metadata_nonograma['size'][0]


class nonogramWindow:
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager

        # Crear color de fondo
        self.Surface_bg = pygame.surface.Surface((300 * WINDOW_SCALE, 300 * WINDOW_SCALE))
        self.Surface_bg.fill((0, 0, 255))

        # Crear surface para el glow
        self.glow_surface = pygame.Surface((256*WINDOW_SCALE, 240*WINDOW_SCALE), pygame.SRCALPHA)
        self.glow_surface.fill((0,0,0))

        # Timer
        self.timer_event = pygame.event.custom_type()
        pygame.time.set_timer(self.timer_event, 1000)
        self.timer = 0

        # Clicks
        self.clicks = 0
        self.initial_square = [0, 0]

        # Ingresar tamaño del puzzle y el cuadrado
        # square_size = (160*WINDOW_SCALE)/puzzle_size
        square_size = 8 * WINDOW_SCALE
        self.obj_square = [
            [Square((i * square_size) + (56 * WINDOW_SCALE), (j * square_size) + 64 * WINDOW_SCALE, 8 * WINDOW_SCALE)
             for i in range(puzzle_size)] for j in range(puzzle_size)]
        # Añadir cuadrados al grupo de sprites, para así poder trabajar con ellos de forma conjunta
        self.group_squares = pygame.sprite.Group()
        for i in range(puzzle_size):
            for j in range(puzzle_size):
                self.group_squares.add(self.obj_square[i][j])

        """
        Ventana Original de la grilla (256x240) --> 160x160
        Puzzle 20x20 --> 24x24px    (20x24 = 480) --> 480/20 = 24
        Puzzle 10x10 --> 48x48px    (10x?  = 480) --> 480/10 = 48
        Puzzle 5x5   -->            (5x?   ? 480) --> 480/5 = 96
        Por lo tanto, el tamaño de cada cuadrado será igual a nuestra constante 480 dividido el tamaño del puzzle

        """

        ########## Crear interfaz ##########
        # Grilla de numeros
        self.Surface_number_up = pygame.surface.Surface((160 * WINDOW_SCALE, 48 * WINDOW_SCALE))
        self.Surface_number_up.fill((18, 100, 114))

        self.Surface_number_left = pygame.surface.Surface((48 * WINDOW_SCALE, 160 * WINDOW_SCALE))
        self.Surface_number_left.fill((18, 100, 114))

        self.number_hints = matriz_numeros(puzzle_size)

        # Añadir cuadrados al grupo de sprites, para así poder trabajar con ellos de forma conjunta
        self.group_number_hints_up = pygame.sprite.Group()
        self.group_number_hints_left = pygame.sprite.Group()
        for i in range(self.number_hints.get_puzzle_size()):
            for j in range(self.number_hints.get_max_numbers()):
                self.group_number_hints_up.add(
                    Square((56 + (i * 8)) * WINDOW_SCALE, (48 - (j * 8)) * WINDOW_SCALE, square_size))
                self.group_number_hints_left.add(
                    Square((40 - (j * 8)) * WINDOW_SCALE, (64 + (i * 8)) * WINDOW_SCALE, square_size))

        ############### RELLENAR MATRIZ ###############
        self.number_hints.set_matriz_filas(get_row_hints(matriz_solucion))
        self.number_hints.set_matriz_columnas(get_col_hints(matriz_solucion))
        ############### RELLENAR MATRIZ ###############

        # Botón de zoom
        self.Button_Zoom = Button(225 * WINDOW_SCALE, 49 * WINDOW_SCALE, 5 * WINDOW_SCALE, "Gráfica/resources/Zoom.png")

        # Botón de antizoom
        self.Button_AntiZoom = Button(242 * WINDOW_SCALE, 49 * WINDOW_SCALE, 5 * WINDOW_SCALE,
                                      "Gráfica/resources/Zoom.png")

        # Boton de menú
        self.Button_Menu = Button(228 * WINDOW_SCALE, 204 * WINDOW_SCALE, 24 * WINDOW_SCALE,
                                  "Gráfica/resources/Menu.png")

        # Boton de pistas
        self.Button_Tips = Button(228 * WINDOW_SCALE, 60 * WINDOW_SCALE, 24 * WINDOW_SCALE,
                                  "Gráfica/resources/Tips.png")

        # Colores
        self.Button_Colours = [[Button(((j * 8) + 232) * WINDOW_SCALE, ((i * 8) + 88) * WINDOW_SCALE, 8 * WINDOW_SCALE,
                                       "Gráfica/resources/Square.png") for i in range(14)] for j in range(2)]

        ########## Crear interfaz ##########

        # Creación de la cámara para Zoom
        camera_group = pygame.sprite.Group()

        self.history = NonogramHistory(matriz_usuario.copy())
        self.solved = False

    def putPixel(self,x, y):
        self.obj_square[x][y].changeImage()
        matriz_usuario[x][y] = self.obj_square[x][y].isFilled()

    def highlightPixel(self, i, j):
        # Varying opacity based on some dynamic factor (e.g., sine wave)
        time = pygame.time.get_ticks()
        opacity = int(128 + 127 * np.sin(time * 0.01))  # Soft pulsing

        glow_square = pygame.Surface((5 * WINDOW_SCALE, 5 * WINDOW_SCALE), pygame.SRCALPHA)
        glow_square.fill((255, 255, 255, opacity))

        self.glow_surface.blit(glow_square, ((self.obj_square[i][j].getPos()[0] + 4), (self.obj_square[i][j].getPos()[1] + 4)))
        self.screen.blit(self.glow_surface, (0, 0))

    def drawLineH(self,x0, y0, x1, y1, isFilling):
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = y1 - y0

        dir = -1 if dy < 0 else 1
        dy *= dir

        if dx != 0:

            y = y0
            p = 2 * dy - dx
            for i in range(dx + 1):
                if isFilling:
                    self.putPixel(x0 + i, y)
                else:
                    self.highlightPixel(x0 + i, y)

                if p >= 0:
                    y += dir
                    p = p - 2 * dx
                p = p + 2 * dy

    def drawLineV(self,x0, y0, x1, y1, isFilling):
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = y1 - y0

        dir = -1 if dx < 0 else 1
        dx *= dir

        if dy != 0:

            x = x0
            p = 2 * dx - dy
            for i in range(dy + 1):
                if isFilling:
                    self.putPixel(x, y0 + i)
                else:
                    self.highlightPixel(x, y0 + i)

                if p >= 0:
                    x += dir
                    p = p - 2 * dy
                p = p + 2 * dx

    def drawLine(self,x0, y0, x1, y1, isFilling):
        if abs(x1 - x0) > abs(y1 - y0):
            self.drawLineH(x0, y0, x1, y1, isFilling)
        else:
            self.drawLineV(x0, y0, x1, y1, isFilling)
        if isFilling:
            self.history.push_state(matriz_usuario.copy())


    def run(self, events):
        mouse = pygame.mouse.get_pressed()

        for event in events:
            if event.type == self.timer_event:
                if not self.solved:
                    self.timer += 1

            # PRESIONAR CUADRADOS
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Guardar cuadrado que presionaste inicialmente
                    for i in range(puzzle_size):
                        for j in range(puzzle_size):
                            if self.obj_square[i][j].isColliding():
                                self.initial_square = [i,j]
                                break


                elif event.button == 3:
                    # Esta función será para marcar el cuadro donde tienes el mouse
                    pass

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    ################### PISTAS #####################################
                    if self.Button_Tips.isColliding():
                        if not is_solved(matriz_usuario):
                            matriz_pistas = np.logical_xor(matriz_solucion, matriz_usuario)

                            # Obtener las posiciones donde hay 1's
                            posiciones = np.where(matriz_pistas == 1)

                            # Elegir aleatoriamente una de esas posiciones
                            indice_random = np.random.randint(len(posiciones[0]))
                            fila_random = posiciones[0][indice_random]
                            columna_random = posiciones[1][indice_random]

                            # La posición aleatoria
                            matriz_usuario[fila_random, columna_random] = 1
                            self.obj_square[fila_random][columna_random].changeImage()
                            matriz_usuario[fila_random][columna_random] = self.obj_square[fila_random][
                                columna_random].isFilled()
                            self.history.push_state(matriz_usuario.copy())
                        ################### PISTAS #####################################

                        if is_solved(matriz_usuario):
                            self.solved = True

                    # Dibujar cuadrados
                    for i in range(puzzle_size):
                        for j in range(puzzle_size):

                            if self.obj_square[i][j].isColliding():
                                if self.initial_square[0] == i and self.initial_square[1] == j:
                                    self.obj_square[i][j].changeImage()
                                    matriz_usuario[i][j] = self.obj_square[i][j].isFilled()
                                    self.history.push_state(matriz_usuario.copy())
                                else:
                                    self.drawLine(self.initial_square[0], self.initial_square[1], i, j, True)

                                # Incrementar variable clicks
                                self.clicks += 1

                                if is_solved(matriz_usuario):
                                    self.solved = True


                elif event.button == 3:
                    # Dibujar cuadrados
                    for i in range(puzzle_size):
                        for j in range(puzzle_size):
                            if self.obj_square[i][j].isColliding():
                                self.obj_square[i][j].changeImageX()
                                matriz_usuario[i][j] = self.obj_square[i][j].isFilled()
                                self.history.push_state(matriz_usuario.copy())

            # MOVER CÁMARA DE PUZZLE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # PUZZLE
                    if (56 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= 210 * WINDOW_SCALE) and (
                            60 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 220 * WINDOW_SCALE):
                        for square in group_squares:
                            square.updatePos(square.rec.x, square.rec.y - ((160 * WINDOW_SCALE) / puzzle_size))
                    # GRILLA DE NUMEROS
                    if (56 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= 215 * WINDOW_SCALE) and (
                            8 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 55 * WINDOW_SCALE):
                        if 48 * WINDOW_SCALE > group_number_hints_up.sprites()[0].getPos()[1] or \
                                group_number_hints_up.sprites()[0].getPos()[1] > 55 * WINDOW_SCALE:
                            for square in group_number_hints_up:
                                square.updatePos(square.rec.x, square.rec.y - ((160 * WINDOW_SCALE) / puzzle_size))

                if event.key == pygame.K_DOWN:
                    if (56 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= 210 * WINDOW_SCALE) and (
                            60 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 220 * WINDOW_SCALE):
                        for square in group_squares:
                            square.updatePos(square.rec.x, square.rec.y + ((160 * WINDOW_SCALE) / puzzle_size))
                    # GRILLA DE NUMEROS
                    if (56 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= 215 * WINDOW_SCALE) and (
                            8 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 55 * WINDOW_SCALE):
                        if 7 * WINDOW_SCALE > \
                                group_number_hints_up.sprites()[number_hints.get_max_numbers() - 1].getPos()[1] or \
                                group_number_hints_up.sprites()[number_hints.get_max_numbers() - 1].getPos()[
                                    1] > 16 * WINDOW_SCALE:
                            for square in group_number_hints_up:
                                square.updatePos(square.rec.x, square.rec.y + ((160 * WINDOW_SCALE) / puzzle_size))

                if event.key == pygame.K_RIGHT:
                    if (56 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= 210 * WINDOW_SCALE) and (
                            60 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 220 * WINDOW_SCALE):
                        for square in group_squares:
                            square.updatePos(square.rec.x + ((160 * WINDOW_SCALE) / puzzle_size), square.rec.y)
                    # GRILLA DE NUMEROS
                    if (0 <= pygame.mouse.get_pos()[0] <= 47 * WINDOW_SCALE) and (
                            64 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 224 * WINDOW_SCALE):
                        if 0 * WINDOW_SCALE > \
                                group_number_hints_left.sprites()[number_hints.get_max_numbers() - 1].getPos()[0] or \
                                group_number_hints_left.sprites()[number_hints.get_max_numbers() - 1].getPos()[
                                    0] > 9 * WINDOW_SCALE:
                            for square in group_number_hints_left:
                                square.updatePos(square.rec.x + ((160 * WINDOW_SCALE) / puzzle_size), square.rec.y)

                if event.key == pygame.K_LEFT:
                    if (56 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= 210 * WINDOW_SCALE) and (
                            60 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 220 * WINDOW_SCALE):
                        for square in group_squares:
                            square.updatePos(square.rec.x - ((160 * WINDOW_SCALE) / puzzle_size), square.rec.y)
                    # GRILLA DE NUMEROS
                    if (0 <= pygame.mouse.get_pos()[0] <= 47 * WINDOW_SCALE) and (
                            64 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 224 * WINDOW_SCALE):
                        if 39 * WINDOW_SCALE > group_number_hints_left.sprites()[0].getPos()[0] or \
                                group_number_hints_left.sprites()[0].getPos()[0] > 46 * WINDOW_SCALE:
                            for square in group_number_hints_left:
                                square.updatePos(square.rec.x - ((160 * WINDOW_SCALE) / puzzle_size), square.rec.y)

                if event.key == pygame.K_o:
                    ################# RESOLUCIÓN AUTOMÁTICA #######################
                    # Solo iniciar si no está ya en proceso de resolución
                    if not hasattr(self, 'auto_solving') or not self.auto_solving:
                        self.auto_solving = True
                        self.last_solve_time = time.time()
                        self.solve_delay = 0.001 # Como se usan 60 FPS el minimo delay es 0.0167
                    ################# RESOLUCIÓN AUTOMÁTICA ########################

                if event.key == pygame.K_z:     #deshacer
                    new_state = self.history.undo()
                    # Incrementar variable clicks
                    self.clicks += 1
                    # Actualizar la visualización
                    for i in range(puzzle_size):
                        for j in range(puzzle_size):
                            if new_state[i][j] != matriz_usuario[i][j]:
                                if new_state[i][j] == 1:
                                    self.obj_square[i][j].changeImage()
                                elif new_state[i][j] == 2:
                                    self.obj_square[i][j].changeImageX()
                                else:
                                    if matriz_usuario[i][j] == 2:
                                        self.obj_square[i][j].changeImageX()
                                    else:
                                        self.obj_square[i][j].changeImage()
                    matriz_usuario[:] = new_state

                if event.key == pygame.K_x:  # Rehacer
                    new_state = self.history.redo()
                    self.clicks += 1
                    # Actualizar la visualización
                    for i in range(puzzle_size):
                        for j in range(puzzle_size):
                            if new_state[i][j] != matriz_usuario[i][j]:
                                if new_state[i][j] == 1:
                                    self.obj_square[i][j].changeImage()
                                elif new_state[i][j] == 2:
                                    self.obj_square[i][j].changeImageX()
                                else:
                                    if matriz_usuario[i][j] == 2:
                                        self.obj_square[i][j].changeImageX()
                                    else:
                                        self.obj_square[i][j].changeImage()
                    matriz_usuario[:] = new_state

        ################# DRAW ################

        # Cuadrados puzzle
        self.screen.blit(self.Surface_bg, (0, 0))
        # Dibujar tamaño del cuadro de la grilla
        pygame.draw.rect(self.Surface_bg, (177, 226, 231),
                         (52 * WINDOW_SCALE, 60 * WINDOW_SCALE, 168 * WINDOW_SCALE, 168 * WINDOW_SCALE))

        for i in range(puzzle_size):
            for j in range(puzzle_size):
                # Esconder si está fuera de pantalla
                if self.obj_square[i][j].rec.y < (62 * WINDOW_SCALE) or self.obj_square[i][j].rec.y > (
                        220 * WINDOW_SCALE) or self.obj_square[i][j].rec.x < (54 * WINDOW_SCALE) or self.obj_square[i][
                    j].rec.x > (210 * WINDOW_SCALE):
                    self.obj_square[i][j].setAlpha(0)
                else:
                    self.obj_square[i][j].setAlpha(255)

                # Añadir a pantalla
                self.Surface_bg.blit(self.obj_square[i][j].image,
                                     (self.obj_square[i][j].getPos()[0], self.obj_square[i][j].getPos()[1]))

        ################ HIGHLIGHT SQUARES ################
        self.glow_surface.fill((0, 0, 0, 0))

        if mouse[0]:
            # Resaltar casillas
            for i in range(puzzle_size):
                for j in range(puzzle_size):
                    if self.obj_square[i][j].isColliding():
                        if self.initial_square[0] == i and self.initial_square[1] == j:
                            self.highlightPixel(i,j)
                        else:
                            self.drawLine(self.initial_square[0], self.initial_square[1], i, j, False)



        ################ HIGHLIGHT SQUARES ################

        # Resolución automática del puzzle
        if hasattr(self, 'auto_solving') and self.auto_solving:
            current_time = time.time()
            if current_time - self.last_solve_time >= self.solve_delay:
                matriz_limpia = matriz_usuario
                matriz_limpia[matriz_limpia != 1] = 0
                matriz_pistas = np.logical_xor(matriz_solucion, matriz_usuario)
                posiciones = np.where(matriz_pistas == 1)
                # Incrementar variable clicks
                self.clicks += 1

                if len(posiciones[0]) > 0:
                    # Elegir la siguiente posición a rellenar
                    indice_random = np.random.randint(len(posiciones[0]))
                    fila_random = posiciones[0][indice_random]
                    columna_random = posiciones[1][indice_random]

                    matriz_usuario[fila_random, columna_random] = 1
                    self.obj_square[fila_random][columna_random].changeImage()
                    matriz_usuario[fila_random][columna_random] = self.obj_square[fila_random][
                        columna_random].isFilled()
                    self.history.push_state(matriz_usuario.copy())

                    self.last_solve_time = current_time
                else:
                    self.auto_solving = False
                    if is_solved(matriz_usuario):
                        self.solved = True

        ## Interfaz
        # Añadir cuadro para timer
        pygame.draw.rect(self.Surface_bg, (0, 0, 0),
                         (4 * WINDOW_SCALE, 12 * WINDOW_SCALE, 48 * WINDOW_SCALE, 48 * WINDOW_SCALE))
        draw_text("Tiempo", "Arial", (255, 255, 255), 8 * WINDOW_SCALE, 10 * WINDOW_SCALE, 18 * WINDOW_SCALE,
                  self.Surface_bg)
        # Añadir timer
        draw_text(f"{time_to_minutes(self.timer)}", "Arial", (255, 255, 255), 8 * WINDOW_SCALE, 10 * WINDOW_SCALE, 25 * WINDOW_SCALE,
                  self.Surface_bg)

        # Añadir clicks
        draw_text(f"clicks:{self.clicks}", "Arial", (255, 255, 255), 8 * WINDOW_SCALE, 10 * WINDOW_SCALE,42 * WINDOW_SCALE,self.Surface_bg)


        # Añadir cuadro para minimapa
        pygame.draw.rect(self.Surface_bg, (84, 181, 190),
                         (220 * WINDOW_SCALE, 12 * WINDOW_SCALE, 32 * WINDOW_SCALE, 32 * WINDOW_SCALE))

        # Añadir cuadro para colores
        pygame.draw.rect(self.Surface_bg, (16, 92, 106),
                         (228 * WINDOW_SCALE, 84 * WINDOW_SCALE, 24 * WINDOW_SCALE, 120 * WINDOW_SCALE))

        # Cuadro derecha, Colores, Botones
        # pygame.draw.rect(Surface_bg, (235,235,35), (208*WINDOW_SCALE, 0*WINDOW_SCALE,48*WINDOW_SCALE,240*WINDOW_SCALE))

        # Añadir Números Arriba
        self.Surface_bg.blit(self.Surface_number_up, (56 * WINDOW_SCALE, 8 * WINDOW_SCALE))
        # Añadir Números Izquierda
        self.Surface_bg.blit(self.Surface_number_left, (0, 64 * WINDOW_SCALE))

        # Dibujar Numeros pista
        # Columnas
        for square in self.group_number_hints_up:
            if square.rec.y < (8 * WINDOW_SCALE) or square.rec.y > (55 * WINDOW_SCALE):
                square.setAlpha(0)
            else:
                square.setAlpha(255)
            self.Surface_bg.blit(square.image, square.getPos())

        for i in range(self.number_hints.get_puzzle_size()):
            for j in range(self.number_hints.get_max_numbers()):
                if self.number_hints.get_matriz_columna_value(i, j) != 0:
                    pos_x = (self.group_number_hints_up.sprites()[
                                 (i * self.number_hints.get_max_numbers()) + j].getPos()[0] + (2 * WINDOW_SCALE))
                    pos_y = (self.group_number_hints_up.sprites()[
                                 (i * self.number_hints.get_max_numbers()) + j].getPos()[1] - (1 * WINDOW_SCALE))

                    if 4 * WINDOW_SCALE <= pos_y <= 54 * WINDOW_SCALE:
                        draw_text(f"{self.number_hints.get_matriz_columna_value(i, j)}", "Arial", (255, 255, 255),
                                  8 * WINDOW_SCALE, pos_x, pos_y, self.Surface_bg)

        # Filas
        for square in self.group_number_hints_left:
            if square.rec.x < 0 or square.rec.x > (47 * WINDOW_SCALE):
                square.setAlpha(0)
            else:
                square.setAlpha(255)
            self.Surface_bg.blit(square.image, square.getPos())

        for i in range(self.number_hints.get_puzzle_size()):
            for j in range(self.number_hints.get_max_numbers()):
                if self.number_hints.get_matriz_fila_value(i, j) != 0:
                    pos_x = \
                    self.group_number_hints_left.sprites()[(i * self.number_hints.get_max_numbers()) + j].getPos()[
                        0] + (2 * WINDOW_SCALE)
                    pos_y = \
                    self.group_number_hints_left.sprites()[(i * self.number_hints.get_max_numbers()) + j].getPos()[
                        1] - (1 * WINDOW_SCALE)

                    if 0 <= pos_x <= 49 * WINDOW_SCALE:
                        draw_text(f"{self.number_hints.get_matriz_fila_value(i, j)}", "Arial", (255, 255, 255),
                                  8 * WINDOW_SCALE, pos_x, pos_y, self.Surface_bg)

        # Añadir botón de menu
        self.Surface_bg.blit(self.Button_Menu.image, (self.Button_Menu.getPos()))
        # Añadir botón de pistas
        self.Surface_bg.blit(self.Button_Tips.image, (self.Button_Tips.getPos()))

        # Añadir botón de zoom
        self.Surface_bg.blit(self.Button_Zoom.image, (self.Button_Zoom.getPos()))
        # Añadir botón de antizoom
        self.Surface_bg.blit(self.Button_AntiZoom.image, (self.Button_AntiZoom.getPos()))
        # Añadir logo de zoom
        pygame.draw.rect(self.Surface_bg, (47, 110, 117),
                         (232 * WINDOW_SCALE, 48 * WINDOW_SCALE, 8 * WINDOW_SCALE, 8 * WINDOW_SCALE))
        # Añadir botones de colores
        for i in range(14):
            for j in range(2):
                self.Surface_bg.blit(self.Button_Colours[j][i].image, (self.Button_Colours[j][i].getPos()))
        # Mostrar texto "resuelto"
        if self.solved:
            var_image = pygame.transform.scale(pygame.image.load("Gráfica/resources/Resuelto.png"),
                                               (200 * WINDOW_SCALE, 100 * WINDOW_SCALE))
            self.Surface_bg.blit(var_image, (50 * WINDOW_SCALE, 100 * WINDOW_SCALE))
        pygame.display.flip()
        ################# DRAW ################