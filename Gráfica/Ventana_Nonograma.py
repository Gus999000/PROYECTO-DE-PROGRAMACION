import pygame as pg
from Gráfica.Button import Button
from Gráfica.draw_text import draw_text
from Lógica.comparar_matriz import matriz_usuario
from Lógica.comparar_matriz import is_solved
from Gráfica.Matriz_numeros import matriz_numeros

WINDOW_SCALE = 3

class Square(pg.sprite.Sprite):

    Filled = False
    x = 0
    y = 0
    size = 0
    def __init__(self, pos_x, pos_y, scale):
        #Hereda pg.sprite.Sprite
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.size = scale
        # {pos_x, pox_y, width, height}
        self.rec = pg.Rect(pos_x+56*WINDOW_SCALE,pos_y+64*WINDOW_SCALE,scale,scale)
        if not self.Filled:
            self.image = pg.image.load("Gráfica/resources/Square.png")
        else:
            self.image = pg.image.load("Gráfica/resources/SquareFill.png")

        self.image = pg.transform.scale(self.image,(scale,scale))

    def isColliding(self):
        return self.rec.collidepoint(pg.mouse.get_pos())

    def changeImage(self):
        if self.Filled:
            self.image = pg.image.load("Gráfica/resources/Square.png")
            self.Filled = False
        else:
            self.image = pg.image.load("Gráfica/resources/SquareFill.png")
            self.Filled = True
        self.image = pg.transform.scale(self.image, (self.rec[2], self.rec[2]))

    def setAlpha(self, alpha):
        self.image.set_alpha(alpha)

    def updatePos(self,new_x, new_y):
        self.rec.topleft = (new_x,new_y)

    def isFilled(self):
        if self.Filled:
            return 1
        else:
            return 0

    def getPos(self):
        return self.rec


def mainloop():
    # Crear Ventana
    # 256 x 240
    screen_size = (256*WINDOW_SCALE,240*WINDOW_SCALE)
    screen = pg.display.set_mode(screen_size)

    pg.display.flip()

    # Crear color de fondo
    Surface_bg = pg.surface.Surface((300*WINDOW_SCALE,300*WINDOW_SCALE))
    Surface_bg.fill((0,0,255))

    # Ingresar tamaño del puzzle y el cuadrado
    puzzle_size = 20
    square_size = (160*WINDOW_SCALE)/puzzle_size
    obj_square = [[Square(i * square_size, j * square_size, square_size) for i in range(puzzle_size)] for j in range(puzzle_size)]
    # Añadir cuadrados al grupo de sprites, para así poder trabajar con ellos de forma conjunta
    group_squares = pg.sprite.Group()
    for i in range(puzzle_size):
        for j in range(puzzle_size):
            group_squares.add(obj_square[i][j])

    """
    Ventana Original de la grilla (256x240) --> 160x160
    Puzzle 20x20 --> 24x24px    (20x24 = 480) --> 480/20 = 24
    Puzzle 10x10 --> 48x48px    (10x?  = 480) --> 480/10 = 48
    Puzzle 5x5   -->            (5x?   ? 480) --> 480/5 = 96
    Por lo tanto, el tamaño de cada cuadrado será igual a nuestra constante 480 dividido el tamaño del puzzle
    
    """

    ########## Crear interfaz ##########
    # Grilla de numeros
    Surface_number_up = pg.surface.Surface((160*WINDOW_SCALE,48*WINDOW_SCALE))
    Surface_number_up.fill((18,100,114))

    Surface_number_left = pg.surface.Surface((48*WINDOW_SCALE,160 * WINDOW_SCALE))
    Surface_number_left.fill((18, 100, 114))

    number_hints = matriz_numeros(puzzle_size)
    ############### RELLENAR CON MATRIZ DE EJEMPLO ###############
    matriz_ejemplo1 =  [[0], [0], [3], [7], [9], [10], [1, 2, 5], [1, 3, 6], [1, 4, 1], [1, 5, 1], [11, 1], [11, 1], [11, 1], [11, 1], [13], [11], [4, 4], [2, 2], [0], [0]]
    matriz_ejemplo2 = [[0], [0], [2], [2, 8], [2, 1, 8], [5, 8], [5, 7], [4, 6], [4, 6], [5, 7], [14], [15], [14], [11], [1, 1], [1, 1], [6], [0], [0], [0]]
    number_hints.set_matriz_filas(matriz_ejemplo1)
    number_hints.set_matriz_columnas(matriz_ejemplo2)
    ############### RELLENAR CON MATRIZ DE EJEMPLO ###############

    # Botón de zoom
    Button_Zoom = Button(225*WINDOW_SCALE, 49*WINDOW_SCALE, 5*WINDOW_SCALE, "Gráfica/resources/Zoom.png")

    # Botón de antizoom
    Button_AntiZoom = Button(242*WINDOW_SCALE,49*WINDOW_SCALE,5*WINDOW_SCALE, "Gráfica/resources/Zoom.png")

    # Boton de menú
    Button_Menu = Button(228*WINDOW_SCALE, 204*WINDOW_SCALE, 24*WINDOW_SCALE, "Gráfica/resources/Menu.png")

    # Boton de pistas
    Button_Tips = Button(228*WINDOW_SCALE, 60*WINDOW_SCALE, 24*WINDOW_SCALE, "Gráfica/resources/Tips.png")

    # Colores
    Button_Colours = [[Button(((j*8)+232)*WINDOW_SCALE,((i*8)+88)*WINDOW_SCALE,8*WINDOW_SCALE,"Gráfica/resources/Square.png") for i in range(14)] for j in range(2)]

    ########## Crear interfaz ##########


    # Creación de la cámara para Zoom
    camera_group = pg.sprite.Group()

    # Main Loop
    running = True
    while running:

        # Eventos
        for event in pg.event.get():
            # SALIR
            if event.type == pg.QUIT:
                running = False
            # PRESIONAR CUADRADOS
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in range(puzzle_size):
                    for j in range(puzzle_size):
                        if obj_square[i][j].isColliding():
                            obj_square[i][j].changeImage()
                            matriz_usuario[i][j] = obj_square[i][j].isFilled()
                            if is_solved(matriz_usuario):
                                print('Has resuelto el nonograma!!!!')
            # MOVER CÁMARA DE PUZZLE
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    for square in group_squares:
                        square.updatePos(square.rec.x, square.rec.y - (8 * WINDOW_SCALE))
                if event.key == pg.K_DOWN:
                    for square in group_squares:
                        square.updatePos(square.rec.x, square.rec.y + (8*WINDOW_SCALE))
                if event.key == pg.K_RIGHT:
                    for square in group_squares:
                        square.updatePos(square.rec.x + (8*WINDOW_SCALE), square.rec.y)
                if event.key == pg.K_LEFT:
                    for square in group_squares:
                        square.updatePos(square.rec.x - (8 * WINDOW_SCALE), square.rec.y)

        ################# DRAW ################
        # Cuadrados grilla
        screen.blit(Surface_bg, (0,0))
        # Dibujar tamaño del cuadro de la grilla
        pg.draw.rect(Surface_bg, (177,226,231), (52*WINDOW_SCALE, 60*WINDOW_SCALE, 168*WINDOW_SCALE, 168*WINDOW_SCALE))

        for i in range(puzzle_size):
            for j in range(puzzle_size):
                # Esconder si está fuera de pantalla
                if obj_square[i][j].rec.y < (62 * WINDOW_SCALE) or obj_square[i][j].rec.y > (220 * WINDOW_SCALE) or obj_square[i][j].rec.x < (54 * WINDOW_SCALE) or obj_square[i][j].rec.x > (210 * WINDOW_SCALE):
                    obj_square[i][j].setAlpha(0)
                else:
                    obj_square[i][j].setAlpha(255)

                # Añadir a pantalla
                Surface_bg.blit(obj_square[i][j].image, (obj_square[i][j].getPos()[0], obj_square[i][j].getPos()[1]))


        ## Interfaz
        # Añadir cuadro para timer
        pg.draw.rect(Surface_bg, (0,0,0), (4*WINDOW_SCALE,12*WINDOW_SCALE,48*WINDOW_SCALE,48*WINDOW_SCALE))
        draw_text("timer", "Arial", (255,255,255), 10*WINDOW_SCALE, 20*WINDOW_SCALE, 26*WINDOW_SCALE,Surface_bg)

        # Añadir cuadro para minimapa
        pg.draw.rect(Surface_bg, (84,181,190), (220*WINDOW_SCALE, 12*WINDOW_SCALE, 32*WINDOW_SCALE, 32*WINDOW_SCALE))

        # Añadir cuadro para colores
        pg.draw.rect(Surface_bg, (16,92,106), (228*WINDOW_SCALE,84*WINDOW_SCALE,24*WINDOW_SCALE,120*WINDOW_SCALE))

        # Cuadro derecha, Colores, Botones
        #pg.draw.rect(Surface_bg, (235,235,35), (208*WINDOW_SCALE, 0*WINDOW_SCALE,48*WINDOW_SCALE,240*WINDOW_SCALE))

        # Añadir Números Arriba
        Surface_bg.blit(Surface_number_up, (56*WINDOW_SCALE,8*WINDOW_SCALE))
        # Añadir Números Izquierda
        Surface_bg.blit(Surface_number_left, (0, 64 * WINDOW_SCALE))

        # Dibujar Numeros pista
        # Columnas
        for i in range(number_hints.get_puzzle_size()):
            for j in range(number_hints.get_max_numbers()):
                if j < 6:
                    #Surface_bg.blit(obj_square[i][j].image,
                    #                ((56 + (i * 8)) * WINDOW_SCALE, (48 - (j * 8)) * WINDOW_SCALE))
                    if number_hints.get_matriz_columna_value(i,j) != 0:
                        draw_text(f"{number_hints.get_matriz_columna_value(i,j)}", "Arial", (255,255,255), 8*WINDOW_SCALE, (58+(i*8))*WINDOW_SCALE, (47 -(j*8))*WINDOW_SCALE,Surface_bg)

        # Filas
        for i in range(number_hints.get_puzzle_size()):
            for j in range(number_hints.get_max_numbers()):
                if j < 6:
                    #Surface_bg.blit(obj_square[i][j].image,
                    #                ((40 - (j * 8)) * WINDOW_SCALE, (64 + (i * 8)) * WINDOW_SCALE))
                    if number_hints.get_matriz_fila_value(i, j) != 0:
                        draw_text(f"{number_hints.get_matriz_fila_value(i,j)}", "Arial", (255,255,255), 8*WINDOW_SCALE, (42-(j*8))*WINDOW_SCALE, (63 +(i*8))*WINDOW_SCALE,Surface_bg)


        # Añadir botón de menu
        Surface_bg.blit(Button_Menu.image, (Button_Menu.getPos()))
        # Añadir botón de pistas
        Surface_bg.blit(Button_Tips.image, (Button_Tips.getPos()))

        #Añadir botón de zoom
        Surface_bg.blit(Button_Zoom.image, (Button_Zoom.getPos()))
        # Añadir botón de antizoom
        Surface_bg.blit(Button_AntiZoom.image, (Button_AntiZoom.getPos()))
        # Añadir logo de zoom
        pg.draw.rect(Surface_bg, (47,110,117), (232*WINDOW_SCALE,48*WINDOW_SCALE,8*WINDOW_SCALE,8*WINDOW_SCALE))
        # Añadir botones de colores
        for i in range(14):
            for j in range(2):
                Surface_bg.blit(Button_Colours[j][i].image, (Button_Colours[j][i].getPos()))

        pg.display.flip()
        ################# DRAW ################
mainloop()