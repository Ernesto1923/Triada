import sys

def solve():
    # Leer toda la entrada en bytes
    raw_data = sys.stdin.buffer.read().splitlines()
    if not raw_data:
        sys.stdout.write("SIN DATOS\n")
        return
    
    # Filtrar líneas vacías o limpiar espacios iniciales/finales si los hubiera
    input_data = [line.strip() for line in raw_data if line.strip()]
    if len(input_data) < 2:
        sys.stdout.write("SIN DATOS\n")
        return
    
    # Línea 1: Rango de fechas D1 y D2
    dates = input_data[0].split()
    if len(dates) < 2:
        sys.stdout.write("SIN DATOS\n")
        return
    
    d1 = dates[0].replace(b'-', b'')
    d2 = dates[1].replace(b'-', b'')
    
    try:
        n_line = int(input_data[1])
    except (ValueError, IndexError):
        sys.stdout.write("SIN DATOS\n")
        return
    
    vistos_id = set()
    totales = [0] * 100005
    has_data = False
    
    for i in range(2, 2 + n_line):
        if i >= len(input_data):
            break
        line = input_data[i]
        
        parts = line.split(b',')
        if len(parts) != 4:
            continue
        
        # Limpiar posibles espacios en blanco en cada campo
        fecha = parts[0].strip()
        id_v = parts[1].strip()
        prod_id = parts[2].strip()
        cant = parts[3].strip()
        
        if len(fecha) != 10:
            continue
            
        f_int = fecha.replace(b'-', b'')
        if not (d1 <= f_int <= d2):
            continue
            
        try:
            id_val = int(id_v)
            p_id = int(prod_id)
            cantidad = int(cant)
        except ValueError:
            continue
            
        if not (1 <= p_id <= 100000):
            continue
            
        # Ventas repetidas: La primera ocurrencia cuenta
        if id_val in vistos_id:
            continue
        vistos_id.add(id_val)
        
        totales[p_id] += cantidad
        has_data = True
        
    if not has_data:
        sys.stdout.write("SIN DATOS\n")
        return
        
    productos = []
    for p in range(1, 100001):
        if totales[p] != 0:
            productos.append((totales[p], -p))
            
    if not productos:
        sys.stdout.write("SIN DATOS\n")
        return
        
    # Ordenar de mayor a menor total, y en empate menor producto_id
    productos.sort(key=lambda x: (x[0], x[1]), reverse=True)
    
    salida = []
    for i in range(min(3, len(productos))):
        tot, neg_p = productos[i]
        p = -neg_p
        salida.append(f"{p} {tot}")
        
    sys.stdout.write("\n".join(salida) + "\n")

if __name__ == '__main__':
    solve()
