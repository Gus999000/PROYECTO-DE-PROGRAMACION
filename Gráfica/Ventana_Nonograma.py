import numpy as np
import pygame
import sys
from Gráfica.Button import Button
from Gráfica.Historial_Nonograma import NonogramHistory
from Gráfica.draw_text import draw_text
from Gráfica.Matriz_numeros import matriz_numeros
from Gráfica.Square import Square, WINDOW_SCALE
from Lógica.nonograma_info import matriz_usuario, id_nonograma
from Lógica.nonograma_info import is_solved
from Lógica.hints import get_col_hints
from Lógica.hints import get_row_hints
from Lógica.nonograma_info import matriz_solucion
from Lógica.nonograma_info import metadata_nonograma
from Lógica.archivos_npz import guardarNPZ
from Lógica.archivos_npz import cargarNPZ
from Lógica.time_to_minutes import time_to_minutes
from Lógica.Logros import NonogramAchievementTracker
import time

puzzle_size = metadata_nonograma['size'][0]
WINDOW_SCALE = 3

pygame.font.init()
Font_smolmatrix_smallsize =pygame.font.Font("Gráfica/Audiovisual_juego/Fonts/3x5-smolmatrix.ttf", 5*WINDOW_SCALE)
Font_CutebitmapismA_smallsize =pygame.font.Font("Gráfica/Audiovisual_juego/Fonts/7x-D3CutebitmapismA.ttf", 5*WINDOW_SCALE)
Font_CutebitmapismA_mediumsize =pygame.font.Font("Gráfica/Audiovisual_juego/Fonts/7x-D3CutebitmapismA.ttf", 7*WINDOW_SCALE)
Font_CutebitmapismA_bigsize =pygame.font.Font("Gráfica/Audiovisual_juego/Fonts/7x-D3CutebitmapismA.ttf", 8*WINDOW_SCALE)


class nonogramWindow:
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager

        self.achievement_tracker = NonogramAchievementTracker()

        # Crear surface para el fondo
        self.Surface_bg = pygame.surface.Surface((300 * WINDOW_SCALE, 300 * WINDOW_SCALE))
        self.Surface_bg.fill((0, 0, 0))

        # Crear surface para el glow
        self.glow_surface = pygame.Surface((256*WINDOW_SCALE, 240*WINDOW_SCALE), pygame.SRCALPHA)
        self.glow_surface.fill((0,0,0))

        self.glow_surface2 = pygame.Surface((256*WINDOW_SCALE, 240*WINDOW_SCALE), pygame.SRCALPHA)
        self.glow_surface.fill((0, 0, 0))

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
                self.group_number_hints_up.add(Square((56 + (i * 8)) * WINDOW_SCALE, (48 - (j * 8)) * WINDOW_SCALE, square_size))
                self.group_number_hints_left.add(Square((40 - (j * 8)) * WINDOW_SCALE, (64 + (i * 8)) * WINDOW_SCALE, square_size))

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
        self.Button_Menu = Button(228 * WINDOW_SCALE, 204 * WINDOW_SCALE, 24 * WINDOW_SCALE,"Gráfica/Audiovisual_juego/Sprites/Jugar/boton_pausa.png")

        # Boton de pistas
        self.Button_Tips = Button(228 * WINDOW_SCALE, 60 * WINDOW_SCALE, 24 * WINDOW_SCALE,"Gráfica/Audiovisual_juego/Sprites/Jugar/lvl_boton_pista.png")

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

        self.glow_surface.blit(glow_square, ((self.obj_square[i][j].getPos()[0] + WINDOW_SCALE), (self.obj_square[i][j].getPos()[1] + WINDOW_SCALE)))
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
                            matriz_aux = matriz_usuario
                            matriz_aux[matriz_aux != 1] = 0
                            matriz_pistas = np.logical_xor(matriz_solucion, matriz_aux)

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

                            # Incrementar variable clicks
                            self.clicks += 1
                        ################### PISTAS #####################################

                        if is_solved(matriz_usuario):
                            self.achievement_tracker.puzzle_completed(id_nonograma, self.timer, self.clicks, puzzle_size)
                            self.solved = True
                            self.achievement_tracker.show_achievements(show_all=True)

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
                                    self.achievement_tracker.puzzle_completed(id_nonograma, self.timer, self.clicks, puzzle_size)
                                    self.solved = True
                                    self.achievement_tracker.show_achievements(show_all=True)


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
                        for square in self.group_squares:
                            square.updatePos(square.rec.x, square.rec.y - ((160 * WINDOW_SCALE) / puzzle_size))
                    # GRILLA DE NUMEROS
                    if (56 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= 215 * WINDOW_SCALE) and (
                            8 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 55 * WINDOW_SCALE):
                        if 48 * WINDOW_SCALE > self.group_number_hints_up.sprites()[0].getPos()[1] or \
                                self.group_number_hints_up.sprites()[0].getPos()[1] > 55 * WINDOW_SCALE:
                            for square in self.group_number_hints_up:
                                square.updatePos(square.rec.x, square.rec.y - ((160 * WINDOW_SCALE) / puzzle_size))

                if event.key == pygame.K_DOWN:
                    if (56 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= 210 * WINDOW_SCALE) and (
                            60 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 220 * WINDOW_SCALE):
                        for square in self.group_squares:
                            square.updatePos(square.rec.x, square.rec.y + ((160 * WINDOW_SCALE) / puzzle_size))
                    # GRILLA DE NUMEROS
                    if (56 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= 215 * WINDOW_SCALE) and (
                            8 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 55 * WINDOW_SCALE):
                        if 7 * WINDOW_SCALE > \
                                self.group_number_hints_up.sprites()[self.number_hints.get_max_numbers() - 1].getPos()[1] or \
                                self.group_number_hints_up.sprites()[self.number_hints.get_max_numbers() - 1].getPos()[
                                    1] > 16 * WINDOW_SCALE:
                            for square in self.group_number_hints_up:
                                square.updatePos(square.rec.x, square.rec.y + ((160 * WINDOW_SCALE) / puzzle_size))

                if event.key == pygame.K_RIGHT:
                    if (56 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= 210 * WINDOW_SCALE) and (
                            60 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 220 * WINDOW_SCALE):
                        for square in self.group_squares:
                            square.updatePos(square.rec.x + ((160 * WINDOW_SCALE) / puzzle_size), square.rec.y)
                    # GRILLA DE NUMEROS
                    if (0 <= pygame.mouse.get_pos()[0] <= 47 * WINDOW_SCALE) and (
                            64 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 224 * WINDOW_SCALE):
                        if 0 * WINDOW_SCALE > \
                                self.group_number_hints_left.sprites()[self.number_hints.get_max_numbers() - 1].getPos()[0] or \
                                self.group_number_hints_left.sprites()[self.number_hints.get_max_numbers() - 1].getPos()[
                                    0] > 9 * WINDOW_SCALE:
                            for square in self.group_number_hints_left:
                                square.updatePos(square.rec.x + ((160 * WINDOW_SCALE) / puzzle_size), square.rec.y)

                if event.key == pygame.K_LEFT:
                    if (56 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= 210 * WINDOW_SCALE) and (
                            60 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 220 * WINDOW_SCALE):
                        for square in self.group_squares:
                            square.updatePos(square.rec.x - ((160 * WINDOW_SCALE) / puzzle_size), square.rec.y)
                    # GRILLA DE NUMEROS
                    if (0 <= pygame.mouse.get_pos()[0] <= 47 * WINDOW_SCALE) and (
                            64 * WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 224 * WINDOW_SCALE):
                        if 39 * WINDOW_SCALE > self.group_number_hints_left.sprites()[0].getPos()[0] or \
                                self.group_number_hints_left.sprites()[0].getPos()[0] > 46 * WINDOW_SCALE:
                            for square in self.group_number_hints_left:
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
                    #var_aux = False
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
                                        # Decrementar variable clicks
                                        self.clicks -= 1
                                    else:
                                        self.obj_square[i][j].changeImage()
                    if np.array_equal(new_state, matriz_usuario):
                        # Decrementar variable clicks
                        self.clicks -= 1
                    matriz_usuario[:] = new_state

                if event.key == pygame.K_x:  # Rehacer
                    new_state = self.history.redo()
                    # Actualizar la visualización
                    # Incrementar variable clicks
                    self.clicks += 1
                    for i in range(puzzle_size):
                        for j in range(puzzle_size):
                            if new_state[i][j] != matriz_usuario[i][j]:
                                if new_state[i][j] == 1:
                                    self.obj_square[i][j].changeImage()
                                elif new_state[i][j] == 2:
                                    self.obj_square[i][j].changeImageX()
                                    # Decrementar variable clicks
                                    self.clicks -= 1
                                else:
                                    if matriz_usuario[i][j] == 2:
                                        self.obj_square[i][j].changeImageX()
                                        # Decrementar variable clicks
                                        self.clicks -= 1
                                    else:
                                        self.obj_square[i][j].changeImage()
                    if np.array_equal(new_state, matriz_usuario):
                        # Decrementar variable clicks
                        self.clicks -= 1

                    matriz_usuario[:] = new_state

        ################# DRAW ################


        # Cuadrados puzzle
        self.screen.blit(self.Surface_bg, (0, 0))
        surface_bg_image = pygame.image.load("Gráfica/Audiovisual_juego/Sprites/Jugar/lvl_overlay_nivel-max.png")
        surface_bg_image = pygame.transform.scale(surface_bg_image, (256*WINDOW_SCALE, 240*WINDOW_SCALE))
        self.Surface_bg.blit(surface_bg_image, (0,0))

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
        # Añadir bordes a la grilla
        for i in range(puzzle_size):
            # Bordes Horizontales
            pos_x = self.obj_square[0][i].getPos()[0]
            height = (8*puzzle_size + 62)*WINDOW_SCALE
            borde = pygame.image.load("Gráfica/Audiovisual_juego/Sprites/Jugar/lvl_bordes_grilla.png")
            borde = pygame.transform.scale(borde, (8 * WINDOW_SCALE, 8 * WINDOW_SCALE))
            self.Surface_bg.blit(borde, (pos_x, 57 * WINDOW_SCALE))
            self.Surface_bg.blit(borde, (pos_x, height))

            #Bordes Verticales
            pos_y = self.obj_square[i][0].getPos()[1]
            width = (8*metadata_nonograma['size'][0] + 54)*WINDOW_SCALE
            bordeV = pygame.transform.rotate(borde, 90)
            self.Surface_bg.blit(bordeV, (49*WINDOW_SCALE, pos_y))
            self.Surface_bg.blit(bordeV, (width, pos_y))
        # Añadir esquinas a la grilla
        esquina = pygame.image.load("Gráfica/Audiovisual_juego/Sprites/Jugar/lvl_esquinas_grilla.png")
        esquina = pygame.transform.scale(esquina, (8*WINDOW_SCALE, 8*WINDOW_SCALE))
        esquinaUR = pygame.transform.rotate(esquina, -90)
        esquinaDR = pygame.transform.rotate(esquina, 180)
        esquinaDL = pygame.transform.rotate(esquina, 90)
        self.Surface_bg.blit(esquina, (51*WINDOW_SCALE, 59*WINDOW_SCALE))
        self.Surface_bg.blit(esquinaUR, (self.obj_square[0][puzzle_size - 1].getPos()[0]+5*WINDOW_SCALE, 59 * WINDOW_SCALE))
        self.Surface_bg.blit(esquinaDR, (self.obj_square[0][puzzle_size - 1].getPos()[0]+5*WINDOW_SCALE, self.obj_square[puzzle_size - 1][0].getPos()[1]+5*WINDOW_SCALE))
        self.Surface_bg.blit(esquinaDL, (
        51*WINDOW_SCALE,
        self.obj_square[puzzle_size - 1][0].getPos()[1] + 5 * WINDOW_SCALE))


        ################ HIGHLIGHT SQUARES ################
        # Algoritmo
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

        # Pasar mouse por encima
        self.glow_surface2.fill((0, 0, 0, 0))

        for i in range(puzzle_size):
            for j in range(puzzle_size):
                if self.obj_square[i][j].isColliding():
                    self.highlightPixel(i,j)

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
                        self.achievement_tracker.puzzle_completed(id_nonograma, self.timer, self.clicks, puzzle_size)
                        self.solved = True
                        self.achievement_tracker.show_achievements(show_all=True)

        ## Interfaz
        # Añadir cuadro para timer
        timerImage = pygame.image.load("Gráfica/Audiovisual_juego/Sprites/Jugar/lvl_cuadroinfo0.png")
        timerImage = pygame.transform.scale(timerImage, (48*WINDOW_SCALE, 48*WINDOW_SCALE))
        self.Surface_bg.blit(timerImage, (4 * WINDOW_SCALE, 12 * WINDOW_SCALE))

        # Añadir timer
        self.Surface_bg.blit(Font_CutebitmapismA_mediumsize.render(f"{time_to_minutes(self.timer)}", False, (255, 255, 255)),(10 * WINDOW_SCALE, 25 * WINDOW_SCALE))

        # Añadir clicks
        if self.clicks < 1000:
            self.Surface_bg.blit(Font_CutebitmapismA_mediumsize.render(f"{self.clicks}", False, (255, 255, 255)),(32 * WINDOW_SCALE, 40 * WINDOW_SCALE))
        else:
            self.Surface_bg.blit(Font_CutebitmapismA_smallsize.render(f"{self.clicks}", False, (255, 255, 255)),(32 * WINDOW_SCALE, 42 * WINDOW_SCALE))

        # Añadir cuadro para minimapa
        minimapImage = pygame.image.load("Gráfica/Audiovisual_juego/Sprites/Jugar/Indicador_vista_previa.png")
        minimapImage = pygame.transform.scale(minimapImage,(32*WINDOW_SCALE, 32*WINDOW_SCALE))
        self.Surface_bg.blit(minimapImage, (220*WINDOW_SCALE, 20*WINDOW_SCALE))

        # Añadir cuadro para colores
        monocolorImage = pygame.image.load("Gráfica/Audiovisual_juego/Sprites/Jugar/lvl_mono_relleno_selector.png")
        monocolorImage = pygame.transform.scale(monocolorImage, (24*WINDOW_SCALE, 120*WINDOW_SCALE))
        self.Surface_bg.blit(monocolorImage, (228*WINDOW_SCALE, 84*WINDOW_SCALE))

        # Añadir marco para la grilla
        #marco_grillaImage = pygame.image.load("Gráfica/Audiovisual_juego/Sprites/Jugar/lvl_marco_grilla.png")
        #marco_grillaImage = pygame.transform.scale(marco_grillaImage, (256*WINDOW_SCALE,240*WINDOW_SCALE))
        #self.Surface_bg.blit(marco_grillaImage, (0,0))

        # Dibujar Numeros pista
        # Columnas
        for square in self.group_number_hints_up:
            if 8*WINDOW_SCALE<= square.rec.y <= (56 * WINDOW_SCALE):
                pos_x = square.getPos()[0]
                if (pos_x // (8 * WINDOW_SCALE)) % 2 == 0:
                    pygame.draw.rect(self.Surface_bg, (14, 82, 93),(square.getPos()[0], square.getPos()[1], 8 * WINDOW_SCALE, 8 * WINDOW_SCALE))
                else:
                    pygame.draw.rect(self.Surface_bg, (91, 177, 194),(square.getPos()[0], square.getPos()[1], 8 * WINDOW_SCALE, 8 * WINDOW_SCALE))


        for i in range(self.number_hints.get_puzzle_size()):
            for j in range(self.number_hints.get_max_numbers()):
                if self.number_hints.get_matriz_columna_value(i, j) != 0:
                    text_surface = Font_smolmatrix_smallsize.render(f"{self.number_hints.get_matriz_columna_value(i, j)}", True, (255, 255, 255))
                    text_width, text_height = text_surface.get_size()
                    x = self.group_number_hints_up.sprites()[(i * self.number_hints.get_max_numbers()) + j].getPos()[0]
                    y = self.group_number_hints_up.sprites()[(i * self.number_hints.get_max_numbers()) + j].getPos()[1]
                    pos_x = x + (8*WINDOW_SCALE - text_width) // 2
                    pos_y = y + (8*WINDOW_SCALE - text_height) // 2

                    if 4 * WINDOW_SCALE <= pos_y <= 54 * WINDOW_SCALE:
                        self.Surface_bg.blit(text_surface,(pos_x, pos_y))

        # Filas
        for square in self.group_number_hints_left:
            if 0 <= square.rec.x <= (47 * WINDOW_SCALE):
                pos_y = square.getPos()[1]
                if (pos_y // (8 * WINDOW_SCALE)) % 2 == 0:
                    pygame.draw.rect(self.Surface_bg, (14, 82, 93),(square.getPos()[0], square.getPos()[1], 8 * WINDOW_SCALE, 8 * WINDOW_SCALE))
                else:
                    pygame.draw.rect(self.Surface_bg, (91, 177, 194),(square.getPos()[0], square.getPos()[1], 8 * WINDOW_SCALE, 8 * WINDOW_SCALE))


        for i in range(self.number_hints.get_puzzle_size()):
            for j in range(self.number_hints.get_max_numbers()):
                if self.number_hints.get_matriz_fila_value(i, j) != 0:
                    text_surface = Font_smolmatrix_smallsize.render(f"{self.number_hints.get_matriz_fila_value(i, j)}", True, (255, 255, 255))
                    text_width, text_height = text_surface.get_size()
                    x = self.group_number_hints_left.sprites()[(i * self.number_hints.get_max_numbers()) + j].getPos()[0]
                    y = self.group_number_hints_left.sprites()[(i * self.number_hints.get_max_numbers()) + j].getPos()[1]
                    pos_x = x + (8*WINDOW_SCALE - text_width) // 2
                    pos_y = y + (8*WINDOW_SCALE - text_height) // 2

                    if 0 <= pos_x <= 49 * WINDOW_SCALE:
                        self.Surface_bg.blit(text_surface, (pos_x, pos_y))

        ############# HIGHLIGHT FILAS Y COLUMNAS #############

        for square in self.group_number_hints_left:
            # Verificar si está dentro de la grilla
            if 52*WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= (220 * WINDOW_SCALE) and 60*WINDOW_SCALE <= pygame.mouse.get_pos()[1] <= 225*WINDOW_SCALE and 0 <= square.rec.x <= (47 * WINDOW_SCALE):
                pos_y = square.getPos()[1]
                # Si el mouse está dentro de los límites de un cuadrado, destacar la grilla de números correspondiente
                if (pygame.mouse.get_pos()[1] - (7*WINDOW_SCALE) <=pos_y <= pygame.mouse.get_pos()[1]):
                    glow_surface = pygame.Surface((256 * WINDOW_SCALE, 240 * WINDOW_SCALE), pygame.SRCALPHA)
                    glow_square = pygame.Surface((8 * WINDOW_SCALE, 8 * WINDOW_SCALE), pygame.SRCALPHA)
                    glow_square.fill((255, 255, 255, 100))

                    glow_surface.blit(glow_square, (square.getPos()[0], square.getPos()[1]))
                    self.screen.blit(glow_surface, (0, 0))

        for square in self.group_number_hints_up:
            # Verificar si está dentro de la grilla
            if 52 * WINDOW_SCALE <= pygame.mouse.get_pos()[0] <= (220 * WINDOW_SCALE) and 60 * WINDOW_SCALE <=pygame.mouse.get_pos()[1] <= 225 * WINDOW_SCALE and 8*WINDOW_SCALE<= square.rec.y <= (56 * WINDOW_SCALE):
                pos_x = square.getPos()[0]
                # Si el mouse está dentro de los límites de un cuadrado, destacar la grilla de números correspondiente
                if pygame.mouse.get_pos()[0]-(7*WINDOW_SCALE) <=pos_x <= pygame.mouse.get_pos()[0]:
                    glow_surface = pygame.Surface((256 * WINDOW_SCALE, 240 * WINDOW_SCALE), pygame.SRCALPHA)
                    glow_square = pygame.Surface((8 * WINDOW_SCALE, 8 * WINDOW_SCALE), pygame.SRCALPHA)
                    glow_square.fill((255, 255, 255, 100))

                    glow_surface.blit(glow_square, (square.getPos()[0], square.getPos()[1]))
                    self.screen.blit(glow_surface, (0, 0))



        ############# HIGHLIGHT FILAS Y COLUMNAS #############


        # Añadir botón de menu
        self.Surface_bg.blit(self.Button_Menu.image, (self.Button_Menu.getPos()))
        # Añadir botón de pistas
        self.Surface_bg.blit(self.Button_Tips.image, (self.Button_Tips.getPos()))

        # Añadir botón de zoom
        #self.Surface_bg.blit(self.Button_Zoom.image, (self.Button_Zoom.getPos()))3
        # Añadir botón de antizoom
        #self.Surface_bg.blit(self.Button_AntiZoom.image, (self.Button_AntiZoom.getPos()))
        # Añadir logo de zoom
        #pygame.draw.rect(self.Surface_bg, (47, 110, 117),(232 * WINDOW_SCALE, 48 * WINDOW_SCALE, 8 * WINDOW_SCALE, 8 * WINDOW_SCALE))
        # Añadir botones de colores
        """
        for i in range(14):
            for j in range(2):
                self.Surface_bg.blit(self.Button_Colours[j][i].image, (self.Button_Colours[j][i].getPos()))
        """
        # Mostrar texto "resuelto"
        if self.solved:
            # Dibujar rectangulo con alpha
            s = pygame.Surface((256*WINDOW_SCALE, 240*WINDOW_SCALE))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            self.Surface_bg.blit(s, (0, 0))

            # Dibujar rectangulo nivel completado
            var_image = pygame.transform.scale(pygame.image.load("Gráfica/Audiovisual_juego/Sprites/Jugar/lvl_popup_nivel_completado.png"),
                                               (206 * WINDOW_SCALE, 94 * WINDOW_SCALE))
            self.Surface_bg.blit(var_image, (30 * WINDOW_SCALE, 70 * WINDOW_SCALE))

            # Añadir tiempo
            self.Surface_bg.blit(Font_CutebitmapismA_bigsize.render(f"{time_to_minutes(self.timer)}", False, (255, 255, 255)),(110 * WINDOW_SCALE, 101 * WINDOW_SCALE))

            # Añadir clicks
            self.Surface_bg.blit(Font_CutebitmapismA_bigsize.render(f"{self.clicks}", False, (255, 255, 255)), (110*WINDOW_SCALE, 117*WINDOW_SCALE))

        pygame.display.flip()
        ################# DRAW ################

