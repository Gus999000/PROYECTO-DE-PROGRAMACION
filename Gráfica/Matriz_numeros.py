import pygame as pg

class matriz_numeros():
    max_numbers = 0
    puzzle_size = 0
    def __init__(self, size):
        self.puzzle_size = size
        # Limitar la cantidad máxima de números que habrán según el tamaño del puzzle
        if size%2 == 0:
            self.max_numbers = size//2
        else:
            self.max_numbers = (size - 1)//2
        self.matriz_filas = [[0 for i in range(self.max_numbers)] for j in range(size)]
        self.matriz_columnas = [[0 for i in range(self.max_numbers)] for j in range(size)]

    def set_matriz_filas(self, matriz_num):
        index = 0
        for i in range(self.puzzle_size):
            for j in range(len(matriz_num[index])):
                self.matriz_filas[i][j] = matriz_num[i][len(matriz_num[index])-j-1]
            index += 1

    def set_matriz_columnas(self, matriz_num):
        index = 0
        for i in range(self.puzzle_size):
            for j in range(len(matriz_num[index])):
                self.matriz_columnas[i][j] = matriz_num[i][len(matriz_num[index])-j-1]
            index += 1

    def get_puzzle_size(self):
        return self.puzzle_size

    def get_max_numbers(self):
        return self.max_numbers

    def get_matriz_fila_value(self, i, j):
        return self.matriz_filas[i][j]

    def get_matriz_columna_value(self, i, j):
        return self.matriz_columnas[i][j]