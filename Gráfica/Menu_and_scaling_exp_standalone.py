import pygame, sys

from Gráfica.Button import Button_notScaled, Button_notSquare
from Lógica.Logros import NonogramAchievementTracker
from Lógica.nonograma_info import set_variable

# Setup pygame/ventana
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Testeo Menus')

# forzar pygame a usar escalamiento tipo nearest neighbor
if hasattr(pygame, 'GL_NEAREST'):
    pygame.display.gl_set_attribute(pygame.GL_TEXTURE_MIN_FILTER, pygame.GL_NEAREST)
    pygame.display.gl_set_attribute(pygame.GL_TEXTURE_MAG_FILTER, pygame.GL_NEAREST)

# Res original
ORIGINAL_WIDTH, ORIGINAL_HEIGHT = 256, 240
resolutions = [
    (256, 240),  # Min resolution
    (512, 480),
    (768, 720),
    (1024, 960),
    (1280, 1200),
    (1536, 1440)  # Max resolution
]

# Resolucion inicial y estados
initial_scale = 3  # 768/256 = 3
scale_factor = initial_scale
current_resolution_index = 2  # Index para 768x720 en la lista de resolucioes

screen = pygame.display.set_mode((ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor), RESIZABLE)

# ventana virtual
virtual_screen = pygame.Surface((ORIGINAL_WIDTH, ORIGINAL_HEIGHT))

# Renderizacion de texto
title_font = pygame.font.Font('Gráfica/Recursos/Fonts/16x-Vermin Vibes 1989.ttf', 36)
#font = pygame.font.SysFont('OCR-A Extended', 12, bold=True)
font = pygame.font.Font('Gráfica/Recursos/Fonts/7x-zx-spectrum.ttf', 8)


# opciones en video
display_modes = ["Windowed", "Fullscreen", "Windowed Fullscreen"]
current_display_mode = 0
brightness = 50
selected_option = None
selected_color = None

# UI Colors
ui_colors = [
    {"color": (255, 0, 0), "pos": (80, 140), "selected": False},
    {"color": (0, 255, 0), "pos": (120, 140), "selected": False},
    {"color": (0, 0, 255), "pos": (160, 140), "selected": False}
]

# funcion para escalar superficies con nearest neighbor
def pixel_perfect_scale(surface, scale_factor):
    scaled_size = (surface.get_width() * scale_factor, surface.get_height() * scale_factor)
    return pygame.transform.scale(surface, scaled_size, pygame.Surface(scaled_size))

# modificado draw_text para renderizar texto con su tamaño original
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, False, color)  # Set antialiasing to False for crisp text
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)


def draw_button(surface, text, x, y, width=100, height=20):
    button_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    return button_rect


def draw_arrow(surface, x, y, direction='left'):
    color = (255, 255, 255)
    if direction == 'left':
        points = [(x + 10, y), (x, y + 5), (x + 10, y + 10)]
    else:
        points = [(x, y), (x + 10, y + 5), (x, y + 10)]
    pygame.draw.polygon(surface, color, points)
    return pygame.Rect(x, y, 10, 10)


def change_resolution(new_index):
    global screen, scale_factor, current_resolution_index
    if 0 <= new_index < len(resolutions):
        current_resolution_index = new_index
        new_width, new_height = resolutions[current_resolution_index]
        scale_factor = new_width // ORIGINAL_WIDTH
        screen = pygame.display.set_mode((new_width, new_height), RESIZABLE)
        set_variable(scale_factor)
        return True
    return False


def get_current_resolution():
    width, height = screen.get_size()
    for i, (res_width, res_height) in enumerate(resolutions):
        if width == res_width and height == res_height:
            return i
    return current_resolution_index

# Ventanas
class video_Options():
    def __init__(self, display, gameSateManager):
        self.screen = display
        self.gameSateManager = gameSateManager
        self.click = False
        # actualiza el indice de resolucion
        self.current_resolution_index = get_current_resolution()


        # Botones
        self.buttons = []
        for i in range(6):
            if i%2 == 0:
                self.buttons.append(Button_notScaled(0,0,4*scale_factor,6*scale_factor,"Gráfica/Recursos/Sprites/Opciones/op_boton_flecha_izq.png"))
            else:
                self.buttons.append(Button_notScaled(0, 0, 4*scale_factor, 6*scale_factor, "Gráfica/Recursos/Sprites/Opciones/op_boton_flecha_der.png"))
    def run(self, events):
        global current_display_mode, brightness, selected_option, selected_color, scale_factor
        virtual_screen.fill((0, 0, 0))
        # Fondo
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_detalle_fondo_submenu.png"), (0,0))

        # Texto
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_subtitulo_video.png"), (15, 15))

        # Resolucion
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_opcion_video_resolucion.png"),(20, 40))
        current_res = f"{resolutions[current_resolution_index][0]}x{resolutions[current_resolution_index][1]}"
        draw_text(current_res, font, (255, 255, 255), virtual_screen, 175, 40)

        self.buttons[0].updatePos(130 * scale_factor, 40 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[0].image, (self.buttons[0].getPos()[0] // scale_factor, self.buttons[0].getPos()[1] // scale_factor))
        self.buttons[1].updatePos(230 * scale_factor, 40 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[1].image,(self.buttons[1].getPos()[0] // scale_factor, self.buttons[1].getPos()[1] // scale_factor))


        # Display Mode
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_opcion_video_pantalla.png"),(20, 70))
        draw_text(display_modes[current_display_mode], font, (255, 255, 255), virtual_screen, 175, 70)

        self.buttons[2].updatePos(130 * scale_factor, 70 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[2].image, (self.buttons[2].getPos()[0] // scale_factor, self.buttons[2].getPos()[1] // scale_factor))
        self.buttons[3].updatePos(230 * scale_factor, 70 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[3].image,(self.buttons[3].getPos()[0] // scale_factor, self.buttons[3].getPos()[1] // scale_factor))

        # Control de Brillo
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_opcion_video_brillo.png"), (20, 100))

        self.buttons[4].updatePos(130 * scale_factor, 100 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[4].image, (self.buttons[4].getPos()[0] // scale_factor, self.buttons[4].getPos()[1] // scale_factor))
        self.buttons[5].updatePos(230 * scale_factor, 100 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[5].image,(self.buttons[5].getPos()[0] // scale_factor, self.buttons[5].getPos()[1] // scale_factor))

        pygame.draw.rect(virtual_screen, (100, 100, 100), (140, 100, 80, 10))
        pygame.draw.rect(virtual_screen, (255, 255, 255), (140, 100, brightness * 0.8, 10))

        # Elejir color de UI
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_opcion_video_colorui.png"),(20, 130))
        color_positions = [(100, 130), (140, 130), (180, 130)]

        for i, color_option in enumerate(ui_colors):
            color_option["pos"] = color_positions[i]
            pygame.draw.rect(virtual_screen, color_option["color"],
                             (color_option["pos"][0], color_option["pos"][1], 20, 20))
            if color_option["selected"]:
                pygame.draw.rect(virtual_screen, (255, 255, 255),
                                 (color_option["pos"][0] - 2, color_option["pos"][1] - 2, 24, 24), 2)

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.gameSateManager.set_state('optionsMenu')

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if self.buttons[0].isColliding():
                        change_resolution(current_resolution_index - 1)
                    if self.buttons[1].isColliding():
                        change_resolution(current_resolution_index + 1)
                    if self.buttons[2].isColliding():
                        current_display_mode = (current_display_mode - 1) % len(display_modes)
                    if self.buttons[3].isColliding():
                        current_display_mode = (current_display_mode + 1) % len(display_modes)
                    if self.buttons[4].isColliding():
                        brightness = max(0, brightness - 5)
                    if self.buttons[5].isColliding():
                        brightness = min(100, brightness + 5)

                    # seleccion de colores
                    for color_option in ui_colors:
                        color_rect = pygame.Rect(color_option["pos"][0], color_option["pos"][1], 20, 20)
                        if color_rect.collidepoint(scaled_mx, scaled_my):
                            for c in ui_colors:
                                c["selected"] = False
                            color_option["selected"] = True
                            selected_color = color_option["color"]

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)

class options_Menu():
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameSateManager = gameStateManager
        self.click = False


        # Botones
        self.Button_controles = Button_notScaled(65*scale_factor, 30*scale_factor, 72*scale_factor,8*scale_factor,"Gráfica/Recursos/Sprites/Opciones/op_opcion_controles.png")
        self.Button_video = Button_notScaled(65 * scale_factor, 30 * scale_factor, 40 * scale_factor,
                                                 8 * scale_factor,
                                                 "Gráfica/Recursos/Sprites/Opciones/op_opcion_video.png")
        self.Button_audio = Button_notScaled(65 * scale_factor, 30 * scale_factor, 40 * scale_factor,
                                                 8 * scale_factor,
                                                 "Gráfica/Recursos/Sprites/Opciones/op_opcion_audio.png")

    def run(self, events):
        global scale_factor
        virtual_screen.fill((0, 0, 0))

        # Fondo
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_detalle_fondo_menu.png"), (0, 0))

        #Texto
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_titulo.png"), (65,53))

        # Botones
        self.Button_controles.updatePos(100 * scale_factor, 90 * scale_factor, 72 * scale_factor, 8 * scale_factor)
        virtual_screen.blit(self.Button_controles.image, (self.Button_controles.getPos()[0] // scale_factor, self.Button_controles.getPos()[1] // scale_factor))

        self.Button_video.updatePos(115 * scale_factor, 125 * scale_factor, 72 * scale_factor, 8 * scale_factor)
        virtual_screen.blit(self.Button_video.image, (self.Button_video.getPos()[0] // scale_factor, self.Button_video.getPos()[1] // scale_factor))

        self.Button_audio.updatePos(115 * scale_factor, 160 * scale_factor, 72 * scale_factor, 8 * scale_factor)
        virtual_screen.blit(self.Button_audio.image, (
        self.Button_audio.getPos()[0] // scale_factor, self.Button_audio.getPos()[1] // scale_factor))

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.gameSateManager.set_state('menuWindow')


            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if self.Button_controles.isColliding():
                        self.gameSateManager.set_state('controlsOptions')
                    if self.Button_audio.isColliding():
                        self.gameSateManager.set_state('audioOptions')
                    if self.Button_video.isColliding():
                        self.gameSateManager.set_state('videoOptions')

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)

class level_type_Screen():
    def __init__(self, display, gameStateManager):
        self.options = ["Clásico", "Color", "Custom"]
        self.screen = display
        self.gameStateManager = gameStateManager


        # Botones
        self.Button_Clasico = Button_notScaled(30*scale_factor, 100*scale_factor,58*scale_factor,66*scale_factor,"Gráfica/Recursos/Sprites/Jugar/lvl_boton_clasico.png")
        self.Button_Color = Button_notScaled(60 * scale_factor, 100 * scale_factor, 52 * scale_factor,
                                               66 * scale_factor,
                                               "Gráfica/Recursos/Sprites/Jugar/lvl_ejemplo_boton_color.png")
        self.Button_Custom = Button_notScaled(90 * scale_factor, 100 * scale_factor, 52 * scale_factor,
                                               66 * scale_factor,
                                               "Gráfica/Recursos/Sprites/Jugar/lvl_boton_custom.png")


    def run(self, events):
        virtual_screen.fill((0, 0, 0))

        # Fondo
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Jugar/lvl_menu_detalle_fondo.png"),(0,0))

        # Texto
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Jugar/lvl_menu_categoria_titulo.png"),(55,55))

        # Botones
        self.Button_Clasico.updatePos(30*scale_factor, 100*scale_factor,58*scale_factor,66*scale_factor)
        virtual_screen.blit(self.Button_Clasico.image, (self.Button_Clasico.getPos()[0] // scale_factor, self.Button_Clasico.getPos()[1] // scale_factor))

        self.Button_Color.updatePos(103 * scale_factor, 100 * scale_factor, 52 * scale_factor, 66 * scale_factor)
        virtual_screen.blit(self.Button_Color.image, (self.Button_Color.getPos()[0] // scale_factor, self.Button_Color.getPos()[1] // scale_factor))

        self.Button_Custom.updatePos(175 * scale_factor, 100 * scale_factor, 58 * scale_factor, 66 * scale_factor)
        virtual_screen.blit(self.Button_Custom.image, (self.Button_Custom.getPos()[0] // scale_factor, self.Button_Custom.getPos()[1] // scale_factor))

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.gameStateManager.set_state('menuWindow')


            if event.type == MOUSEBUTTONUP:
                if self.Button_Clasico.isColliding():
                    self.gameStateManager.set_state('difficultyScreen')
                if self.Button_Color.isColliding():
                    self.gameStateManager.set_state('difficultyScreen')
                if self.Button_Custom.isColliding():
                    self.gameStateManager.set_state('difficultyScreen')

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)

class difficulty_Screen():
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager


        # Botones
        self.Button_Facil = Button_notScaled(46*scale_factor, 80*scale_factor,164*scale_factor,20*scale_factor,"Gráfica/Recursos/Sprites/Jugar/lvl_boton_dificultad_facil.png")
        self.Button_Medio = Button_notScaled(46 * scale_factor, 100 * scale_factor, 164 * scale_factor,
                                             20 * scale_factor,
                                             "Gráfica/Recursos/Sprites/Jugar/lvl_boton_dificultad_medio.png")
        self.Button_Dificil = Button_notScaled(46 * scale_factor, 100 * scale_factor, 164 * scale_factor,
                                             20 * scale_factor,
                                             "Gráfica/Recursos/Sprites/Jugar/lvl_boton_dificultad_dificil.png")


    def run(self, events):
        virtual_screen.fill((0, 0, 0))

        # Fondo
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Jugar/lvl_dificultad_detalle_fondo.png"),(0, 0))

        # Texto
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Jugar/lvl_dificultad_titulo.png"),(55,55))

        # Botones
        self.Button_Facil.updatePos(46 * scale_factor, 90 * scale_factor, 164 * scale_factor, 20 * scale_factor)
        virtual_screen.blit(self.Button_Facil.image, (self.Button_Facil.getPos()[0] // scale_factor, self.Button_Facil.getPos()[1] // scale_factor))

        self.Button_Medio.updatePos(46 * scale_factor, 130 * scale_factor, 164 * scale_factor, 20 * scale_factor)
        virtual_screen.blit(self.Button_Medio.image, (
        self.Button_Medio.getPos()[0] // scale_factor, self.Button_Medio.getPos()[1] // scale_factor))

        self.Button_Dificil.updatePos(46 * scale_factor, 170 * scale_factor, 164 * scale_factor, 20 * scale_factor)
        virtual_screen.blit(self.Button_Dificil.image, (
            self.Button_Dificil.getPos()[0] // scale_factor, self.Button_Dificil.getPos()[1] // scale_factor))

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.gameStateManager.set_state('levelTypeScreen')


            if event.type == MOUSEBUTTONUP:
                if self.Button_Facil.isColliding():
                    self.gameStateManager.set_state_id('levelSelectionScreen', 0)

                if self.Button_Medio.isColliding():
                    self.gameStateManager.set_state_id('levelSelectionScreen', 1)
                if self.Button_Dificil.isColliding():
                    self.gameStateManager.set_state_id('levelSelectionScreen', 2)

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)

class level_selection_Screen():

    id = 0
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager
        self.num_levels = 8
        self.rows, self.cols = 2, 4  # Grid arrangement

        self.level_size = 36

        self.horizontal_spacing = (ORIGINAL_WIDTH - (self.cols * self.level_size)) // (self.cols + 1)
        self.vertical_spacing = (ORIGINAL_HEIGHT - (self.rows * self.level_size) - 60) // (self.rows + 1)  # Account for title space (60px)


        # Botones
        self.Buttons = []
        for i in range(self.rows):
            for j in range(self.cols):
                pos_x = (self.horizontal_spacing + j * (self.level_size + self.horizontal_spacing))*scale_factor
                pos_y = (60 + self.vertical_spacing + i * (self.level_size + self.vertical_spacing))*scale_factor
                id = ((i*4)+j)+1
                boton = {
                    "id": id,  # Asignar un ID único, desde 1 a 8
                    "button": Button_notScaled(pos_x,pos_y,36*scale_factor, 36*scale_factor, f"Gráfica/Recursos/Sprites/Jugar/lvl_boton_nivel{id}.png")
                }
                self.Buttons.append(boton)
    def set_id(self,id):
        self.id = id
    def run(self, events):
        virtual_screen.fill((0, 0, 0))

        # Fondo
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Jugar/lvl_niveles_detalle_fondo.png"),(0, 0))

        #Text
        if self.id == 0:
            text_image = pygame.image.load("Gráfica/Recursos/Sprites/Jugar/lvl_subtitulo_dificultad_facil.png")
        elif self.id == 1:
            text_image = pygame.image.load("Gráfica/Recursos/Sprites/Jugar/lvl_subtitulo_dificultad_medio.png")
        elif self.id == 2:
            text_image = pygame.image.load("Gráfica/Recursos/Sprites/Jugar/lvl_subtitulo_dificultad_dificil.png")

        virtual_screen.blit(text_image, (5, 15))

        # Botones
        for row in range(self.rows):
            for col in range(self.cols):
                level_index = (row * 4) + col
                x = self.horizontal_spacing + col * (self.level_size + self.horizontal_spacing)
                y = 60 + self.vertical_spacing + row * (self.level_size + self.vertical_spacing)
                boton = self.Buttons[level_index]["button"]
                boton.updatePos(x * scale_factor, y * scale_factor, 36 * scale_factor,36 * scale_factor)
                virtual_screen.blit(boton.image, (x,y))

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.gameStateManager.set_state('difficultyScreen')


            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    for i in range(8):
                        if self.Buttons[i]["button"].isColliding():
                            if self.gameStateManager.id*100 + i + 1 >= 100:
                                self.gameStateManager.set_id_nonograma("n" + str(self.gameStateManager.id * 100 + i + 1))
                            else:
                                self.gameStateManager.set_id_nonograma("n00" + str(self.gameStateManager.id * 100 + i + 1))
                            self.gameStateManager.set_state('nonogramWindow')

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)
"""
def placeholder_level_screen():
    running = True
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text("Pantalla de nivel", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)
"""

class controls_Options():
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager
    def run(self, events):
        virtual_screen.fill((0, 0, 0))


        # Fondo
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_detalle_fondo_submenu.png"),(0, 0))

        # Texto
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_subtitulo_controles.png"), (15, 15))

        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_pantalla_controles_texto.png"),(30, 40))


        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.gameStateManager.set_state('optionsMenu')

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)

class audio_Options():
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager


        # Botones
        self.buttons = []
        for i in range(6):
            if i % 2 == 0:
                self.buttons.append(Button_notScaled(0, 0, 4 * scale_factor, 6 * scale_factor,"Gráfica/Recursos/Sprites/Opciones/op_boton_flecha_izq.png"))
            else:
                self.buttons.append(Button_notScaled(0, 0, 4 * scale_factor, 6 * scale_factor,"Gráfica/Recursos/Sprites/Opciones/op_boton_flecha_der.png"))
    def run(self, events):
        virtual_screen.fill((0, 0, 0))
        # Fondo
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_detalle_fondo_submenu.png"), (0, 0))

        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_subtitulo_audio.png"),(15, 15))
        # Global
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_opcion_audio_global.png"), (20, 40))
        self.buttons[0].updatePos(130 * scale_factor, 40 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[0].image, (self.buttons[0].getPos()[0] // scale_factor, self.buttons[0].getPos()[1] // scale_factor))
        self.buttons[1].updatePos(230 * scale_factor, 40 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[1].image,(self.buttons[1].getPos()[0] // scale_factor, self.buttons[1].getPos()[1] // scale_factor))

        #Musica
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_opcion_audio_musica.png"),(20, 70))
        self.buttons[2].updatePos(130 * scale_factor, 70 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[2].image, (self.buttons[2].getPos()[0] // scale_factor, self.buttons[2].getPos()[1] // scale_factor))
        self.buttons[3].updatePos(230 * scale_factor, 70 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[3].image,(self.buttons[3].getPos()[0] // scale_factor, self.buttons[3].getPos()[1] // scale_factor))

        #SFX
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Opciones/op_opcion_audio_SFX.png"),(20, 100))
        self.buttons[4].updatePos(130 * scale_factor, 100 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[4].image, (self.buttons[4].getPos()[0] // scale_factor, self.buttons[4].getPos()[1] // scale_factor))
        self.buttons[5].updatePos(230 * scale_factor, 100 * scale_factor, 4 * scale_factor, 6 * scale_factor)
        virtual_screen.blit(self.buttons[5].image,(self.buttons[5].getPos()[0] // scale_factor, self.buttons[5].getPos()[1] // scale_factor))


        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.gameStateManager.set_state('optionsMenu')
        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)

# Ventana para crear
class create_Screen():
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager

        # Botones
        self.draw_Button = Button_notScaled(40*scale_factor, 85*scale_factor, 84*scale_factor,98*scale_factor, "Gráfica/Recursos/Sprites/Crear/cr_boton_dibujar.png")
        self.import_Button = Button_notScaled(135 * scale_factor, 85 * scale_factor, 84 * scale_factor,98*scale_factor,"Gráfica/Recursos/Sprites/Crear/cr_boton_importar.png")

        self.Button_Confirmar = Button_notScaled(134*scale_factor,157*scale_factor, 84*scale_factor,20*scale_factor,"Gráfica/Recursos/Sprites/Crear/cr_boton_popup_confirmar.png")
        self.Button_Cancelar = Button_notScaled(38 * scale_factor, 157 * scale_factor, 84 * scale_factor,20 * scale_factor,"Gráfica/Recursos/Sprites/Crear/cr_boton_popup_cancelar.png")

        # Popup elegir tamaño
        self.choose_size = False
        self.buttons = []
        self.buttons.append(Button_notScaled(135*scale_factor,109*scale_factor,4*scale_factor,6*scale_factor, "Gráfica/Recursos/Sprites/Opciones/op_boton_flecha_izq.png"))
        self.buttons.append(Button_notScaled(170*scale_factor, 109*scale_factor, 4 * scale_factor, 6 * scale_factor, "Gráfica/Recursos/Sprites/Opciones/op_boton_flecha_der.png"))
        self.buttons.append(Button_notScaled(135 * scale_factor, 125 * scale_factor, 4 * scale_factor, 6 * scale_factor,"Gráfica/Recursos/Sprites/Opciones/op_boton_flecha_izq.png"))
        self.buttons.append(Button_notScaled(170 * scale_factor, 125 * scale_factor, 4 * scale_factor, 6 * scale_factor,"Gráfica/Recursos/Sprites/Opciones/op_boton_flecha_der.png"))

    def run(self, events):
        virtual_screen.fill((0, 0, 0))

        # Fondo
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Crear/cr_detalle_fondo.png"),(0,0))

        # Texto
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Crear/cr_titulo.png"), (85, 55))

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                if self.choose_size:
                    self.choose_size = False
                else:
                    self.choose_size = False
                    self.gameStateManager.set_state('menuWindow')

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Presionar boton de dibujar
                    if self.draw_Button.isColliding():
                        self.choose_size = True
                    if self.choose_size == True:
                        if self.Button_Cancelar.isColliding():
                            self.choose_size = False
                        if self.Button_Confirmar.isColliding():
                            self.gameStateManager.set_state('createNonogram')
        ######## DIBUJAR ########

        virtual_screen.blit(self.draw_Button.image, (self.draw_Button.getPos()[0]//scale_factor, self.draw_Button.getPos()[1]//scale_factor))
        virtual_screen.blit(self.import_Button.image, (self.import_Button.getPos()[0]//scale_factor, self.import_Button.getPos()[1]//scale_factor))


        if self.choose_size:
            # Dibujar rectangulo con alpha
            s = pygame.Surface((256*scale_factor, 240*scale_factor))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            virtual_screen.blit(s, (0, 0))

            # Dibujar popup
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Crear/cr_popup_opciones0.png"),(25, 80))

            # Botones
            virtual_screen.blit(self.buttons[0].image, (self.buttons[0].getPos()[0] // scale_factor, self.buttons[0].getPos()[1] // scale_factor))
            virtual_screen.blit(self.buttons[1].image, (self.buttons[1].getPos()[0] // scale_factor, self.buttons[1].getPos()[1] // scale_factor))
            virtual_screen.blit(self.buttons[2].image, (self.buttons[2].getPos()[0] // scale_factor, self.buttons[2].getPos()[1] // scale_factor))
            virtual_screen.blit(self.buttons[3].image, (self.buttons[3].getPos()[0] // scale_factor, self.buttons[3].getPos()[1] // scale_factor))

            virtual_screen.blit(self.Button_Confirmar.image, (self.Button_Confirmar.getPos()[0] // scale_factor, self.Button_Confirmar.getPos()[1] // scale_factor))
            virtual_screen.blit(self.Button_Cancelar.image, (self.Button_Cancelar.getPos()[0] // scale_factor, self.Button_Cancelar.getPos()[1] // scale_factor))

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))

        ######## DIBUJAR ########
        pygame.display.update()
        mainClock.tick(60)

class achievements_Screen():
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager

        # Achievements
        self.achievement_tracker = NonogramAchievementTracker()

        # Botones
        self.Button_vel1 = Button_notScaled(20*scale_factor, 50*scale_factor, 32*scale_factor,32*scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_vel1.png")
        self.Button_vel2 = Button_notScaled(20 * scale_factor, 110 * scale_factor, 32 * scale_factor, 32 * scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_vel2.png")
        self.Button_vel3 = Button_notScaled(20 * scale_factor, 80 * scale_factor, 32 * scale_factor, 32 * scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_vel3.png")

        self.Button_dif1 = Button_notScaled(20 * scale_factor, 30 * scale_factor, 32 * scale_factor, 32 * scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_dif1.png")
        self.Button_dif2 = Button_notScaled(20 * scale_factor, 50 * scale_factor, 32 * scale_factor, 32 * scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_dif2.png")
        self.Button_dif3 = Button_notScaled(20 * scale_factor, 80 * scale_factor, 32 * scale_factor, 32 * scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_dif3.png")

        self.Button_click1 = Button_notScaled(20 * scale_factor, 30 * scale_factor, 32 * scale_factor, 32 * scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_click1.png")
        self.Button_click2 = Button_notScaled(20 * scale_factor, 50 * scale_factor, 32 * scale_factor, 32 * scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_click2.png")
        self.Button_click3 = Button_notScaled(20 * scale_factor, 80 * scale_factor, 32 * scale_factor, 32 * scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_click3.png")

        self.Button_creapuzzle = Button_notScaled(20 * scale_factor, 30 * scale_factor, 32 * scale_factor,32 * scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_creapuzle.png")
        self.Button_cambiacolor = Button_notScaled(20 * scale_factor, 50 * scale_factor, 32 * scale_factor,32 * scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_cambiacolor.png")
        self.Button_logros100 = Button_notScaled(20 * scale_factor, 80 * scale_factor, 32 * scale_factor,32 * scale_factor,"Gráfica/Recursos/Sprites/Logros/lgr_icono_logros100.png")
    def run(self, events):
        virtual_screen.fill((0, 0, 0))
        # Fondo
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/logros/lgr_detalle_fondo.png"),(0,0))

        # Texto
        virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_titulo.png"),(80, 15))

        ###### LOGROS ######
        # Velocidad
        self.Button_vel1.updatePos(20 * scale_factor, 50 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_vel1.image, (self.Button_vel1.getPos()[0] // scale_factor, self.Button_vel1.getPos()[1] // scale_factor))
        # Para este checkbox necesitamos una condición if, que vendrá por la parte lógica de Logros
        if "Speedster I" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox1.png"),(44,74))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"), (44, 74))

        self.Button_vel2.updatePos(20 * scale_factor, 110 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_vel2.image, (self.Button_vel2.getPos()[0] // scale_factor, self.Button_vel2.getPos()[1] // scale_factor))
        if "Speedster II" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox1.png"),(44, 134))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"), (44, 134))

        self.Button_vel3.updatePos(20 * scale_factor, 170 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_vel3.image, (self.Button_vel3.getPos()[0] // scale_factor, self.Button_vel3.getPos()[1] // scale_factor))

        if "Speedster III" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox1.png"), (44, 194))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"), (44, 194))

        # Dificultad
        self.Button_dif1.updatePos(80 * scale_factor, 50 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_dif1.image, (
        self.Button_dif1.getPos()[0] // scale_factor, self.Button_dif1.getPos()[1] // scale_factor))
        if "AccessGranted" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox1.png"),(104, 74))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"),(104, 74))


        self.Button_dif2.updatePos(80 * scale_factor, 110 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_dif2.image, (
        self.Button_dif2.getPos()[0] // scale_factor, self.Button_dif2.getPos()[1] // scale_factor))
        if "Breacher" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox1.png"),(104, 134))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"),(104, 134))


        self.Button_dif3.updatePos(80 * scale_factor, 170 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_dif3.image, (
        self.Button_dif3.getPos()[0] // scale_factor, self.Button_dif3.getPos()[1] // scale_factor))
        if "Netrunner" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox1.png"),(104, 194))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"),(104, 194))


        # Clicks
        self.Button_click1.updatePos(140 * scale_factor, 50 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_click1.image, (self.Button_click1.getPos()[0] // scale_factor, self.Button_click1.getPos()[1] // scale_factor))
        if "Minimalist I" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbo1.png"),(164, 74))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"),(164, 74))

        self.Button_click2.updatePos(140 * scale_factor, 110 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_click2.image, (self.Button_click2.getPos()[0] // scale_factor, self.Button_click2.getPos()[1] // scale_factor))
        if "Minimalist II" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox1.png"),(164, 134))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"),(164, 134))

        self.Button_click3.updatePos(140 * scale_factor, 170 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_click3.image, (self.Button_click3.getPos()[0] // scale_factor, self.Button_click3.getPos()[1] // scale_factor))
        if "Minimalist III" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox1.png"),(164, 194))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"),(164, 194))

        # Miscelanea
        self.Button_creapuzzle.updatePos(200 * scale_factor, 50 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_creapuzzle.image, (self.Button_creapuzzle.getPos()[0] // scale_factor, self.Button_creapuzzle.getPos()[1] // scale_factor))
        if "Picasso" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox1.png"),(224, 74))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"),(224, 74))

        self.Button_cambiacolor.updatePos(200 * scale_factor, 110 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_cambiacolor.image, (self.Button_cambiacolor.getPos()[0] // scale_factor, self.Button_cambiacolor.getPos()[1] // scale_factor))
        if "HUE Shift" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox1.png"),(224, 134))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"),(224, 134))

        self.Button_logros100.updatePos(200 * scale_factor, 170 * scale_factor, 32 * scale_factor, 32 * scale_factor)
        virtual_screen.blit(self.Button_logros100.image, (self.Button_logros100.getPos()[0] // scale_factor, self.Button_logros100.getPos()[1] // scale_factor))

        if "Completionist" in self.achievement_tracker.show_achievements():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox1.png"),(224, 194))
        else:
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_checkbox0.png"),(224, 194))

        ###### LOGROS ######

        # Mostrar logros
        if self.Button_vel1.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_tiempo1_desc.png"),(70,40))
        elif self.Button_vel2.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_tiempo2_desc.png"),(70,100))
        elif self.Button_vel3.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_tiempo3_desc.png"),(70,160))

        if self.Button_dif1.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_dificultad1_desc.png"),(130,40))
        elif self.Button_dif2.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_dificultad2_desc.png"),(130,100))
        elif self.Button_dif3.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_dificultad3_desc.png"),(130,160))

        if self.Button_click1.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_click1_desc.png"),(10,40))
        elif self.Button_click2.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_click2_desc.png"),(10,100))
        elif self.Button_click3.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_click3_desc.png"),(10,160))

        if self.Button_creapuzzle.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_dibujapuzle_desc.png"),(70,40))
        elif self.Button_cambiacolor.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_cambiacolor_desc.png"),(70,100))
        elif self.Button_logros100.isColliding():
            virtual_screen.blit(pygame.image.load("Gráfica/Recursos/Sprites/Logros/lgr_icono_logros100_desc.png"),(70,160))


        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.gameStateManager.set_state('menuWindow')

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)

"""
def sub_screen(title):
    running = True
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text(title, font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 4)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)
"""


class menuWindow():
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager


        # Botones
        self.Button_Jugar = Button_notScaled(109*scale_factor, 101*scale_factor, 40*scale_factor,8*scale_factor,"Gráfica/Recursos/Sprites/Menu_principal/mp_boton_jugar.png")
        self.Button_Opciones = Button_notScaled(109*scale_factor, 118*scale_factor, 64*scale_factor, 8*scale_factor,
                                             "Gráfica/Recursos/Sprites/Menu_principal/mp_boton_opciones.png")
        self.Button_Crear = Button_notScaled(109*scale_factor, 135*scale_factor, 40*scale_factor, 8*scale_factor,
                                             "Gráfica/Recursos/Sprites/Menu_principal/mp_boton_crear.png")
        self.Button_Logros = Button_notScaled(109*scale_factor, 152*scale_factor, 47*scale_factor, 8*scale_factor,
                                             "Gráfica/Recursos/Sprites/Menu_principal/mp_boton_logros.png")

        self.click = False
        self.confirm_exit = False

    def run(self, events):
        # Gradiente en fondo
        for y in range(ORIGINAL_HEIGHT):
            color = (0 + y // 4, 0 + y // 12, 0 + y // 3)
            pygame.draw.line(virtual_screen, color, (0, y), (ORIGINAL_WIDTH, y))

        # Fondo
        bg_image = pygame.image.load("Gráfica/Recursos/Sprites/Menu_principal/mp_fondo.png")
        virtual_screen.blit(bg_image,(0,0))

        # Dibuja texto
        bg_text = pygame.image.load("Gráfica/Recursos/Sprites/Menu_principal/mp_Titulo.png")
        virtual_screen.blit(bg_text, (15,15))
        bg_text_detalle = pygame.image.load("Gráfica/Recursos/Sprites/Menu_principal/mp_detalles.png")
        virtual_screen.blit(bg_text_detalle, (35, 208))


        # Display de botones y funcionalidad
        self.Button_Jugar.updatePos(109*scale_factor, 101*scale_factor, 40*scale_factor,8*scale_factor)
        self.Button_Opciones.updatePos(109*scale_factor, 118*scale_factor, 64*scale_factor, 8*scale_factor)
        self.Button_Crear.updatePos(109*scale_factor, 135*scale_factor, 40*scale_factor, 8*scale_factor)
        self.Button_Logros.updatePos(109*scale_factor, 152*scale_factor, 47*scale_factor, 8*scale_factor)
        virtual_screen.blit(self.Button_Jugar.image,(self.Button_Jugar.getPos()[0]//scale_factor,self.Button_Jugar.getPos()[1]//scale_factor))
        virtual_screen.blit(self.Button_Opciones.image, (self.Button_Opciones.getPos()[0]//scale_factor,self.Button_Opciones.getPos()[1]//scale_factor))
        virtual_screen.blit(self.Button_Logros.image, (self.Button_Logros.getPos()[0]//scale_factor,self.Button_Logros.getPos()[1]//scale_factor))
        virtual_screen.blit(self.Button_Crear.image, (self.Button_Crear.getPos()[0]//scale_factor,self.Button_Crear.getPos()[1]//scale_factor))



        mx, my = pygame.mouse.get_pos()
        mx = int(mx / scale_factor)
        my = int(my / scale_factor)

        if not self.confirm_exit:
            self.click = False

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.confirm_exit = True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if self.Button_Jugar.isColliding():
                        self.gameStateManager.set_state('levelTypeScreen')
                    if self.Button_Opciones.isColliding():
                        self.gameStateManager.set_state('optionsMenu')
                    if self.Button_Crear.isColliding():
                        self.gameStateManager.set_state('createScreen')
                    if self.Button_Logros.isColliding():
                        self.gameStateManager.set_state('achievementsScreen')


        if self.confirm_exit:
            pygame.draw.rect(virtual_screen, (0, 0, 0), (50, 80, 156, 80))
            pygame.draw.rect(virtual_screen, (255, 255, 255), (50, 80, 156, 80), 2)
            draw_text("Seguro que ", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 100)
            draw_text("quieres salir?", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 120)

            yes_rect = draw_button(virtual_screen, "Si", 90, 150, 40, 20)
            no_rect = draw_button(virtual_screen, "No", 165, 150, 40, 20)

            draw_text("Si", font, (255, 255, 255), virtual_screen, 90, 150)
            draw_text("No", font, (255, 255, 255), virtual_screen, 165, 150)

            if self.click:
                if yes_rect.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()
                elif no_rect.collidepoint(mx, my):
                    self.confirm_exit = False
                self.click = False

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)