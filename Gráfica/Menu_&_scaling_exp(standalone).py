import pygame, sys
import math

# Setup pygame/ventana
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Game Menu System')

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
title_font = pygame.font.Font('Vermin Vibes.ttf', 36)
font = pygame.font.SysFont('OCR-A Extended', 12, bold=True)

# opciones en video
display_modes = ["Windowed", "Fullscreen", "Windowed\nFullscreen"]
current_display_mode = 0
brightness = 50
crt_filter = True  # Filtr CRT
selected_option = None
selected_color = None

# UI Colors
ui_colors = [
    {"color": (255, 0, 0), "pos": (80, 140), "selected": False},
    {"color": (0, 255, 0), "pos": (120, 140), "selected": False},
    {"color": (0, 0, 255), "pos": (160, 140), "selected": False}
]

# Estados de transiciones
TRANSITION_DURATION = 30
transition_frame = 0
is_transitioning = False
transition_type = None  # 'fade' or 'push'
transition_direction = None  # 'in' or 'out'
next_screen = None
current_screen = None


def apply_crt_filter(surface):
    if not crt_filter:
        return surface

    width, height = surface.get_size()
    filtered = surface.copy()

    # Efecto scanlines
    for y in range(0, height, 2):
        dark_line = pygame.Surface((width, 1))
        dark_line.fill((0, 0, 0))
        dark_line.set_alpha(50)
        filtered.blit(dark_line, (0, y))

    # Efecto vignette
    vignette = pygame.Surface((width, height))
    center_x, center_y = width // 2, height // 2
    max_dist = math.sqrt(center_x ** 2 + center_y ** 2)

    for x in range(width):
        for y in range(height):
            dist = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            intensity = int(255 * (1 - dist / max_dist))
            vignette.set_at((x, y), (intensity, intensity, intensity))

    filtered.blit(vignette, (0, 0), special_flags=pygame.BLEND_MULT)
    return filtered

#funcionalidad de transicion de pantallas
def handle_transition():
    global transition_frame, is_transitioning, current_screen

    if is_transitioning:
        if transition_type == 'fade':
            alpha = min(255, int((transition_frame / TRANSITION_DURATION) * 255))
            if transition_direction == 'out':
                alpha = 255 - alpha

            fade_surface = pygame.Surface((ORIGINAL_WIDTH, ORIGINAL_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(alpha)
            virtual_screen.blit(fade_surface, (0, 0))

        elif transition_type == 'push':
            offset = int((transition_frame / TRANSITION_DURATION) * ORIGINAL_WIDTH)
            if transition_direction == 'out':
                offset = ORIGINAL_WIDTH - offset

            temp_surface = virtual_screen.copy()
            virtual_screen.fill((0, 0, 0))
            virtual_screen.blit(temp_surface, (offset if transition_direction == 'in' else -offset, 0))

            # añade filtro
            if transition_frame % 2:
                virtual_screen.scroll(0, 1)
            else:
                virtual_screen.scroll(0, -1)

        transition_frame += 1
        if transition_frame >= TRANSITION_DURATION:
            is_transitioning = False
            transition_frame = 0
            if next_screen:
                current_screen = next_screen


def start_transition(trans_type, direction, next_screen_func=None):
    global is_transitioning, transition_type, transition_direction, next_screen, transition_frame
    is_transitioning = True
    transition_type = trans_type
    transition_direction = direction
    transition_frame = 0
    next_screen = next_screen_func


def draw_text(text, font, color, surface, x, y):
    if '\n' in text:
        lines = text.split('\n')
        line_height = font.get_height()
        for i, line in enumerate(lines):
            textobj = font.render(line, True, color)
            textrect = textobj.get_rect(center=(x, y + i * line_height))
            surface.blit(textobj, textrect)
    else:
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


def video_options():
    global click, current_resolution_index, current_display_mode, brightness, selected_option, selected_color, screen, scale_factor, crt_filter, virtual_screen
    running = True
    current_resolution_index = get_current_resolution()

    while running:
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

        # toggle del filtro CRT
        draw_text("CRT Filter:", font, (255, 255, 255), virtual_screen, 45, 160)
        crt_status = "On" if crt_filter else "Off"
        draw_text(crt_status, font, (255, 255, 255), virtual_screen, 175, 160)
        left_arrow_crt = draw_arrow(virtual_screen, 120, 155, 'left')
        right_arrow_crt = draw_arrow(virtual_screen, 230, 155, 'right')

        # Elejir color de UI
        draw_text("Color UI:", font, (255, 255, 255), virtual_screen, 63, 190)
        color_positions = [(100, 185), (140, 185), (180, 185)]

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
                    elif left_arrow_crt.collidepoint(scaled_mx, scaled_my) or right_arrow_crt.collidepoint(scaled_mx,
                                                                                                           scaled_my):
                        crt_filter = not crt_filter

                    # seleccion de colores
                    for color_option in ui_colors:
                        color_rect = pygame.Rect(color_option["pos"][0], color_option["pos"][1], 20, 20)
                        if color_rect.collidepoint(scaled_mx, scaled_my):
                            for c in ui_colors:
                                c["selected"] = False
                            color_option["selected"] = True
                            selected_color = color_option["color"]

        if crt_filter:
            virtual_screen = apply_crt_filter(virtual_screen)

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.update()
        mainClock.tick(60)


def level_screen():
    global virtual_screen
    running = True
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text("Pantalla nivel", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        if crt_filter:
            virtual_screen = apply_crt_filter(virtual_screen)

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        handle_transition()
        pygame.display.update()
        mainClock.tick(60)


def levels_layout(difficulty):
    global virtual_screen
    running = True
    grid_cols = 4
    grid_rows = 3
    padding = 20
    icon_size = 40
    spacing_x = (ORIGINAL_WIDTH - 2 * padding) // (grid_cols - 1)
    spacing_y = (ORIGINAL_HEIGHT - 2 * padding - 40) // (grid_rows - 1)

    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text(f"Niveles - {difficulty}", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 30)

        level_rects = []
        for row in range(grid_rows):
            for col in range(grid_cols):
                level_num = row * grid_cols + col + 1
                x = padding + col * spacing_x
                y = padding + 40 + row * spacing_y
                level_rect = pygame.Rect(x - icon_size // 2, y - icon_size // 2, icon_size, icon_size)
                pygame.draw.rect(virtual_screen, (100, 100, 100), level_rect)
                draw_text(str(level_num), font, (255, 255, 255), virtual_screen, x, y)
                level_rects.append(level_rect)

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(level_rects):
                        if rect.collidepoint(scaled_mx, scaled_my):
                            start_transition('fade', 'out', level_screen)
                            return

        if crt_filter:
            virtual_screen = apply_crt_filter(virtual_screen)

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        handle_transition()
        pygame.display.update()
        mainClock.tick(60)

def difficulty_select(game_type):
    global virtual_screen
    running = True
    difficulties = ["Easy", "Medium", "Hard"]
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text(f"{game_type} - Select Difficulty", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 30)

        button_rects = []
        for i, diff in enumerate(difficulties):
            button_rect = draw_button(virtual_screen, diff, ORIGINAL_WIDTH // 2, 80 + i * 40)
            button_rects.append(button_rect)
            draw_text(diff, font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 80 + i * 40)

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(scaled_mx, scaled_my):
                            start_transition('push', 'out')
                            levels_layout(difficulties[i])
                            return

        if crt_filter:
            virtual_screen = apply_crt_filter(virtual_screen)

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        handle_transition()
        pygame.display.update()
        mainClock.tick(60)


def game_select():
    global virtual_screen
    running = True
    game_types = ["Classic", "Color", "Custom"]
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text("Select Game Type", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 30)

        button_rects = []
        for i, game_type in enumerate(game_types):
            button_rect = draw_button(virtual_screen, game_type, ORIGINAL_WIDTH // 2, 80 + i * 40)
            button_rects.append(button_rect)
            draw_text(game_type, font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 80 + i * 40)

        mx, my = pygame.mouse.get_pos()
        scaled_mx = int(mx / scale_factor)
        scaled_my = int(my / scale_factor)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(scaled_mx, scaled_my):
                            start_transition('push', 'out')
                            difficulty_select(game_types[i])
                            return

        if crt_filter:
            virtual_screen = apply_crt_filter(virtual_screen)

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        handle_transition()
        pygame.display.update()
        mainClock.tick(60)


def options_menu():
    global virtual_screen, click, scale_factor, screen
    running = True
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text("Options", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 30)

        button_texts = ["Controls", "Video", "Audio"]
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
                            start_transition('push', 'out')
                            if i == 0:
                                controls()
                            elif i == 1:
                                video_options()
                            elif i == 2:
                                audio()
                            return

        if crt_filter:
            virtual_screen = apply_crt_filter(virtual_screen)

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        handle_transition()
        pygame.display.update()
        mainClock.tick(60)


def controls():
    global virtual_screen
    running = True
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text("Controls", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 4)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        if crt_filter:
            virtual_screen = apply_crt_filter(virtual_screen)

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        handle_transition()
        pygame.display.update()
        mainClock.tick(60)


def audio():
    global virtual_screen
    running = True
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text("Audio", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 4)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        if crt_filter:
            virtual_screen = apply_crt_filter(virtual_screen)

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        handle_transition()
        pygame.display.update()
        mainClock.tick(60)


def create():
    global virtual_screen
    running = True
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text("Create", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 4)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        if crt_filter:
            virtual_screen = apply_crt_filter(virtual_screen)

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        handle_transition()
        pygame.display.update()
        mainClock.tick(60)


def achievements():
    global virtual_screen
    running = True
    while running:
        virtual_screen.fill((0, 0, 0))
        draw_text("Achievements", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 4)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        if crt_filter:
            virtual_screen = apply_crt_filter(virtual_screen)

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        handle_transition()
        pygame.display.update()
        mainClock.tick(60)


def main_menu():
    global virtual_screen, click, scale_factor, screen, confirm_exit
    click = False
    confirm_exit = False
    current_screen = 'main'

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
                        start_transition('fade', 'out')
                        if i == 0:
                            game_select()
                        elif i == 1:
                            options_menu()
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

        if crt_filter:
            virtual_screen = apply_crt_filter(virtual_screen)

        scaled_surface = pygame.transform.scale(virtual_screen,
                                                (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        handle_transition()
        pygame.display.update()
        mainClock.tick(60)


if __name__ == '__main__':
    main_menu()

