import numpy as np

def cargarNPZ(nombre: str):
    """"cargarNPZ recibe el nombre del archivo y devuelve la matriz contenida en este"""
    matriz = np.load(nombre + ".npz")
    return matriz["arr_0"]

def guardarNPZ(nombre: str, matriz: np.ndarray):
    """guardarNPZ recibe el nombre de la matriz junto con la matriz en cuestión y crea un archivo .npz con el nombre de la matriz, si el archivo ya existe, lo sobrescribe"""
    np.savez(nombre + ".npz", matriz)