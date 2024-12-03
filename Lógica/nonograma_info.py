import numpy as np
import os

from Gráfica.Create_Nonograma import WINDOW_SCALE

"""
Casa: n001 (5x5)
Fuerte: n002 (5x5)
2: n003 (6x6)
Pikachu: n004 (10x10)
Ignored: n005 (8x8)
Café: n006 (10x10)
Casco: n007 (10x10)
Mario: n008 (10x10)
Game Boy: n101 (15x15)
Super Estrella: n102 (15x15)
Mago: n103 (15x15)
Rata: n104 (15x15)
Bicho: n105 (17x17)
Ying-Yang: n106 (18x18)
Aperture Science: n107 (20x20)
Bomba: n108 (20x20)
Micro: n201 (20x20)
Dino: n202 (20x20)

"""
window_scale = 3

def set_variable(value):
    global window_scale
    window_scale = value
def get_variable():
    return window_scale

id_nonograma = 'n106'

# Crear una ruta relativa basada en la ubicación de este archivo
current_dir = os.path.dirname(__file__)
nonograms_path = os.path.join(current_dir, 'nonograms.npz')
metadata_path = os.path.join(current_dir, 'nonograms_metadata.npz')

# Cargar la matriz y metadatos desde el archivo .npz
with np.load(nonograms_path) as nonograms_data:
    matriz_solucion = nonograms_data[id_nonograma]                    # Acceder a los nonogramas

with np.load(metadata_path, allow_pickle=True) as metadata:
    metadata_nonograma = metadata[id_nonograma].item()           # Acceder a los metadatos


matriz_usuario = np.zeros_like(matriz_solucion)

def is_solved(self):
    matriz_limpia = self.copy()
    matriz_limpia[matriz_limpia != 1] = 0
    return np.array_equal(matriz_solucion, matriz_limpia)

# Imprimir metadatos del nonograma
print("Información del Nonograma")
print(f"Título: {metadata_nonograma['title']}")
print(f"Descripción: {metadata_nonograma['description']}")
print(f"Tamaño: {metadata_nonograma['size'][0]}x{metadata_nonograma['size'][1]}")
print(f"Color: {metadata_nonograma['color']}")
print(f"Fecha de creación: {metadata_nonograma['date_created']}")