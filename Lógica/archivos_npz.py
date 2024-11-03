import numpy as np

def cargarNPZ(nombre: str, id: str):
    """"cargarNPZ recibe el nombre del archivo, el id de la matriz y devuelve la matriz correspondiente"""
    matriz = np.load(nombre + ".npz")
    return matriz[id]

def guardarNPZ(nombre: str, id: str, matriz: np.ndarray):
    """guardarNPZ recibe el nombre e id de la matriz junto con la matriz en cuestión y crea un archivo .npz, si el archivo ya existe, lo sobrescribe"""
    np.savez(nombre + ".npz", matriz=id)