import pygame as pg
from Gráfica.Button import Button
from Gráfica.draw_text import draw_text
from Lógica.comparar_matriz import matriz_usuario
from Lógica.comparar_matriz import is_solved
from Lógica.archivos_npz import guardarNPZ
from Lógica.archivos_npz import cargarNPZ

WINDOW_SCALE = 3

class Square(pg.sprite.Sprite):

    Filled = False

    def __init__(self, pos_x, pos_y, scale):
        #Hereda pg.sprite.Sprite
        super().__init__()
        # {pos_x, pox_y, width, height}
        self.__rec = [pos_x+56*WINDOW_SCALE,pos_y+64*WINDOW_SCALE,scale,scale]
        if not self.Filled:
            self.image = pg.image.load("Gráfica/resources/Square.png")
        else:
            self.image = pg.image.load("Gráfica/resources/SquareFill.png")

        self.image = pg.transform.scale(self.image,(scale,scale))

    def isColliding(self):
        CollideBox = pg.Rect(self.__rec[0], self.__rec[1], self.__rec[2], self.__rec[3])
        if CollideBox.collidepoint(pg.mouse.get_pos()):
            return True
        else:
            return False

    def changeImage(self):
        if self.Filled:
            self.image = pg.image.load("Gráfica/resources/Square.png")
            self.image = pg.transform.scale(self.image, (self.__rec[2], self.__rec[2]))
            self.Filled = False
            pass
        else:
            self.image = pg.image.load("Gráfica/resources/SquareFill.png")
            self.image = pg.transform.scale(self.image, (self.__rec[2], self.__rec[2]))
            self.Filled = True
            pass

    def isFilled(self):
        if self.Filled:
            return 1
        else:
            return 0

    def getPos(self):
        return self.__rec


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
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in range(puzzle_size):
                    for j in range(puzzle_size):
                        if obj_square[i][j].isColliding():
                            obj_square[i][j].changeImage()
                            matriz_usuario[i][j] = obj_square[i][j].isFilled()
                            if is_solved(matriz_usuario):
                                print('Has resuelto el nonograma!!!!')

        ################# DRAW ################
        # Cuadrados grilla
        screen.blit(Surface_bg, (0,0))
        # Dibujar tamaño del cuadro de la grilla
        pg.draw.rect(Surface_bg, (177,226,231), (52*WINDOW_SCALE, 60*WINDOW_SCALE, 168*WINDOW_SCALE, 168*WINDOW_SCALE))

        for i in range(puzzle_size):
            for j in range(puzzle_size):
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