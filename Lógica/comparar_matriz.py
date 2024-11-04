import numpy as np
import os

# Crear una ruta relativa basada en la ubicación de este archivo
current_dir = os.path.dirname(__file__)
npz_path = os.path.join(current_dir, 'solutions.npz')

# Cargar la matriz desde el archivo .npz
with np.load(npz_path) as data:
    matriz_solucion = data['nonogram_1']

matriz_usuario = np.zeros_like(matriz_solucion)

def is_solved(self):
    return np.array_equal(matriz_solucion, self)

print("¿Nonograma resuelto?", is_solved(matriz_usuario))