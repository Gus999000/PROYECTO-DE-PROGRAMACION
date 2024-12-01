import numpy as np

def cargarNPZ(nombre: str, id: str):
    with np.load(nombre) as data:
        return data[id]

def guardarNPZ(nombre: str, id: str, matriz: np.ndarray):
    #Revisa si el archivo ya existe y carga matrices existentes si es que existe, si no existe, inicia con un diccionario vacío
    try:
        data = dict(np.load(nombre))
    except FileNotFoundError:
        data = {}

    #Agregar o actualizar la matriz con el id dado
    data[id] = matriz

    #Guardar todas las matrices en el archivo
    np.savez(nombre, **data)