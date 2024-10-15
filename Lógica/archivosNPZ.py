import numpy as np

def cargarNPZ(nombre: str):
    matriz = np.load(nombre + ".npz")
    return matriz["arr_0"]

def guardarNPZ(nombre: str, matriz: np.ndarray):
    if matriz.ndim == 2:
        np.savez(nombre + ".npz", matriz)
    else:
        print("error")