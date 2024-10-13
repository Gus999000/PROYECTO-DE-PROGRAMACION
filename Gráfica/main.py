import pygame as pg
from Button import Button
from draw_text import draw_text

WINDOW_SCALE = 3

class Square(pg.sprite.Sprite):

    Filled = False

    def __init__(self, pos_x, pos_y, scale):
        #Hereda pg.sprite.Sprite
        super().__init__()
        # {pos_x, pox_y, width, height}
        self.__rec = [pos_x+48*WINDOW_SCALE,pos_y+80*WINDOW_SCALE,scale,scale]
        if not self.Filled:
            self.image = pg.image.load("resources/Square.png")
        else:
            self.image = pg.image.load("resources/SquareFill.png")

        self.image = pg.transform.scale(self.image,(scale,scale))

    def isColliding(self):
        CollideBox = pg.Rect(self.__rec[0], self.__rec[1], self.__rec[2], self.__rec[3])
        if CollideBox.collidepoint(pg.mouse.get_pos()):
            return True
        else:
            return False

    def changeImage(self):
        if self.Filled:
            self.image = pg.image.load("resources/Square.png")
            self.image = pg.transform.scale(self.image, (self.__rec[2], self.__rec[2]))
            self.Filled = False
            pass
        else:
            self.image = pg.image.load("resources/SquareFill.png")
            self.image = pg.transform.scale(self.image, (self.__rec[2], self.__rec[2]))
            self.Filled = True
            pass

    def getPos(self):
        return self.__rec


def main():

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
    Surface_number_up = pg.surface.Surface((160*WINDOW_SCALE,80*WINDOW_SCALE))
    Surface_number_up.fill((0,255,0))

    Surface_number_left = pg.surface.Surface((48*WINDOW_SCALE,160 * WINDOW_SCALE))
    Surface_number_left.fill((0, 255, 0))

    # Boton de deshacer
    Button_Undo = Button(213*WINDOW_SCALE, 34*WINDOW_SCALE, 16*WINDOW_SCALE, "resources/Undo.png")

    # Botón de zoom
    Button_Zoom = Button(235*WINDOW_SCALE, 34*WINDOW_SCALE, 16*WINDOW_SCALE, "resources/Zoom.png")

    # Boton de menú
    Button_Menu = Button(213*WINDOW_SCALE, 5*WINDOW_SCALE,16*WINDOW_SCALE, "resources/Menu.png")

    # Boton de pistas
    Button_Tips = Button(235*WINDOW_SCALE, 5*WINDOW_SCALE, 16*WINDOW_SCALE, "resources/Tips.png")

    # Boton de lapiz
    Button_Draw = Button(213*WINDOW_SCALE, 64*WINDOW_SCALE, 16*WINDOW_SCALE, "resources/Pencil.png")

    # Boton de cruz
    Button_Cross = Button(235 * WINDOW_SCALE, 64 * WINDOW_SCALE, 16 * WINDOW_SCALE, "resources/Cross.png")

    # Colores
    Button_Colours = [Button(225*WINDOW_SCALE,((i*16)+96)*WINDOW_SCALE,16*WINDOW_SCALE,"resources/Square.png") for i in range(8)]

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

        ################# DRAW ################
        # Cuadrados grilla
        screen.blit(Surface_bg, (0,0))
        for i in range(puzzle_size):
            for j in range(puzzle_size):
                Surface_bg.blit(obj_square[i][j].image, (obj_square[i][j].getPos()[0], obj_square[i][j].getPos()[1]))

        ## Interfaz
        # Añadir cuadro para timer
        pg.draw.rect(Surface_bg, (0,0,0), (0,40*WINDOW_SCALE,48*WINDOW_SCALE,40*WINDOW_SCALE))
        draw_text("timer", "Arial", (255,255,255), 10*WINDOW_SCALE, 15*WINDOW_SCALE, 55*WINDOW_SCALE,Surface_bg)

        # Cuadro derecha, Colores, Botones
        pg.draw.rect(Surface_bg, (235,235,35), (208*WINDOW_SCALE, 0*WINDOW_SCALE,48*WINDOW_SCALE,240*WINDOW_SCALE))

        # Añadir Números Arriba
        Surface_bg.blit(Surface_number_up, (48*WINDOW_SCALE,0))
        # Añadir Números Izquierda
        Surface_bg.blit(Surface_number_left, (0, 80 * WINDOW_SCALE))
        # Añadir boton de undo
        Surface_bg.blit(Button_Undo.image, (Button_Undo.getPos()))
        #Añadir botón de zoom
        Surface_bg.blit(Button_Zoom.image, (Button_Zoom.getPos()))
        # Añadir botón de menu
        Surface_bg.blit(Button_Menu.image, (Button_Menu.getPos()))
        # Añadir botón de pistas
        Surface_bg.blit(Button_Tips.image, (Button_Tips.getPos()))
        # Añadir botón de lapiz
        Surface_bg.blit(Button_Draw.image, (Button_Draw.getPos()))
        # Añadir botón de cruz
        Surface_bg.blit(Button_Cross.image, (Button_Cross.getPos()))

        # Añadir botones de colores
        for i in range(8):
            Surface_bg.blit(Button_Colours[i].image, (Button_Colours[i].getPos()))

        pg.display.flip()
        ################# DRAW ################

main()