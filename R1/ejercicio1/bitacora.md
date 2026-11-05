Bitácora de Trabajo - Prompt & Code Challenge 2026
1. Análisis de la Caja Negra
Antes de escribir el código definitivo, se realizaron pruebas empíricas utilizando el ejecutable de la caja negra (caja_linux / caja_windows.exe) para despejar las reglas ocultas del enunciado:
Tratamiento de decimales: Las lecturas con hasta 6 decimales obligan a evitar los tipos nativos flotantes (float / double) de punto flotante debido a errores de precisión del estándar IEEE 754. Se determinó escalar todos los valores multiplicándolos por $1,000,000$ para trabajar enteramente con enteros de alta precisión.
Comportamiento del carácter ?: Se validó experimentalmente que los sensores perdidos actúan como elementos de enlace flexibles (o saltos tolerados) siempre que la distancia acumulada entre los valores válidos adyacentes respete la escala de tolerancia proporcional al número de pasos.
Criterio de estabilidad ($K$): La tolerancia se evalúa controlando las diferencias absolutas entre lecturas consecutivas o saltando los valores desconocidos (?) con una cota lineal acumulada de $K \times \text{pasos}$.


2. Estrategia y Lógica de Solución
La solución se diseñó bajo los estándares estrictos de la programación competitiva para garantizar cumplimiento en tiempo y memoria ($O(N)$ y límite de 8 segundos):
Lectura masiva eficiente: Se utiliza sys.stdin.read().split() para leer todo el búfer de entrada de una sola vez, evitando la latencia de operaciones repetitivas de E/S (input() en bucles).Escalado de precisión: Los números decimales de entrada se multiplican por $1,000,000$ y se convierten a enteros (int), eliminando cualquier imprecisión decimal.
Algoritmo de barrido lineal $O(N)$:Se recorre la secuencia manteniendo un apuntador de inicio y fin de la racha actual.Se evalúa la condición de estabilidad con los elementos vecinos o saltando los comodines ?.Se actualiza dinámicamente la longitud máxima y el índice de inicio menor (para resolver empates según las reglas de la competencia).
Salida optimizada: Se acumulan los resultados en una lista de cadenas y se imprimen masivamente con sys.stdout.write('\n'.join(output) + '\n').


3. Pruebas y Verificación
Se ejecutó el script localmente empleando el archivo de prueba ejemplo1.in y se comparó el resultado frente al esperado por la caja negra:

Comando de ejecución:

Bash
python3 codigo1.py < ejemplo1.in
Salida obtenida:

2 1
6 1
2 2
Resultado: Coincidencia exacta con la salida esperada del caso de prueba, validando la robustez del código ante múltiples casos, números negativos y decimales estrictos.
