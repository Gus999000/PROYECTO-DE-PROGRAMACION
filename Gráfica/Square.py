import pygame as pg

WINDOW_SCALE = 3

class Square(pg.sprite.Sprite):

    Filled = False
    x = 0
    y = 0
    size = 0
    def __init__(self, pos_x, pos_y, scale):
        #Hereda pg.sprite.Sprite
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.size = scale
        # {pos_x, pox_y, width, height}
        self.rec = pg.Rect(pos_x,pos_y,scale,scale)
        if not self.Filled:
            self.image = pg.image.load("Gráfica/resources/Square.png")
        else:
            self.image = pg.image.load("Gráfica/resources/SquareFill.png")

        self.image = pg.transform.scale(self.image,(scale,scale))

    def isColliding(self):
        return self.rec.collidepoint(pg.mouse.get_pos())

    def changeImage(self):
        if self.Filled:
            self.image = pg.image.load("Gráfica/resources/Square.png")
            self.Filled = False
        else:
            self.image = pg.image.load("Gráfica/resources/SquareFill.png")
            self.Filled = True
        self.image = pg.transform.scale(self.image, (self.rec[2], self.rec[2]))

    def setAlpha(self, alpha):
        self.image.set_alpha(alpha)

    def updatePos(self,new_x, new_y):
        self.rec.topleft = (new_x,new_y)

    def isFilled(self):
        if self.Filled:
            return 1
        else:
            return 0

    def getPos(self):
        return self.rec