import pygame as pg

def draw_text(text, font, color, size, x, y, surface):

    pg.font.init()
    match font:
        case "Arial":
            myfont = pg.font.SysFont("Arial", size)
        case _:
            myfont = pg.font.SysFont("Arial", size)

    img = myfont.render(text, True, color)
    surface.blit(img, (x,y))