import pygame, sys

from Gráfica.Ventana_Nonograma import WINDOW_SCALE
from Gráfica.Button import Button, Button_notSquare, Button_notScaled

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
title_font = pygame.font.Font('Gráfica/Audiovisual_juego/Fonts/16x-Vermin Vibes 1989.ttf', 36)
font = pygame.font.SysFont('OCR-A Extended', 12, bold=True)

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
    def run(self, events):
        global current_display_mode, brightness, selected_option, selected_color, scale_factor
        virtual_screen.fill((0, 0, 0))
        draw_text("Video", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 30)

        # controles de resolucion
        draw_text("Resolucion:", font, (255, 255, 255), virtual_screen, 50, 70)
        current_res = f"{resolutions[current_resolution_index][0]}x{resolutions[current_resolution_index][1]}"
        draw_text(current_res, font, (255, 255, 255), virtual_screen, 175, 70)
        left_arrow_res = draw_arrow(virtual_screen, 120, 65, 'left')
        right_arrow_res = draw_arrow(virtual_screen, 230, 65, 'right')

        # controles de display mode
        draw_text("Pantalla:", font, (255, 255, 255), virtual_screen, 43, 100)
        draw_text(display_modes[current_display_mode], font, (255, 255, 255), virtual_screen, 175, 100)
        left_arrow_display = draw_arrow(virtual_screen, 120, 95, 'left')
        right_arrow_display = draw_arrow(virtual_screen, 230, 95, 'right')

        # control de brillo
        draw_text("Brillo:", font, (255, 255, 255), virtual_screen, 35, 130)
        pygame.draw.rect(virtual_screen, (100, 100, 100), (140, 125, 80, 10))
        pygame.draw.rect(virtual_screen, (255, 255, 255), (140, 125, brightness * 0.8, 10))
        left_arrow_brightness = draw_arrow(virtual_screen, 120, 125, 'left')
        right_arrow_brightness = draw_arrow(virtual_screen, 230, 125, 'right')

        # Elejir color de UI
        draw_text("Color UI:", font, (255, 255, 255), virtual_screen, 63, 160)
        color_positions = [(100, 155), (140, 155), (180, 155)]

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
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if left_arrow_res.collidepoint(scaled_mx, scaled_my):
                        change_resolution(current_resolution_index - 1)
                    elif right_arrow_res.collidepoint(scaled_mx, scaled_my):
                        change_resolution(current_resolution_index + 1)
                    elif left_arrow_display.collidepoint(scaled_mx, scaled_my):
                        current_display_mode = (current_display_mode - 1) % len(display_modes)
                    elif right_arrow_display.collidepoint(scaled_mx, scaled_my):
                        current_display_mode = (current_display_mode + 1) % len(display_modes)
                    elif left_arrow_brightness.collidepoint(scaled_mx, scaled_my):
                        brightness = max(0, brightness - 5)
                    elif right_arrow_brightness.collidepoint(scaled_mx, scaled_my):
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
    def run(self, events):
        global scale_factor
        virtual_screen.fill((0, 0, 0))
        draw_text("Opciones", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 30)

        button_texts = ["Controles", "Video", "Audio"]
        button_rects = []
        for i, text in enumerate(button_texts):
            button_rect = draw_button(virtual_screen, text, ORIGINAL_WIDTH // 2, 80 + i * 40)
            button_rects.append(button_rect)
            draw_text(text, font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 80 + i * 40)

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
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(scaled_mx, scaled_my):
                            if i == 0:
                                self.gameSateManager.set_state('controlsOptions')
                            elif i == 1:
                                self.gameSateManager.set_state('videoOptions')
                            elif i == 2:
                                self.gameSateManager.set_state('audioOptions')

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)

class level_type_Screen():
    def __init__(self, display, gameStateManager):
        self.options = ["Clásico", "Color", "Custom"]
        self.screen = display
        self.gameStateManager = gameStateManager
    def run(self, events):
        virtual_screen.fill((0, 0, 0))
        draw_text("Selecciona el tipo de nivel", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 30)

        button_rects = []
        for i, option in enumerate(self.options):
            button_rect = draw_button(virtual_screen, option, ORIGINAL_WIDTH // 2, 80 + i * 40)
            button_rects.append(button_rect)
            draw_text(option, font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 80 + i * 40)

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.gameStateManager.set_state('menuWindow')
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(scaled_mx, scaled_my):
                        self.gameStateManager.set_state('difficultyScreen')

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)

class difficulty_Screen():
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager
        self.difficulties = ["Fácil", "Medio", "Difícil"]
    def run(self, events):
        virtual_screen.fill((0, 0, 0))
        draw_text("Selecciona la dificultad", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 30)

        button_rects = []
        for i, difficulty in enumerate(self.difficulties):
            button_rect = draw_button(virtual_screen, difficulty, ORIGINAL_WIDTH // 2, 80 + i * 40)
            button_rects.append(button_rect)
            draw_text(difficulty, font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 80 + i * 40)

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.gameStateManager.set_state('levelTypeScreen')
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(scaled_mx, scaled_my):
                        self.gameStateManager.set_state('levelSelectionScreen')

        scaled_surface = pixel_perfect_scale(virtual_screen, scale_factor)
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)

class level_selection_Screen():
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager
        self.num_levels = 8
        self.rows, self.cols = 2, 4  # Grid arrangement
        self.level_size = 40

        self.horizontal_spacing = (ORIGINAL_WIDTH - (self.cols * self.level_size)) // (self.cols + 1)
        self.vertical_spacing = (ORIGINAL_HEIGHT - (self.rows * self.level_size) - 60) // (self.rows + 1)  # Account for title space (60px)
    def run(self, events):
        virtual_screen.fill((0, 0, 0))
        draw_text("Selecciona el nivel", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 30)

        level_rects = []
        for row in range(self.rows):
            for col in range(self.cols):
                level_index = row * self.cols + col
                x = self.horizontal_spacing + col * (self.level_size + self.horizontal_spacing)
                y = 60 + self.vertical_spacing + row * (self.level_size + self.vertical_spacing)
                level_rect = pygame.Rect(x, y, self.level_size, self.level_size)
                level_rects.append(level_rect)
                pygame.draw.rect(virtual_screen, (255, 255, 255), level_rect)
                draw_text(str(level_index + 1), font, (0, 0, 0), virtual_screen, x + self.level_size // 2,
                          y + self.level_size // 2)

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.gameStateManager.set_state('difficultyScreen')
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(level_rects):
                    if rect.collidepoint(scaled_mx, scaled_my):
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
        draw_text("Controles", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 4)

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
    def run(self, events):
        virtual_screen.fill((0, 0, 0))
        draw_text("Audio", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 4)

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
        self.draw_Button = Button_notScaled(40*scale_factor, 85*scale_factor, 84*scale_factor,98*scale_factor, "Gráfica/Audiovisual_juego/Sprites/Crear/cr_boton_dibujar.png")
        self.import_Button = Button_notScaled(135 * scale_factor, 85 * scale_factor, 84 * scale_factor,98*scale_factor,"Gráfica/Audiovisual_juego/Sprites/Crear/cr_boton_importar.png")

        self.Button_Confirmar = Button_notScaled(134*scale_factor,157*scale_factor, 84*scale_factor,20*scale_factor,"Gráfica/Audiovisual_juego/Sprites/Crear/cr_boton_popup_confirmar.png")
        self.Button_Cancelar = Button_notScaled(38 * scale_factor, 157 * scale_factor, 84 * scale_factor,20 * scale_factor,"Gráfica/Audiovisual_juego/Sprites/Crear/cr_boton_popup_cancelar.png")

        # Popup elegir tamaño
        self.choose_size = False
        self.buttons = []
        self.buttons.append(Button_notScaled(135*scale_factor,109*scale_factor,4*scale_factor,6*scale_factor, "Gráfica/Audiovisual_juego/Sprites/Opciones/op_boton_flecha_izq.png"))
        self.buttons.append(Button_notScaled(170*scale_factor, 109*scale_factor, 4 * scale_factor, 6 * scale_factor, "Gráfica/Audiovisual_juego/Sprites/Opciones/op_boton_flecha_der.png"))
        self.buttons.append(Button_notScaled(135 * scale_factor, 125 * scale_factor, 4 * scale_factor, 6 * scale_factor,"Gráfica/Audiovisual_juego/Sprites/Opciones/op_boton_flecha_izq.png"))
        self.buttons.append(Button_notScaled(170 * scale_factor, 125 * scale_factor, 4 * scale_factor, 6 * scale_factor,"Gráfica/Audiovisual_juego/Sprites/Opciones/op_boton_flecha_der.png"))

    def run(self, events):
        virtual_screen.fill((0, 0, 0))

        # Fondo
        virtual_screen.blit(pygame.image.load("Gráfica/Audiovisual_juego/Sprites/Crear/cr_detalle_fondo.png"),(0,0))

        # Texto
        virtual_screen.blit(pygame.image.load("Gráfica/Audiovisual_juego/Sprites/Crear/cr_titulo.png"), (85, 55))

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
            virtual_screen.blit(pygame.image.load("Gráfica/Audiovisual_juego/Sprites/Crear/cr_popup_opciones0.png"),(25, 80))

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
    def run(self, events):
        virtual_screen.fill((0, 0, 0))
        draw_text("Logros", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 4)

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
        self.click = False
        self.confirm_exit = False

    def run(self, events):
        # Gradiente en fondo
        for y in range(ORIGINAL_HEIGHT):
            color = (0 + y // 4, 0 + y // 12, 0 + y // 3)
            pygame.draw.line(virtual_screen, color, (0, y), (ORIGINAL_WIDTH, y))

        # Dibuja texto
        draw_text('Gridlock', title_font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 4)

        # Display de botones y funcionalidad
        button_texts = ["Jugar", "Opciones", "Crear", "Logros"]
        button_rects = []
        for i, text in enumerate(button_texts):
            button_rect = draw_button(virtual_screen, text, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 2 - 20 + i * 20)
            button_rects.append(button_rect)
            draw_text(text, font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2,
                      ORIGINAL_HEIGHT // 2 - 20 + i * 20)

        mx, my = pygame.mouse.get_pos()
        mx = int(mx / scale_factor)
        my = int(my / scale_factor)

        if not self.confirm_exit:
            if self.click:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mx, my):
                        if i == 0:
                            self.gameStateManager.set_state('levelTypeScreen')
                        elif i == 1:
                            # Cambiar estado a 'optionsMenu', ver en objeto stateManager en main
                            self.gameStateManager.set_state('optionsMenu')
                        elif i == 2:
                            self.gameStateManager.set_state('createScreen')
                        elif i == 3:
                            self.gameStateManager.set_state('achievementsScreen')
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