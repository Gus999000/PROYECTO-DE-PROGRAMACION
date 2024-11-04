import pygame as pg
from Gráfica.Button import Button
from Gráfica.draw_text import draw_text
from Lógica.comparar_matriz import matriz_usuario
from Lógica.comparar_matriz import is_solved
from Gráfica.Matriz_numeros import matriz_numeros
from Gráfica.Square import Square

WINDOW_SCALE = 3
puzzle_size = 20

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
    square_size = (160*WINDOW_SCALE)/puzzle_size
    obj_square = [[Square((i * square_size) + (56*WINDOW_SCALE), (j * square_size) + 64*WINDOW_SCALE, square_size) for i in range(puzzle_size)] for j in range(puzzle_size)]
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

    # Añadir cuadrados al grupo de sprites, para así poder trabajar con ellos de forma conjunta
    group_number_hints_up = pg.sprite.Group()
    group_number_hints_left = pg.sprite.Group()
    for i in range(number_hints.get_puzzle_size()):
        for j in range(number_hints.get_max_numbers()):
            group_number_hints_up.add(Square((56 + (i * 8)) * WINDOW_SCALE,  (48 - (j * 8)) * WINDOW_SCALE, square_size))
            group_number_hints_left.add(Square((40 - (j * 8)) * WINDOW_SCALE, (64 + (i * 8)) * WINDOW_SCALE, square_size))
    ############### RELLENAR CON MATRIZ DE EJEMPLO ###############
    matriz_ejemplo1 =  [[0], [0], [1,2,1,1,3,1,2], [7], [9], [10], [1, 2, 5], [1, 3, 6], [1, 4, 1], [1, 5, 1], [11, 1], [11, 1], [11, 1], [11, 1], [13], [11], [4, 4], [2, 2], [0], [0],[0]]
    matriz_ejemplo2 = [[0], [0], [1,1,2,3,4,5,6,7,8,9], [2, 8], [2, 1, 8], [5, 8], [5, 7], [4, 6], [4, 6], [5, 7], [14], [15], [14], [11], [1, 1], [1, 1], [6], [0], [0], [0],[0]]
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
                    # PUZZLE
                    if (56*WINDOW_SCALE <= pg.mouse.get_pos()[0] <= 210*WINDOW_SCALE) and (60*WINDOW_SCALE <= pg.mouse.get_pos()[1] <= 220*WINDOW_SCALE):
                        for square in group_squares:
                            square.updatePos(square.rec.x, square.rec.y - ((160*WINDOW_SCALE)/puzzle_size))
                    # GRILLA DE NUMEROS
                    if (56 * WINDOW_SCALE <= pg.mouse.get_pos()[0] <= 215 * WINDOW_SCALE) and (8 * WINDOW_SCALE <= pg.mouse.get_pos()[1] <= 55 * WINDOW_SCALE):
                        if 48*WINDOW_SCALE > group_number_hints_up.sprites()[0].getPos()[1] or group_number_hints_up.sprites()[0].getPos()[1] > 55*WINDOW_SCALE:
                            for square in group_number_hints_up:
                                square.updatePos(square.rec.x, square.rec.y - ((160 * WINDOW_SCALE) / puzzle_size))


                if event.key == pg.K_DOWN:
                    if (56 * WINDOW_SCALE <= pg.mouse.get_pos()[0] <= 210 * WINDOW_SCALE) and (60 * WINDOW_SCALE <= pg.mouse.get_pos()[1] <= 220 * WINDOW_SCALE):
                        for square in group_squares:
                            square.updatePos(square.rec.x, square.rec.y + ((160*WINDOW_SCALE)/puzzle_size))
                    # GRILLA DE NUMEROS
                    if (56 * WINDOW_SCALE <= pg.mouse.get_pos()[0] <= 215 * WINDOW_SCALE) and (8 * WINDOW_SCALE <= pg.mouse.get_pos()[1] <= 55 * WINDOW_SCALE):
                        if 7 * WINDOW_SCALE > group_number_hints_up.sprites()[number_hints.get_max_numbers()-1].getPos()[1] or group_number_hints_up.sprites()[number_hints.get_max_numbers()-1].getPos()[1] > 16 * WINDOW_SCALE:
                            for square in group_number_hints_up:
                                square.updatePos(square.rec.x, square.rec.y + ((160*WINDOW_SCALE)/puzzle_size))


                if event.key == pg.K_RIGHT:
                    if (56 * WINDOW_SCALE <= pg.mouse.get_pos()[0] <= 210 * WINDOW_SCALE) and (60 * WINDOW_SCALE <= pg.mouse.get_pos()[1] <= 220 * WINDOW_SCALE):
                        for square in group_squares:
                            square.updatePos(square.rec.x + ((160*WINDOW_SCALE)/puzzle_size), square.rec.y)
                    # GRILLA DE NUMEROS
                    if (0 <= pg.mouse.get_pos()[0] <= 47 * WINDOW_SCALE) and (64 * WINDOW_SCALE <= pg.mouse.get_pos()[1] <= 224 * WINDOW_SCALE):
                        if 0 * WINDOW_SCALE > group_number_hints_left.sprites()[number_hints.get_max_numbers() - 1].getPos()[0] or group_number_hints_left.sprites()[number_hints.get_max_numbers() - 1].getPos()[0] > 9 * WINDOW_SCALE:
                            for square in group_number_hints_left:
                                square.updatePos(square.rec.x + ((160*WINDOW_SCALE)/puzzle_size), square.rec.y)

                if event.key == pg.K_LEFT:
                    if (56 * WINDOW_SCALE <= pg.mouse.get_pos()[0] <= 210 * WINDOW_SCALE) and (60 * WINDOW_SCALE <= pg.mouse.get_pos()[1] <= 220 * WINDOW_SCALE):
                        for square in group_squares:
                            square.updatePos(square.rec.x - ((160*WINDOW_SCALE)/puzzle_size), square.rec.y)
                    # GRILLA DE NUMEROS
                    if (0 <= pg.mouse.get_pos()[0] <= 47 * WINDOW_SCALE) and (64 * WINDOW_SCALE <= pg.mouse.get_pos()[1] <= 224 * WINDOW_SCALE):
                        if 39 * WINDOW_SCALE > group_number_hints_left.sprites()[0].getPos()[0] or group_number_hints_left.sprites()[0].getPos()[0] > 46 * WINDOW_SCALE:
                            for square in group_number_hints_left:
                                square.updatePos(square.rec.x - ((160*WINDOW_SCALE)/puzzle_size), square.rec.y)


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
        for square in group_number_hints_up:
            if square.rec.y < (8*WINDOW_SCALE) or square.rec.y > (55*WINDOW_SCALE):
                square.setAlpha(0)
            else:
                square.setAlpha(255)
            Surface_bg.blit(square.image, square.getPos())

        for i in range(number_hints.get_puzzle_size()):
            for j in range(number_hints.get_max_numbers()):
                if number_hints.get_matriz_columna_value(i,j) != 0:
                    pos_x = (group_number_hints_up.sprites()[(i*number_hints.get_max_numbers()) + j].getPos()[0] + (2*WINDOW_SCALE))
                    pos_y = (group_number_hints_up.sprites()[(i*number_hints.get_max_numbers()) + j].getPos()[1] - (1*WINDOW_SCALE))

                    if 4*WINDOW_SCALE<= pos_y <= 54*WINDOW_SCALE:
                        draw_text(f"{number_hints.get_matriz_columna_value(i,j)}", "Arial", (255,255,255), 8*WINDOW_SCALE, pos_x, pos_y,Surface_bg)




        # Filas
        for square in group_number_hints_left:
            if square.rec.x < 0 or square.rec.x > (47*WINDOW_SCALE):
                square.setAlpha(0)
            else:
                square.setAlpha(255)
            Surface_bg.blit(square.image, square.getPos())

        for i in range(number_hints.get_puzzle_size()):
            for j in range(number_hints.get_max_numbers()):
                if number_hints.get_matriz_fila_value(i, j) != 0:
                    pos_x = group_number_hints_left.sprites()[(i*number_hints.get_max_numbers()) + j].getPos()[0] + (2*WINDOW_SCALE)
                    pos_y = group_number_hints_left.sprites()[(i * number_hints.get_max_numbers()) + j].getPos()[1] - (1 * WINDOW_SCALE)

                    if 0 <= pos_x <= 49*WINDOW_SCALE:
                        draw_text(f"{number_hints.get_matriz_fila_value(i,j)}", "Arial", (255,255,255), 8*WINDOW_SCALE, pos_x, pos_y,Surface_bg)

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