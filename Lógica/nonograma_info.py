import numpy as np
import os

"""
Casa: n001 (5x5)
Fuerte: n002 (5x5)
2: n003 (6x6)
Pikachu: n100 (10x10)
Ignored: n101 (8x8)
Café: n102 (10x10)
Casco: n103 (10x10)
Mario: n104 (10x10)
Game Boy: n200 (15x15)
Super Estrella: n201 (15x15)
Mago: n202 (15x15)
Rata: n203 (15x15)
Bicho: n300 (17x17)
Micro: n301 (20x20)
Ying-Yang: n302 (18x18)
Aperture Science: n303 (20x20)
Bomba: n304 (20x20)
Dino: n305 (20x20)

"""

id_nonograma = 'n302'

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