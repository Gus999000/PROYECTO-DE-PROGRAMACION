from PIL import Image
import numpy as np

def importarIMG(ruta: str):
    #Cargar la imagen
    imagen = Image.open(ruta)

    #Cambiar la resolución
    nueva_resolución = (100, 100)
    imagen_nueva = imagen.resize(nueva_resolución)

    #Convertir la imagen a una matriz
    matriz_imagen = np.array(imagen_nueva)
    return matriz_imagen

#def dibujarNN():