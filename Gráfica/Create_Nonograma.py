import numpy as np
import pygame
import sys
from Gráfica.Button import Button, Button_notSquare
from Gráfica.Historial_Nonograma import NonogramHistory
from Gráfica.draw_text import draw_text
from Gráfica.Matriz_numeros import matriz_numeros
from Gráfica.Square import Square, WINDOW_SCALE
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

puzzle_size = metadata_nonograma['size'][0]
WINDOW_SCALE = 3

pygame.font.init()
Font_smolmatrix_smallsize =pygame.font.Font("Gráfica/Recursos/Fonts/3x5-smolmatrix.ttf", 5*WINDOW_SCALE)
Font_CutebitmapismA_smallsize =pygame.font.Font("Gráfica/Recursos/Fonts/7x-D3CutebitmapismA.ttf", 5*WINDOW_SCALE)
Font_CutebitmapismA_mediumsize =pygame.font.Font("Gráfica/Recursos/Fonts/7x-D3CutebitmapismA.ttf", 7*WINDOW_SCALE)
Font_CutebitmapismA_bigsize =pygame.font.Font("Gráfica/Recursos/Fonts/7x-D3CutebitmapismA.ttf", 8*WINDOW_SCALE)

class createNonogram:
    _user_text = "" # MAX 27 CHARACTERS
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager

        # Crear surface para el fondo
        self.Surface_bg = pygame.surface.Surface((300 * WINDOW_SCALE, 300 * WINDOW_SCALE))
        self.Surface_bg.fill((0, 0, 0))

        # Crear surface para el glow
        self.glow_surface = pygame.Surface((256*WINDOW_SCALE, 240*WINDOW_SCALE), pygame.SRCALPHA)
        self.glow_surface.fill((0,0,0))

        self.glow_surface2 = pygame.Surface((256*WINDOW_SCALE, 240*WINDOW_SCALE), pygame.SRCALPHA)
        self.glow_surface.fill((0, 0, 0))

        self.initial_square = [0, 0]

        # Ingresar tamaño del puzzle y el cuadrado
        # square_size = (160*WINDOW_SCALE)/puzzle_size
        square_size = 8 * WINDOW_SCALE
        self.obj_square = [[Square((i * square_size) + (15 * WINDOW_SCALE), (j * square_size) + 23 * WINDOW_SCALE, 8 * WINDOW_SCALE)for i in range(puzzle_size)] for j in range(puzzle_size)]
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

        # Botones de menú
        self.Button_Menu = Button(228 * WINDOW_SCALE, 204 * WINDOW_SCALE, 24 * WINDOW_SCALE,"Gráfica/Recursos/Sprites/Jugar/boton_pausa.png")
        self.Button_Guardar = Button_notSquare(54*WINDOW_SCALE,102*WINDOW_SCALE,54*WINDOW_SCALE, 6*WINDOW_SCALE, "Gráfica/Recursos/Sprites/Crear/cr_opcion_guardar_popup.png")
        self.Button_MenuPrincipal = Button_notSquare(54*WINDOW_SCALE, 118*WINDOW_SCALE, 110 * WINDOW_SCALE, 7 * WINDOW_SCALE,"Gráfica/Recursos/Sprites/Crear/cr_opcion_menuprincipal_popup.png")
        self.Button_CerrarJuego = Button_notSquare(54*WINDOW_SCALE, 134*WINDOW_SCALE, 94 * WINDOW_SCALE, 7 * WINDOW_SCALE,"Gráfica/Recursos/Sprites/Crear/cr_opcion_cerrarjuego_popup.png")

        self.Button_GuardarySalir = Button_notSquare(38*WINDOW_SCALE,123*WINDOW_SCALE,84*WINDOW_SCALE,20*WINDOW_SCALE,"Gráfica/Recursos/Sprites/Crear/cr_boton_popup_guardar.png")
        self.Button_Cancelar = Button_notSquare(134*WINDOW_SCALE, 123*WINDOW_SCALE, 84*WINDOW_SCALE, 20*WINDOW_SCALE, "Gráfica/Recursos/Sprites/Crear/cr_boton_popup_cancelar.png")

        self.pause = False  # Pausa del juego
        self.guardar = False # Popup para guardar

        # Boton de pistas
        self.Button_Tips = Button(228 * WINDOW_SCALE, 60 * WINDOW_SCALE, 24 * WINDOW_SCALE,"Gráfica/Recursos/Sprites/Jugar/lvl_boton_pista.png")

        # Colores
        self.Button_Colours = [[Button(((j * 8) + 232) * WINDOW_SCALE, ((i * 8) + 88) * WINDOW_SCALE, 8 * WINDOW_SCALE,
                                       "Gráfica/resources/Square.png") for i in range(14)] for j in range(2)]

        ########## Crear interfaz ##########

        # Creación de la cámara para Zoom
        camera_group = pygame.sprite.Group()

        self.history = NonogramHistory(matriz_usuario.copy())
        self.solved = False

    def putPixel(self,x, y):
        if not self.obj_square[x][y].isFilled():
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

    def GuardarMatriz(self, nombre:str, id: str):
        estado_actual = matriz_usuario.copy()
        matriz_binaria = np.zeros_like(estado_actual)

        for i in range(puzzle_size):
            for j in range(puzzle_size):
                if estado_actual[i][j] == 1:
                    matriz_binaria[i][j] = 1

        guardarNPZ(nombre, id, matriz_binaria)

    def run(self, events):
        mouse = pygame.mouse.get_pressed()

        for event in events:

            # PRESIONAR CUADRADOS
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Guardar cuadrado que presionaste inicialmente
                    if not self.pause:
                        for i in range(puzzle_size):
                            for j in range(puzzle_size):
                                if self.obj_square[i][j].isColliding():
                                    self.initial_square = [i,j]
                                    break

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Dibujar cuadrados
                    if not self.pause:
                        for i in range(puzzle_size):
                            for j in range(puzzle_size):

                                if self.obj_square[i][j].isColliding():
                                    if self.initial_square[0] == i and self.initial_square[1] == j:
                                        self.obj_square[i][j].changeImage()
                                        matriz_usuario[i][j] = self.obj_square[i][j].isFilled()
                                        self.history.push_state(matriz_usuario.copy())
                                    else:
                                        self.drawLine(self.initial_square[0], self.initial_square[1], i, j, True)
                    else:
                        if self.guardar:
                            if self.Button_Cancelar.isColliding():
                                self._user_text = ""
                                self.guardar = False
                            elif self.Button_GuardarySalir.isColliding():
                                self.GuardarMatriz("created.npz", self._user_text)
                                self.gameStateManager.set_state("menuWindow")
                    # Menu
                    if self.Button_Menu.isColliding():
                        self.pause = True
                    # Botones del Menú
                    if self.pause:
                        if self.Button_Guardar.isColliding():
                            self.guardar = True
                        if self.Button_MenuPrincipal.isColliding():
                            self.gameStateManager.set_state("menuWindow")
                        if self.Button_CerrarJuego.isColliding():
                            pygame.quit()
                            sys.exit()

                elif event.button == 3:
                    # Dibujar cuadrados
                    if not self.pause:
                        for i in range(puzzle_size):
                            for j in range(puzzle_size):
                                if self.obj_square[i][j].isColliding():
                                    self.obj_square[i][j].changeImageX()
                                    matriz_usuario[i][j] = self.obj_square[i][j].isFilled()
                                    self.history.push_state(matriz_usuario.copy())

            if event.type == pygame.KEYDOWN:
                # Pausa
                if event.key == pygame.K_ESCAPE:
                    if self.pause and not self.guardar:
                        self.pause = False
                        self.guardar = False
                    elif self.pause and self.guardar:
                        self.guardar = False
                        self._user_text = ""
                    else:
                        self.pause = True
                # Ingresar texto al presionar cualquier tecla
                if self.pause and self.guardar:
                    if event.key == pygame.K_BACKSPACE:
                        self._user_text = self._user_text[0:-1]
                    else:
                        if len(self._user_text) <= 27:
                            self._user_text += event.unicode

                # Resetear dibujo
                if event.key == pygame.K_r:
                    # Resetear matriz
                    matriz_usuario[:] = np.zeros_like(matriz_usuario)
                    for i in range(puzzle_size):
                        for j in range(puzzle_size):
                            if self.obj_square[i][j].isFilled():
                                self.obj_square[i][j].changeImage()

                if event.key == pygame.K_z:     #deshacer
                    new_state = self.history.undo()
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
        surface_bg_image = pygame.image.load("Gráfica/Recursos/Sprites/Crear/cr_overlay_lienzo.png")
        surface_bg_image = pygame.transform.scale(surface_bg_image, (256*WINDOW_SCALE, 240*WINDOW_SCALE))
        self.Surface_bg.blit(surface_bg_image, (0,0))

        for i in range(puzzle_size):
            for j in range(puzzle_size):
                # Esconder si está fuera de pantalla
                """
                if self.obj_square[i][j].rec.y < (62 * WINDOW_SCALE) or self.obj_square[i][j].rec.y > (
                        220 * WINDOW_SCALE) or self.obj_square[i][j].rec.x < (54 * WINDOW_SCALE) or self.obj_square[i][
                    j].rec.x > (210 * WINDOW_SCALE):
                    self.obj_square[i][j].setAlpha(0)
                else:
                    self.obj_square[i][j].setAlpha(255)
                """
                # Añadir a pantalla
                self.Surface_bg.blit(self.obj_square[i][j].image,
                                     (self.obj_square[i][j].getPos()[0], self.obj_square[i][j].getPos()[1]))

        # Añadir bordes a la grilla
        for i in range(puzzle_size):
            # Bordes Horizontales
            pos_x = self.obj_square[0][i].getPos()[0]
            height = (8*puzzle_size + 21)*WINDOW_SCALE
            borde = pygame.image.load("Gráfica/Recursos/Sprites/Jugar/lvl_bordes_grilla.png")
            borde = pygame.transform.scale(borde, (8 * WINDOW_SCALE, 8 * WINDOW_SCALE))
            self.Surface_bg.blit(borde, (pos_x, 16 * WINDOW_SCALE))
            self.Surface_bg.blit(borde, (pos_x, height))

            #Bordes Verticales

            pos_y = self.obj_square[i][0].getPos()[1]
            width = (8*puzzle_size + 13)*WINDOW_SCALE
            bordeV = pygame.transform.rotate(borde, 90)
            self.Surface_bg.blit(bordeV, (8*WINDOW_SCALE, pos_y))
            self.Surface_bg.blit(bordeV, (width, pos_y))

        # Añadir esquinas a la grilla
        esquina = pygame.image.load("Gráfica/Recursos/Sprites/Jugar/lvl_esquinas_grilla.png")
        esquina = pygame.transform.scale(esquina, (8*WINDOW_SCALE, 8*WINDOW_SCALE))
        esquinaUR = pygame.transform.rotate(esquina, -90)
        esquinaDR = pygame.transform.rotate(esquina, 180)
        esquinaDL = pygame.transform.rotate(esquina, 90)
        self.Surface_bg.blit(esquina, (10*WINDOW_SCALE, 18*WINDOW_SCALE))
        self.Surface_bg.blit(esquinaUR, (self.obj_square[0][puzzle_size - 1].getPos()[0]+5*WINDOW_SCALE, 18 * WINDOW_SCALE))
        self.Surface_bg.blit(esquinaDR, (self.obj_square[0][puzzle_size - 1].getPos()[0]+5*WINDOW_SCALE, self.obj_square[puzzle_size - 1][0].getPos()[1]+5*WINDOW_SCALE))
        self.Surface_bg.blit(esquinaDL, (10*WINDOW_SCALE,self.obj_square[puzzle_size - 1][0].getPos()[1] + 5 * WINDOW_SCALE))


        ################ HIGHLIGHT SQUARES ################
        if not self.pause:
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

        # Añadir cuadro para minimapa
        minimapImage = pygame.image.load("Gráfica/Recursos/Sprites/Jugar/Indicador_vista_previa.png")
        minimapImage = pygame.transform.scale(minimapImage,(32*WINDOW_SCALE, 32*WINDOW_SCALE))
        self.Surface_bg.blit(minimapImage, (220*WINDOW_SCALE, 20*WINDOW_SCALE))

        # Añadir cuadro para colores
        monocolorImage = pygame.image.load("Gráfica/Recursos/Sprites/Jugar/lvl_mono_relleno_selector.png")
        monocolorImage = pygame.transform.scale(monocolorImage, (24*WINDOW_SCALE, 120*WINDOW_SCALE))
        self.Surface_bg.blit(monocolorImage, (228*WINDOW_SCALE, 67*WINDOW_SCALE))

        # Añadir botón de menu
        self.Surface_bg.blit(self.Button_Menu.image, (self.Button_Menu.getPos()))

        # Pausa
        if self.pause and self.guardar:
            # Dibujar rectangulo con alpha
            s = pygame.Surface((256*WINDOW_SCALE, 240*WINDOW_SCALE))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            self.Surface_bg.blit(s, (0, 0))

            # Dibujar cuadro
            var_image = pygame.transform.scale(pygame.image.load("Gráfica/Recursos/Sprites/Crear/cr_popup_guardar.png"),(206 * WINDOW_SCALE, 86 * WINDOW_SCALE))
            self.Surface_bg.blit(var_image, (25 * WINDOW_SCALE, 70 * WINDOW_SCALE))

            # Dibujar botones
            self.Surface_bg.blit(self.Button_GuardarySalir.image,self.Button_GuardarySalir.getPos())
            self.Surface_bg.blit(self.Button_Cancelar.image, self.Button_Cancelar.getPos())

            # Ingresar texto
            text_surface = Font_CutebitmapismA_mediumsize.render(self._user_text, False, (255,255,255))
            self.Surface_bg.blit(text_surface,(43*WINDOW_SCALE,98*WINDOW_SCALE))
        elif self.pause:
            # Dibujar rectangulo con alpha
            s = pygame.Surface((256*WINDOW_SCALE, 240*WINDOW_SCALE))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            self.screen.blit(s, (0, 0))

            # Dibujar cuadro
            var_image = pygame.transform.scale(pygame.image.load("Gráfica/Recursos/Sprites/Crear/cr_popup_pausa.png"),(158 * WINDOW_SCALE, 94 * WINDOW_SCALE))
            self.screen.blit(var_image, (30 * WINDOW_SCALE, 70 * WINDOW_SCALE))

            # Dibujar botones
            self.screen.blit(self.Button_Guardar.image,self.Button_Guardar.getPos())
            self.screen.blit(self.Button_MenuPrincipal.image, self.Button_MenuPrincipal.getPos())
            self.screen.blit(self.Button_CerrarJuego.image, self.Button_CerrarJuego.getPos())

        pygame.display.flip()
        ################# DRAW ################