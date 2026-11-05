# Prompt para Generar la Bitácora de Trabajo en Markdown (`bitacora.md`)

Copia y pega el siguiente prompt en la IA para obtener la bitácora estructurada de tu experimento y avance con el **Ejercicio 2 (La Impresora)**:

---

### 📝 Prompt a enviar:

> **Rol:** Actúa como un Desarrollador de Software y Líder Técnico de Proyectos.
> 
> **Tarea:** Redacta una **bitácora de trabajo completa y profesional** en formato Markdown (`bitacora.md`) para registrar el proceso de análisis, experimentación de la caja negra y diseño técnico del **Ejercicio 2: La Impresora** de la Ronda 1 del Prompt & Code Challenge 2026.
> 
> **Estructura requerida para el documento:**
> 
> 1. **Encabezado e Información del Proyecto:**
>    - Título del proyecto/ejercicio.
>    - Nombre de la Ronda (Ronda 1 - Categoría Básica).
>    - Fecha de ejecución y estado actual del trabajo (Fase de Experimentación y Diseño).
> 
> 2. **Resumen del Problema:**
>    - Breve descripción del comportamiento de la Impresora (`ADD`, `BOOST`, `CANCEL`, `PRINT k`).
>    - Restricciones técnicas ($Q \le 10^6$ operaciones, Límite de tiempo: 10s, Memoria: 256 MB).
> 
> 3. **Diseño del Plan de Experimentación (Caja Negra):**
>    - Descripción de la metodología empírica aplicada para descubrir reglas ocultas.
>    - Detalle de los **5 experimentos diseñados** (Objetivo, Entrada `.in` utilizada y las Hipótesis evaluadas sobre criterios de desempate, persistencia y reuso de IDs).
> 
> 4. **Prompts y Metodología de IA:**
>    - Registro detallado de los prompts clave utilizados para guiar la solución estructurada paso a paso.
> 
> 5. **Estrategia Algorítmica Propuesta:**
>    - Justificación técnica del uso de estructuras de datos optimizadas en Python (`heapq` con eliminación perezosa / Lazy Deletion, diccionarios de estado `dict`).
>    - Complejidad esperada de tiempo $O(Q \log Q)$ y memoria $O(Q)$.
> 
> 6. **Flujo de Trabajo en Git y Próximos Pasos:**
>    - Registro de comandos Git (`git add`, `git commit`, `git push`).
>    - Estado de las entregas y tareas pendientes antes de la finalización del código definitivo.
> 
> **Requisito de formato:** Genera directamente el contenido completo en Markdown profesional con tablas, listas de verificación (checklists) y bloques de código.