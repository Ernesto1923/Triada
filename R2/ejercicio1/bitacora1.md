# Bitácora Técnica: Resolución del Problema "BF - Ventas Masivas"

## 1. Información General

* **Nombre del Reto:** BF - Ventas masivas
* **Competencia / Ronda:** Gran Final (Ronda 2 - Categoría Básica)
* **Restricciones del Sistema:**
  * **Tiempo Límite:** 16.0 segundos
  * **Memoria Límite:** 64.0 MB (Estricto)
  * **Volumen de Entrada:** Hasta $3,000,000$ de registros ($\approx 90\text{ MB}$ de datos crudos en texto plano)
* **Objetivo:** Filtrar y acumular ventas válidas procesando el flujo de datos dentro de un rango de fechas $[D_1, D_2]$, deduplicar ventas por `id_venta`, e imprimir hasta los 3 productos con mayor total de ventas acumuladas. En caso de empate en ventas, priorizar por menor `producto_id`. Si no existen registros válidos, retornar `"SIN DATOS"`.

---

## 2. Análisis de la Caja Negra y Reglas de Negocio

A través del análisis del formato y casos de prueba, se establecieron las siguientes reglas empíricas de filtrado:

1. **Estructura de la Entrada:**
   * **Línea 1:** Rango de fechas válido (`D1 D2`).
   * **Línea 2:** Número total de registros $N$.
   * **Líneas $3$ a $N+2$:** Registros de venta con formato `fecha id_venta producto_id cantidad`.

2. **Criterios de Invalidez de Registros:**
   * Registros con menos de 4 campos requeridos.
   * Errores de parseo o tipos no enteros en `producto_id` o `cantidad`.
   * Identificadores de producto fuera del rango válido ($1 \le \text{producto\_id} \le 100,000$).
   * Cantidades no positivas ($\text{cantidad} \le 0$).
   * Fechas fuera del rango inclusivo $[D_1, D_2]$.

3. **Manejo de Duplicados (`id_venta`):**
   * Se considera únicamente la **primera ocurrencia** válida de un `id_venta`. Ocurrencias posteriores con el mismo identificador son ignoradas.

---

## 3. Arquitectura y Optimización de Memoria

Para garantizar el cumplimiento del límite estricto de **64 MB** al procesar **90 MB** de texto, se aplicaron estrategias de optimización extrema en Python:

### a) Procesamiento por Streaming en E/S Nivel Byte
Cargar todo el texto a memoria usando métodos como `sys.stdin.read().split()` crearía millones de objetos `str` y punteros de lista, disparando el uso de RAM por encima de los 300 MB. 

* **Solución:** Iteración directa en streaming a nivel de bytes mediante `sys.stdin.buffer`. De esta forma, solo se mantiene una línea en memoria RAM a la vez, permitiendo que el recolector de basura de Python mantenga el *footprint* de memoria base cercano a cero.

### b) Comparación Eficiente de Fechas
En lugar de instanciar objetos costosos como `datetime.date`, el formato estándar `YYYY-MM-DD` permite la comparación lexicográfica directa entre cadenas de bytes (`bytes`), reduciendo a $\mathcal{O}(1)$ el costo de filtrado por fecha.

### c) Estructura de Datos de Tamaño Fijo para Acumulación
Dado que el identificador de producto está acotado ($1 \le \text{producto\_id} \le 100,000$), se utiliza una lista plana estática de enteros `[0] * 100001`. 
* Esto evita la sobrecarga de tablas hash de los diccionarios nativos (`dict`).
* La actualización y acceso se realiza por índice en tiempo estricto $\mathcal{O}(1)$ con consumo de memoria inferior a **1 MB**.

### d) Control de Duplicados
Un conjunto `set()` mantiene el registro de `id_venta` procesados. Dado el alcance de memoria disponible, el `set` almacena cadenas de bytes compactas manteniendo el pico de consumo dentro del margen tolerado por la restricción de 64 MB.

### e) Análisis de Complejidad
* **Complejidad Temporal:** $\mathcal{O}(N)$ donde $N \le 3,000,000$. Cada línea requiere operaciones de parsing y validación $\mathcal{O}(1)$. El ordenamiento final aplica sobre máximo $100,000$ elementos no nulos ($\mathcal{O}(K \log K)$ donde $K \le 100,000$). Tiempo de ejecución estimado: $< 3.5$ segundos (muy inferior al límite de 16 s).
* **Complejidad Espacial:** $\mathcal{O}(U)$ en el peor caso, donde $U$ es la cantidad de `id_venta` únicos procesados, acotada estrictamente dentro de los 64 MB.

---

## 4. Código Final Optimizado

```python
import sys

def main():
    d1 = None
    d2 = None
    n_skipped = False
    vistos = set()
    totales = [0] * 100001
    hay_datos = False

    # Lectura en streaming a nivel de bytes para evitar overhead de memoria
    for line in sys.stdin.buffer:
        parts = line.split()
        if not parts:
            continue

        # Lectura de la ventana de fechas (D1, D2)
        if d1 is None:
            if len(parts) >= 2:
                d1 = parts[0]
                d2 = parts[1]
            continue

        # Ignorar la línea con la cantidad N de registros
        if not n_skipped:
            n_skipped = True
            continue

        # Parsing y validación rápida
        try:
            if len(parts) < 4:
                continue
            fecha = parts[0]
            id_venta = parts[1]
            prod_id = int(parts[2])
            cantidad = int(parts[3])

            # Filtrado por rango de fechas inclusivo
            if not (d1 <= fecha <= d2):
                continue

            # Filtrado de id_venta duplicados
            if id_venta in vistos:
                continue

            # Validación de identificador de producto y cantidad positiva
            if 1 <= prod_id <= 100000 and cantidad > 0:
                vistos.add(id_venta)
                totales[prod_id] += cantidad
                hay_datos = True
        except (ValueError, IndexError):
            continue

    # Si no hubo registros válidos procesados
    if not hay_datos:
        sys.stdout.write("SIN DATOS\n")
        return

    # Selección de productos con ventas acumuladas
    productos_con_ventas = [
        (p, totales[p]) for p in range(1, 100001) if totales[p] > 0
    ]
    
    # Ordenamiento: 1º Mayor cantidad vendida (-x[1]), 2º Menor ID de producto (x[0])
    productos_con_ventas.sort(key=lambda x: (-x[1], x[0]))

    # Construcción de la salida formateada en bytes
    salida = []
    for p, t in productos_con_ventas[:3]:
        salida.append(f"{p} {t}".encode("ascii"))

    sys.stdout.buffer.write(b"\n".join(salida) + b"\n")

if __name__ == "__main__":
    main()
```