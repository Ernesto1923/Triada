import sys

def solve():
    # Lectura eficiente de toda la entrada estándar de una sola vez
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    T_cases = int(next(iterator))
    
    output = []
    
    for _ in range(T_cases):
        N = int(next(iterator))
        K_float = float(next(iterator))
        
        # Multiplicamos por 1,000,000 para trabajar enteramente con enteros
        # y evitar problemas de precisión con punto flotante (IEEE 754).
        K = int(round(K_float * 1000000))
        
        arr = []
        for _ in range(N):
            val_str = next(iterator)
            if val_str == '?':
                arr.append(None)
            else:
                arr.append(int(round(float(val_str) * 1000000)))
        
        # Variables para almacenar la mejor racha (longitud máxima y posición de inicio 1-indexed)
        max_len = 0
        best_start = 1
        
        # Si N == 0, caso borde
        if N == 0:
            output.append("0 1")
            continue
            
        # Algoritmo de exploración lineal optimizado O(N)
        # Gestionamos tramos continuos considerando '?' como elementos válidos de enlace o expansión.
        current_len = 0
        current_start = 1
        
        # Implementación eficiente basada en la validación de diferencias y tolerancia K
        i = 0
        while i < N:
            # Iniciamos una nueva racha en i
            start = i
            current_len = 1
            
            j = i + 1
            while j < N:
                # Verificamos la estabilidad con el elemento anterior válido o contiguo
                # Si hay '?', evaluamos la distancia respetando la tolerancia acumulada o el salto permitido.
                # Condición de estabilidad simplificada para vecinos o elementos con '?' intermediarios:
                if arr[j] is not None and arr[j-1] is not None:
                    if abs(arr[j] - arr[j-1]) > K:
                        break
                elif arr[j] is not None:
                    # Si hay '?' intermedios, buscamos el último valor válido anterior para verificar la distancia total
                    prev_valid_idx = j - 1
                    while prev_valid_idx >= start and arr[prev_valid_idx] is None:
                        prev_valid_idx -= 1
                    
                    if prev_valid_idx >= start:
                        steps = j - prev_valid_idx
                        if abs(arr[j] - arr[prev_valid_idx]) > K * steps:
                            break
                
                current_len += 1
                j += 1
            
            # Actualizamos la mejor racha encontrada
            if current_len > max_len:
                max_len = current_len
                best_start = start + 1 # Convertimos a 1-indexed
            elif current_len == max_len:
                if (start + 1) < best_start:
                    best_start = start + 1
            
            # Avanzamos eficientemente
            i = j if j > i + 1 else i + 1

        output.append(f"{max_len} {best_start}")
        
    # Imprimimos todos los resultados de forma eficiente con '\n'
    sys.stdout.write('\n'.join(output) + '\n')

if __name__ == '__main__':
    solve()
