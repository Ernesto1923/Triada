# Registro Completo de Conversación y Documentación Técnica: Ejercicio 2 (La Impresora) — Ronda 1

Documento de registro colaborativo para la resolución del problema **La Impresora** (Ronda 1, Ejercicio 2), incluyendo la fase de análisis empírico (caja negra), el diseño de experimentos, la implementación en Python 3 optimizada para alto rendimiento, y la documentación de arquitectura.

---

## Índice
1. [Perfil y Rol Técnico](#1-perfil-y-rol-técnico)
2. [Fase 1: Planteamiento del Problema e Incógnitas](#2-fase-1-planteamiento-del-problema-e-incógnitas)
3. [Fase 2: Diseño de Experimentos de Caja Negra](#3-fase-2-diseño-de-experimentos-de-caja-negra)
4. [Fase 3: Código de Solución Completo en Python 3](#4-fase-3-código-de-solución-completo-en-python-3)
5. [Fase 4: Análisis de Complejidad y Estrategia de Optimización](#5-fase-4-análisis-de-complejidad-y-estrategia-de-optimización)

---

## 1. Perfil y Rol Técnico

* **Rol:** Ingeniero de Software competitivo especializado en estructuras de datos, optimización de tiempo/memoria y resolución de problemas de caja negra.
* **Lenguaje y Entorno:** Python 3 (utilizando E/S por buffer con `sys.stdin.buffer.read` y gestión eficiente de heaps con eliminación perezosa).
* **Objetivo:** Resolver $Q \le 10^6$ operaciones en un tiempo límite de 10.0 segundos y 256 MB de memoria.

---

## 2. Fase 1: Planteamiento del Problema e Incógnitas

### 2.1 Enunciado del Problema
Una impresora procesa $Q$ órdenes secuenciales:
- `ADD id p`: Agrega un trabajo con prioridad `p`.
- `BOOST id x`: Incrementa la prioridad en `x` e imprime `"OK"` si el trabajo está pendiente; si no, imprime `"NO"`.
- `CANCEL id`: Elimina el trabajo del sistema e imprime `"OK"` si está pendiente; si no, imprime `"NO"`.
- `PRINT k`: Extrae e imprime hasta `k` trabajos pendientes (de mayor a menor prioridad), eliminándolos del sistema. Si no hay pendientes, imprime `"VACIA"`.

### 2.2 Restricciones
- Tiempo límite: 10 segundos.
- Memoria máxima: 256 MB.
- $Q \le 10^6$
- $1 \le id \le 2 \cdot 10^6$
- $1 \le p \le 10^9$
- $1 \le x \le 10^{18}$
- $1 \le k \le 10^6$

### 2.3 Incógnitas Iniciales (Comportamiento Oculto de Caja Negra)
1. Criterio de desempate cuando dos trabajos tienen la misma prioridad (¿FIFO, LIFO, menor `id`, mayor `id`?).
2. Efecto de `BOOST` sobre el orden de antigüedad en caso de empate.
3. Posibilidad de re-insertar un `id` previamente cancelado o impreso.

---

## 3. Fase 2: Diseño de Experimentos de Caja Negra

Para aislar empíricamente las reglas del sistema, se formularon los siguientes experimentos mínimos:

### Experimento 1: Prioridades Iguales (FIFO vs ID)
**Entrada:**
```text
4
ADD 20 5
ADD 10 5
PRINT 2
```
* **Hipótesis H1 (FIFO):** Salida `20 10` (llegó primero 20).
* **Hipótesis H2 (Menor ID):** Salida `10 20` (10 < 20).

### Experimento 2: Aislar FIFO de ID Mayor
**Entrada:**
```text
4
ADD 5 10
ADD 15 10
PRINT 2
```
* **Hipótesis H1 (FIFO / Menor ID):** Salida `5 15`.
* **Hipótesis H3 (Mayor ID):** Salida `15 5`.

### Experimento 3: Efecto de BOOST en la Antigüedad
**Entrada:**
```text
4
ADD 10 5
ADD 20 3
BOOST 20 2
PRINT 2
```
* Determina si `BOOST` reinicia el orden de llegada al alcanzar la misma prioridad que un elemento anterior.

### Experimento 4: Ciclo de Vida y Re-inserción
**Entrada:**
```text
5
ADD 7 10
CANCEL 7
ADD 7 15
PRINT 1
```
* Verifica si la eliminación por `CANCEL` permite reinstanciar un trabajo con el mismo `id`.

> **Conclusión confirmada por las reglas finales:**
> - Desempate a igual prioridad: **MENOR ID**.
> - Acumulación de `BOOST`: La prioridad se suma ($p = p + x$).
> - Operaciones inválidas sobre IDs no activos devuelven `"NO"`.

---

## 4. Fase 3: Código de Solución Completo en Python 3

```python
import sys
import heapq

def solve():
    input_data = sys.stdin.buffer.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    Q = int(next(iterator))
    
    MAX_ID = 2000005
    version = [0] * MAX_ID
    prio = [0] * MAX_ID
    is_active = [False] * MAX_ID
    
    heap = []
    out = []
    
    for _ in range(Q):
        cmd = next(iterator).decode('ascii')
        if cmd == 'ADD':
            jid = int(next(iterator))
            p = int(next(iterator))
            version[jid] += 1
            prio[jid] = p
            is_active[jid] = True
            heapq.heappush(heap, (-p, jid, version[jid]))
        elif cmd == 'BOOST':
            jid = int(next(iterator))
            x = int(next(iterator))
            if is_active[jid]:
                prio[jid] += x
                version[jid] += 1
                is_active[jid] = True
                heapq.heappush(heap, (-prio[jid], jid, version[jid]))
                out.append(b"OK")
            else:
                out.append(b"NO")
        elif cmd == 'CANCEL':
            jid = int(next(iterator))
            if is_active[jid]:
                is_active[jid] = False
                out.append(b"OK")
            else:
                out.append(b"NO")
        elif cmd == 'PRINT':
            k = int(next(iterator))
            printed = []
            while heap and len(printed) < k:
                neg_p, jid, ver = heapq.heappop(heap)
                if is_active[jid] and version[jid] == ver and prio[jid] == -neg_p:
                    is_active[jid] = False
                    printed.append(str(jid).encode('ascii'))
            if not printed:
                out.append(b"VACIA")
            else:
                out.append(b" ".join(printed))
                
    sys.stdout.write("\n".join(res.decode('ascii') if isinstance(res, bytes) else res for res in out) + "\n")

if __name__ == '__main__':
    solve()
```

---

## 5. Fase 4: Análisis de Complejidad y Estrategia de Optimización

### 5.1 Complejidad Temporal
- **E/S Rápida:** $O(Q)$ usando `sys.stdin.buffer.read().split()`.
- **ADD / BOOST:** $O(\log N)$ por inserción en `heapq` (donde $N \le Q$).
- **CANCEL:** $O(1)$ gracias a la desactivación perezosa (`is_active[jid] = False`).
- **PRINT:** Extracción con borrado perezoso (Lazy Deletion). Cada elemento entra al heap máximo 2 veces (por `ADD` o `BOOST`), garantizando un costo amortizado total de $O(Q \log Q)$.

### 5.2 Complejidad Espacial
- **Arreglos directos de tamaño $2 \cdot 10^6$:** $\approx 3 \times 16\text{ MB} \approx 48\text{ MB}$.
- **Heap de tuplas y lista de resultados:** $\approx 80\text{ MB}$.
- **Uso total de memoria:** $\approx 130\text{ MB}$, muy inferior al límite de 256 MB.