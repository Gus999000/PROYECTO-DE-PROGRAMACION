import pygame as pg

class Button():
    def __init__(self, pos_x, pos_y, scale, img_path):
        self.__rec = [pos_x, pos_y, scale, scale]
        self.image = pg.image.load(img_path)
        self.image = pg.transform.scale(self.image,(scale,scale))

    def isColliding(self):
        CollideBox = pg.Rect(self.__rec[0], self.__rec[1], self.__rec[2], self.__rec[3])
        if CollideBox.collidepoint(pg.mouse.get_pos()):
            return True
        else:
            return False

    def setImage(self, img_path):
        self.image = pg.image.load(img_path)
        self.image = pg.transform.scale(self.image, (scale,scale))

    def getPos(self):
        return self.__rec

class Button_notSquare():
    def __init__(self, pos_x, pos_y, width ,height, img_path):
        self.__rec = [pos_x, pos_y, width, height]
        self.image = pg.image.load(img_path)
        self.image = pg.transform.scale(self.image,(width,height))

    def isColliding(self):
        CollideBox = pg.Rect(self.__rec[0], self.__rec[1], self.__rec[2], self.__rec[3])
        if CollideBox.collidepoint(pg.mouse.get_pos()):
            return True
        else:
            return False

    def setImage(self, img_path):
        self.image = pg.image.load(img_path)
        self.image = pg.transform.scale(self.image, (width,height))

    def getPos(self):
        return self.__rec

class Button_notScaled():
    def __init__(self, pos_x, pos_y, width ,height, img_path):
        self.__rec = [pos_x, pos_y, width, height]
        self.image = pg.image.load(img_path)

    def isColliding(self):
        CollideBox = pg.Rect(self.__rec[0], self.__rec[1], self.__rec[2], self.__rec[3])
        if CollideBox.collidepoint(pg.mouse.get_pos()):
            return True
        else:
            return False

    def updatePos(self, new_x, new_y, width, height):
        self.__rec = [new_x, new_y, width, height]

    def setImage(self, img_path):
        self.image = pg.image.load(img_path)

    def getPos(self):
        return self.__rec
