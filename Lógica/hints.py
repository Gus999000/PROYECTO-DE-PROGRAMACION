from comparar_matriz import matriz_solucion
def generate_hints(lines):
    hints = []
    for line in lines:
        hint = []
        count = 0
        for cell in line:
            if cell == 1:
                count += 1
            elif count > 0:
                hint.append(count)
                count = 0
        if count > 0:
            hint.append(count)
        hints.append(hint if hint else [0])     # Esto es por si no hay ni una casilla pintada en la fila/columna
    return hints

def get_row_hints(solution):
    return generate_hints(solution)

def get_col_hints(solution):
    transposed_solution = solution.T  # Transponer usando numpy
    return generate_hints(transposed_solution)

# Ejemplos 
solution = matriz_solucion

row_hints = get_row_hints(solution)
col_hints = get_col_hints(solution)
print("Ejemplo 1")
print("Pistas de filas:", row_hints)
print("Pistas de columnas:", col_hints)
print("\n")
