import pygame, sys

# Setup pygame/ventana
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Testeo Menus')

# Res original
ORIGINAL_WIDTH, ORIGINAL_HEIGHT = 256, 240
scale_factor = 3  # factor de escalamiento, ajustable
screen = pygame.display.set_mode((ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor), RESIZABLE)

# ventana virtual
virtual_screen = pygame.Surface((ORIGINAL_WIDTH, ORIGINAL_HEIGHT))

# Renderizacion de texto
title_font = pygame.font.Font('Vermin Vibes.ttf', 36)
font = pygame.font.SysFont('OCR-A Extended', 12, bold=True)

# Video settings
# Updated resolutions list with more options
resolutions = [
    (256, 240),   # Min resolution
    (512, 480),
    (768, 720),
    (1024, 960),
    (1280, 1200),
    (1536, 1440)  # Max resolution
]
current_resolution_index = 0
display_modes = ["Windowed", "Fullscreen", "Windowed Fullscreen"]
current_display_mode = 0
brightness = 50  # Default brightness
selected_option = None
selected_color = None

# UI Colors
ui_colors = [
    {"color": (255, 0, 0), "pos": (80, 140), "selected": False},
    {"color": (0, 255, 0), "pos": (120, 140), "selected": False},
    {"color": (0, 0, 255), "pos": (160, 140), "selected": False}
]

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
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

click = False
confirm_exit = False


def main_menu():
    global click, scale_factor, screen, confirm_exit
    while True:
        # Gradiente en fondo
        for y in range(ORIGINAL_HEIGHT):
            color = (0 + y // 4, 0 + y // 12, 0 + y // 3)
            pygame.draw.line(virtual_screen, color, (0, y), (ORIGINAL_WIDTH, y))

        # Dibuja texto
        draw_text('PLACEHOLDER', title_font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 4)

        # Display de botones y funcionalidad
        button_texts = ["Play", "Options", "Create", "Achievements"]
        button_rects = []
        for i, text in enumerate(button_texts):
            button_rect = draw_button(virtual_screen, text, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 2 - 20 + i * 20)
            button_rects.append(button_rect)
            draw_text(text, font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2,
                      ORIGINAL_HEIGHT // 2 - 20 + i * 20)

        mx, my = pygame.mouse.get_pos()
        mx = int(mx / scale_factor)
        my = int(my / scale_factor)

        if not confirm_exit:
            if click:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mx, my):
                        if i == 0:
                            play()
                        elif i == 1:
                            options_menu()  # Changed to options_menu
                        elif i == 2:
                            create()
                        elif i == 3:
                            achievements()
            click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    confirm_exit = True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if confirm_exit:
            pygame.draw.rect(virtual_screen, (0, 0, 0), (50, 80, 156, 80))
            pygame.draw.rect(virtual_screen, (255, 255, 255), (50, 80, 156, 80), 2)
            draw_text("Are you sure you", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 100)
            draw_text("want to exit?", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 120)

            yes_rect = draw_button(virtual_screen, "Yes", 90, 150, 40, 20)
            no_rect = draw_button(virtual_screen, "No", 165, 150, 40, 20)

            draw_text("Yes", font, (255, 255, 255), virtual_screen, 90, 150)
            draw_text("No", font, (255, 255, 255), virtual_screen, 165, 150)

            if click:
                if yes_rect.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()
                elif no_rect.collidepoint(mx, my):
                    confirm_exit = False
                click = False

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.update()
        mainClock.tick(60)


def video_options():
    global click, current_resolution_index, current_display_mode, brightness, selected_option, selected_color, screen, scale_factor
    running = True
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text("Video", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 30)

        # Resolution controls - Moved to the right
        draw_text("Resolucion:", font, (255, 255, 255), virtual_screen, 70, 70)
        current_res = f"{resolutions[current_resolution_index][0]}x{resolutions[current_resolution_index][1]}"
        draw_text(current_res, font, (255, 255, 255), virtual_screen, 170, 70)  # Moved right
        left_arrow_res = draw_arrow(virtual_screen, 140, 65, 'left')  # Adjusted position
        right_arrow_res = draw_arrow(virtual_screen, 200, 65, 'right')  # Adjusted position

        # Display mode controls - Moved to the right
        draw_text("Pantalla:", font, (255, 255, 255), virtual_screen, 63, 100)
        draw_text(display_modes[current_display_mode], font, (255, 255, 255), virtual_screen, 170, 100)  # Moved right
        left_arrow_display = draw_arrow(virtual_screen, 140, 95, 'left')  # Adjusted position
        right_arrow_display = draw_arrow(virtual_screen, 200, 95, 'right')  # Adjusted position

        # Brightness control - Moved to the right
        draw_text("Brillo:", font, (255, 255, 255), virtual_screen, 55, 130)
        # Moved brightness bar and arrows to the right
        pygame.draw.rect(virtual_screen, (100, 100, 100), (140, 125, 80, 10))  # Background bar
        pygame.draw.rect(virtual_screen, (255, 255, 255), (140, 125, brightness * 0.8, 10))  # Progress bar
        left_arrow_brightness = draw_arrow(virtual_screen, 120, 125, 'left')
        right_arrow_brightness = draw_arrow(virtual_screen, 230, 125, 'right')

        # Color UI selection
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

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if left_arrow_res.collidepoint(scaled_mx, scaled_my):
                        if current_resolution_index > 0:
                            current_resolution_index -= 1
                            new_width = resolutions[current_resolution_index][0]
                            new_height = resolutions[current_resolution_index][1]
                            scale_factor = new_width // ORIGINAL_WIDTH
                            screen = pygame.display.set_mode((new_width, new_height), RESIZABLE)
                    elif right_arrow_res.collidepoint(scaled_mx, scaled_my):
                        if current_resolution_index < len(resolutions) - 1:
                            current_resolution_index += 1
                            new_width = resolutions[current_resolution_index][0]
                            new_height = resolutions[current_resolution_index][1]
                            scale_factor = new_width // ORIGINAL_WIDTH
                            screen = pygame.display.set_mode((new_width, new_height), RESIZABLE)
                    elif left_arrow_display.collidepoint(scaled_mx, scaled_my):
                        current_display_mode = (current_display_mode - 1) % len(display_modes)
                    elif right_arrow_display.collidepoint(scaled_mx, scaled_my):
                        current_display_mode = (current_display_mode + 1) % len(display_modes)
                    elif left_arrow_brightness.collidepoint(scaled_mx, scaled_my):
                        brightness = max(0, brightness - 5)
                    elif right_arrow_brightness.collidepoint(scaled_mx, scaled_my):
                        brightness = min(100, brightness + 5)

                    # Color selection
                    for color_option in ui_colors:
                        color_rect = pygame.Rect(color_option["pos"][0], color_option["pos"][1], 20, 20)
                        if color_rect.collidepoint(scaled_mx, scaled_my):
                            for c in ui_colors:
                                c["selected"] = False
                            color_option["selected"] = True
                            selected_color = color_option["color"]

        scaled_surface = pygame.transform.scale(virtual_screen,
                                             (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)


def options_menu():
    global click, scale_factor, screen
    running = True
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text("Options", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 30)

        button_texts = ["Controles", "Video", "Audio"]
        button_rects = []
        for i, text in enumerate(button_texts):
            button_rect = draw_button(virtual_screen, text, ORIGINAL_WIDTH // 2, 80 + i * 40)
            button_rects.append(button_rect)
            draw_text(text, font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 80 + i * 40)

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(scaled_mx, scaled_my):
                            if i == 0:
                                controls()
                            elif i == 1:
                                video_options()
                            elif i == 2:
                                audio()

        scaled_surface = pygame.transform.scale(virtual_screen,
                                             (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)


def controls():
    sub_screen("Controles")


def audio():
    sub_screen("Audio")


def play():
    sub_screen("Juego")


def create():
    sub_screen("Crear")


def achievements():
    sub_screen("Logros")


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

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.update()
        mainClock.tick(60)


main_menu()