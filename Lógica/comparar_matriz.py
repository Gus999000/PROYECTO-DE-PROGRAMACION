import numpy as np

with np.load('Lógica/solutions.npz') as data:
    # Acceder al nonograma por su id
    matriz_solucion = data['Matriz_Amongus']

matriz_usuario = np.zeros_like(matriz_solucion)

def is_solved(self):
    return np.array_equal(matriz_solucion, self)

print("¿Nonograma resuelto?", is_solved(matriz_usuario))