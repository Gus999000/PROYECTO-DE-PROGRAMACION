from PIL import Image
import numpy as np

def importarIMG(ruta: str):
    try:
        #Cargar la imagen
        imagen = Image.open(ruta)

        #Convertir la imagen a escala de grises
        imagen_gris = imagen.convert('L')

        #Cambiar la resolución
        nueva_resolucion = (25, 25)
        imagen_redimensionada = imagen_gris.resize(nueva_resolucion)

        #Convertir la imagen a una matriz
        matriz_imagen = np.array(imagen_redimensionada)

        #Convertir los valores de los píxeles a 0 (blanco) o 1 (negro)
        matriz_binaria = np.where(matriz_imagen > 127, 0, 1)

        return matriz_binaria
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None

def importarIMG_color(ruta: str):
    try:
        #Cargar la imagen
        imagen = Image.open(ruta)

        #Asegurar que la imagen esté en modo RGB
        imagen_rgb = imagen.convert('RGB')

        #Cambiar la resolución
        nueva_resolucion = (25, 25)
        imagen_redimensionada = imagen_rgb.resize(nueva_resolucion)

        #Convertir la imagen a una matriz
        matriz_imagen = np.array(imagen_redimensionada)

        #Convertir cada píxel a código hexadecimal
        matriz_hex = np.array([[
            f"#{r:02X}{g:02X}{b:02X}" for r, g, b in fila
        ] for fila in matriz_imagen])

        return matriz_hex
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None