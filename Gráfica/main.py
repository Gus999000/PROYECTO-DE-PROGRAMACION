import pygame as pg

class Square(pg.sprite.Sprite):

    Filled = False

    def __init__(self, pos_x, pos_y, scale):
        #Hereda pg.sprite.Sprite
        super().__init__()
        # {pos_x, pox_y, width, height}
        self.__rec = [pos_x+160,pos_y+160,scale,scale]
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
    screen_size = (768,672)
    screen = pg.display.set_mode(screen_size)

    pg.display.flip()

    Surface = pg.surface.Surface((800,800))
    Surface.fill((0,0,255))

    # Ingresar tamaño del puzzle y el cuadrado
    puzzle_size = 20

    square_size = 480/puzzle_size
    obj_square = [[Square(i * square_size, j * square_size, square_size) for i in range(puzzle_size)] for j in range(puzzle_size)]
    # Añadir cuadrados al grupo de sprites, para así poder trabajar con ellos de forma conjunta
    group_squares = pg.sprite.Group()
    for i in range(puzzle_size):
        for j in range(puzzle_size):
            group_squares.add(obj_square[i][j])

    """
    Ventana --> 160x160
    Puzzle 20x20 --> 24x24px    (20x24 = 480) --> 480/20 = 24
    Puzzle 10x10 --> 48x48px    (10x?  = 480) --> 480/10 = 48
    Puzzle 5x5   -->            (5x?   ? 480) --> 480/5 = 96
    Por lo tanto, el tamaño de cada cuadrado será igual a nuestra constante 480 dividido el tamaño del puzzle
    
    """

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

        #draw
        screen.blit(Surface, (0,0))
        for i in range(puzzle_size):
            for j in range(puzzle_size):
                Surface.blit(obj_square[i][j].image, (obj_square[i][j].getPos()[0], obj_square[i][j].getPos()[1]))
        pg.display.flip()

main()