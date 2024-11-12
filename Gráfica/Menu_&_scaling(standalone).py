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

# ventana virutal
virtual_screen = pygame.Surface((ORIGINAL_WIDTH, ORIGINAL_HEIGHT))

# Renderizacion de texto
title_font = pygame.font.Font('Vermin Vibes.ttf', 36)
font = pygame.font.SysFont('OCR-A Extended', 12, bold=True)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)


click = False
confirm_exit = False


def main_menu():
    global click, scale_factor, screen, confirm_exit
    while True:
        # Gradiente en fondo
        for y in range(ORIGINAL_HEIGHT):
            color = (0 + y // 4, 0 + y //12, 0 + y // 3)
            pygame.draw.line(virtual_screen, color, (0, y), (ORIGINAL_WIDTH, y))

        # Dibuja texto
        draw_text('PLACEHOLDER', title_font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 4)

        # Display de botones y funcionalidad
        button_texts = ["Play", "Options", "Create", "Achievements"]
        for i, text in enumerate(button_texts):
            draw_text(text, font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, ORIGINAL_HEIGHT // 2 - 20 + i * 20)

        mx, my = pygame.mouse.get_pos()
        mx = int(mx / scale_factor)
        my = int(my / scale_factor)

        if not confirm_exit:
            # logica de botones, deteccion de click
            if click:
                if ORIGINAL_HEIGHT // 2 - 30 <= my <= ORIGINAL_HEIGHT // 2 - 20:
                    play()
                elif ORIGINAL_HEIGHT // 2 - 10 <= my <= ORIGINAL_HEIGHT // 2:
                    options()
                elif ORIGINAL_HEIGHT // 2 + 10 <= my <= ORIGINAL_HEIGHT // 2 + 20:
                    create()
                elif ORIGINAL_HEIGHT // 2 + 30 <= my <= ORIGINAL_HEIGHT // 2 + 40:
                    achievements()
            click = False
        # volver atras dentro de menus
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    confirm_exit = True
                elif event.key == K_UP:
                    scale_factor += 1
                    screen = pygame.display.set_mode((ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor), RESIZABLE)
                elif event.key == K_DOWN and scale_factor > 1:
                    scale_factor -= 1
                    screen = pygame.display.set_mode((ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor), RESIZABLE)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Popup de salida del programa
        if confirm_exit:
            pygame.draw.rect(virtual_screen, (0, 0, 0), (50, 80, 156, 80))
            pygame.draw.rect(virtual_screen, (255, 255, 255), (50, 80, 156, 80), 2)
            draw_text("Are you sure you", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 100)
            draw_text("want to exit?", font, (255, 255, 255), virtual_screen, ORIGINAL_WIDTH // 2, 120)
            draw_text("Yes", font, (255, 255, 255), virtual_screen, 90, 150)
            draw_text("No", font, (255, 255, 255), virtual_screen, 165, 150)

            # Deteccion de cursor popup
            if click:
                if 80 <= mx <= 100 and 140 <= my <= 160:
                    pygame.quit()
                    sys.exit()
                elif 155 <= mx <= 175 and 140 <= my <= 160:
                    confirm_exit = False
                click = False

        # Escalamiento de ventana virtual a tamaño real de ventana
        scaled_surface = pygame.transform.scale(virtual_screen, (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.update()
        mainClock.tick(60)


def play():
    sub_screen("Juego")


def options():
    sub_screen("Opciones")


def create():
    sub_screen("Crear")


def achievements():
    sub_screen("Logros")

# Funcionalidad general sub-ventanas del menu
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

        scaled_surface = pygame.transform.scale(virtual_screen, (ORIGINAL_WIDTH * scale_factor, ORIGINAL_HEIGHT * scale_factor))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.update()
        mainClock.tick(60)


main_menu()
