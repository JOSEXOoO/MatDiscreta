# Optimizador de Rutas Europeas - Matemática Discreta

**Autor:** [José Manuel Mardones Escobar]
**Modalidad:** Proyecto Individual (Matematica Discreta)

## Descripción General del Problema
Este proyecto consiste en el modelamiento computacional de una red de ciudades mediante un grafo ponderado no dirigido. El objetivo principal es calcular la ruta óptima (camino mínimo) entre 15 urbes de Europa Central y Occidental. El criterio de ponderación utilizado corresponde a la distancia terrestre mínima en kilómetros por autopista, garantizando pesos estrictamente positivos. La solución implementa el Algoritmo de Dijkstra para la optimización de los trayectos.

## Librerías Utilizadas
El proyecto fue desarrollado en Python 3 utilizando las siguientes librerías:
* `networkx`: Para el modelamiento matemático del grafo y la ejecución del algoritmo de Dijkstra.
* `matplotlib`: Para la distribución espacial y renderizado visual del grafo.
* `tkinter`: (Nativa de Python) Para la construcción de la interfaz gráfica de usuario.

## Instrucciones de Ejecución

1. **Clonar el repositorio:**
   Descargue este repositorio o clónelo utilizando el comando:
   `git clone [URL-DE-TU-REPOSITORIO]`

2. **Instalar dependencias:**
   Abra una terminal en la carpeta del proyecto y ejecute:
   `pip install -r requirements.txt`

3. **Iniciar la Interfaz Gráfica:**
   Para ejecutar la aplicación, corra el archivo principal desde la terminal:
   `python interfaz.py`

4. **Uso de la Aplicación:**
   * Seleccione una ciudad de origen y una ciudad de destino en los menús desplegables.
   * Haga clic en "Calcular Ruta Óptima" para visualizar el camino en rojo sobre el mapa, junto con el costo total y la secuencia de nodos.
   * Utilice el botón "Limpiar ruta" para restablecer el mapa a su estado original antes de realizar una nueva consulta.