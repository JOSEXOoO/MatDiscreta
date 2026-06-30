import json
import networkx as nx

class GrafoCiudades:
    def __init__(self, ruta_archivo="datos_grafo.json"):
        """Inicializa el grafo cargando los vértices y aristas desde el archivo JSON."""
        self.ruta_archivo = ruta_archivo
        self.G = nx.Graph()  # Grafo no dirigido ponderado
        self._cargar_datos()

    def _cargar_datos(self):
        """Método privado para leer el JSON y poblar el grafo G."""
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                
            # Agregamos vértices (V)
            self.G.add_nodes_from(datos["ciudades"])
            
            # Agregamos aristas ponderadas (E, w)
            for conexion in datos["conexiones"]:
                self.G.add_edge(
                    conexion["origen"], 
                    conexion["destino"], 
                    weight=conexion["peso"]
                )
        except FileNotFoundError:
            raise Exception(f"Error: No se encontró el archivo {self.ruta_archivo}. Ejecuta primero el Paso 1.")

    def obtener_lista_ciudades(self):
        """Devuelve la lista alfabética de vértices (ideal para los menús desplegables de la GUI)."""
        return sorted(list(self.G.nodes))

    def calcular_ruta_optima(self, origen, destino):
        """
        Aplica el Algoritmo de Dijkstra para encontrar el camino mínimo P* y su costo C(P*).
        Retorna: (lista_de_ciudades, costo_total_km)
        """
        if origen not in self.G or destino not in self.G:
            raise ValueError("La ciudad de origen o destino no existe en el conjunto V.")

        try:
            
            ruta = nx.dijkstra_path(self.G, source=origen, target=destino, weight="weight")
            
            
            costo_total = nx.dijkstra_path_length(self.G, source=origen, target=destino, weight="weight")
            
            return ruta, int(costo_total)
            
        except nx.NetworkXNoPath:
            raise Exception(f"No existe un camino conexo entre {origen} y {destino}.")

    def obtener_objeto_grafo(self):
        """Devuelve el objeto interno de NetworkX para poder dibujarlo en la pantalla."""
        return self.G

if __name__ == "__main__":
    print("--- INICIANDO PRUEBAS DEL MOTOR DE GRAFOS ---")
    motor = GrafoCiudades()
    
    # Pruebas obligatorias
    pruebas = [
        ("Madrid", "Lyon"),       # Prueba 1: Distancia media
        ("Roma", "Ámsterdam"),    #Prueba 2: Extremo sur a extremo norte
        ("París", "París")        # Prueba 3: Caso borde (mismo nodo)
    ]
    
    for origen, destino in pruebas:
        ruta, costo = motor.calcular_ruta_optima(origen, destino)
        print(f"\nRuta óptima calculada: {origen} -> {destino}")
        print(f"Secuencia P*: {' -> '.join(ruta)}")
        print(f"Costo C(P*):  {costo} km")