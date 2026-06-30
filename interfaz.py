import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

# Importamos la lógica matemática
from logica_grafo import GrafoCiudades

class ProyectoFinalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Final - Matemática Discreta: Optimizador de Rutas")
        self.root.geometry("1100x650")
        self.root.minsize(900, 500)

        #motor del grafo
        try:
            self.motor = GrafoCiudades()
            self.G = self.motor.obtener_objeto_grafo()
            self.ciudades = self.motor.obtener_lista_ciudades()
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))
            self.root.destroy()
            return

        # Fijamos (seed=42)
        self.posiciones = nx.spring_layout(self.G, seed=42, k=0.8)

        self._construir_interfaz()
        self.dibujar_grafo()  # Dibujamos el mapa

    def _construir_interfaz(self):
        """Crea el panel izquierdo de controles y el panel derecho para el dibujo."""
        # Panel Izquierdo (Controles)
        panel_controles = tk.Frame(self.root, width=320, bg="#f0f2f5", padx=20, pady=20)
        panel_controles.pack(side="left", fill="y")
        panel_controles.pack_propagate(False)

        tk.Label(panel_controles, text="Buscador de Rutas", font=("Arial", 16, "bold"), bg="#f0f2f5", fg="#1a1a1a").pack(pady=(0, 20))

        # Selector Origen
        tk.Label(panel_controles, text="Ciudad de Origen ($s$):", font=("Arial", 10, "bold"), bg="#f0f2f5").pack(anchor="w")
        self.cb_origen = ttk.Combobox(panel_controles, values=self.ciudades, state="readonly")
        self.cb_origen.pack(fill="x", pady=(5, 15))
        self.cb_origen.set("Madrid")  # Valor por defecto

        # Selector Destino
        tk.Label(panel_controles, text="Ciudad de Destino ($t$):", font=("Arial", 10, "bold"), bg="#f0f2f5").pack(anchor="w")
        self.cb_destino = ttk.Combobox(panel_controles, values=self.ciudades, state="readonly")
        self.cb_destino.pack(fill="x", pady=(5, 20))
        self.cb_destino.set("Praga")  # Valor por defecto

        # Botón Calcular
        btn_calcular = tk.Button(
            panel_controles, text="⚡ Calcular Ruta Óptima", font=("Arial", 11, "bold"),
            bg="#0066cc", fg="white", activebackground="#004c99", activeforeground="white",
            relief="flat", cursor="hand2", pady=10, command=self.ejecutar_calculo
        )
        btn_calcular.pack(fill="x", pady=(0, 25))

        # Panel de Resultados (Costo y Secuencia)
        tk.Label(panel_controles, text="Resultados del Algoritmo:", font=("Arial", 10, "bold"), bg="#f0f2f5").pack(anchor="w")
        
        self.lbl_costo = tk.Label(panel_controles, text="Costo Total: -- km", font=("Arial", 12, "bold"), bg="#e6f2ff", fg="#004080", pady=10)
        self.lbl_costo.pack(fill="x", pady=(5, 10))

        tk.Label(panel_controles, text="Recorrido ($P^*$):", font=("Arial", 9), bg="#f0f2f5").pack(anchor="w")
        self.txt_secuencia = tk.Text(panel_controles, height=6, width=30, font=("Consolas", 10), bg="white", relief="solid", bd=1)
        self.txt_secuencia.pack(fill="x", pady=(5, 10))

        # Botón Limpiar
        btn_limpiar = tk.Button(
            panel_controles, text="🧹 Limpiar ruta", font=("Arial", 9),
            bg="#6c757d", fg="white", activebackground="#5a6268", activeforeground="white",
            relief="flat", cursor="hand2", padx=12, pady=4, command=self.limpiar_interfaz
        )
        btn_limpiar.pack(pady=(5, 0))

        #(Lienzo del Grafo)
        self.panel_mapa = tk.Frame(self.root, bg="white")
        self.panel_mapa.pack(side="right", fill="both", expand=True)

        self.figura = plt.Figure(figsize=(7, 6), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self.ax.axis("off")

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.panel_mapa)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def dibujar_grafo(self, ruta_optima=None):
        """Dibuja la red completa y superpone la ruta óptima resaltada si existe."""
        self.ax.clear()
        self.ax.axis("off")

        # 1. Dibujamos todas las aristas base en gris claro
        nx.draw_networkx_edges(self.G, self.posiciones, ax=self.ax, edge_color="#cccccc", width=1.5)

        # 2. Dibujamos todos los nodos base en azul claro
        nx.draw_networkx_nodes(self.G, self.posiciones, ax=self.ax, node_color="#99c2ff", node_size=600, edgecolors="#005ce6")

        # 3. Dibujamos las etiquetas de las ciudades
        nx.draw_networkx_labels(self.G, self.posiciones, ax=self.ax, font_size=8, font_weight="bold", font_family="sans-serif")

        # 4. Dibujamos los pesos w(u,v) (kilómetros) en cada arista base
        etiquetas_pesos = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(self.G, self.posiciones, edge_labels=etiquetas_pesos, ax=self.ax, font_size=7)

        #RESALTE DE RUTA ÓPTIMA
        if ruta_optima and len(ruta_optima) > 1:
            aristas_ruta = [(ruta_optima[i], ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]

            nx.draw_networkx_edges(self.G, self.posiciones, edgelist=aristas_ruta, ax=self.ax, edge_color="#ff3333", width=4)
            nx.draw_networkx_nodes(self.G, self.posiciones, nodelist=ruta_optima, ax=self.ax, node_color="#ff4d4d", node_size=700, edgecolors="#b30000")

        self.figura.tight_layout()
        self.canvas.draw()

    def ejecutar_calculo(self):
        """Captura los datos de la GUI, llama al algoritmo y actualiza la pantalla."""
        origen = self.cb_origen.get()
        destino = self.cb_destino.get()

        if origen == destino:
            messagebox.showwarning("Aviso", "La ciudad de origen y destino son la misma.")
            return

        try:
            ruta, costo = self.motor.calcular_ruta_optima(origen, destino)

            self.lbl_costo.config(text=f"Costo Total: {costo} km")
            
            self.txt_secuencia.delete("1.0", tk.END)
            texto_ruta = " ➔\n".join(ruta)
            self.txt_secuencia.insert(tk.END, texto_ruta)

            self.dibujar_grafo(ruta_optima=ruta)

        except Exception as e:
            messagebox.showerror("Error de Cálculo", str(e))

    def limpiar_interfaz(self):
        """Restablece los textos, selectores y devuelve el mapa a su estado gris neutro."""
        self.cb_origen.set("Madrid")
        self.cb_destino.set("Praga")
        self.lbl_costo.config(text="Costo Total: -- km")
        self.txt_secuencia.delete("1.0", tk.END)
        self.dibujar_grafo(ruta_optima=None)


if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = ProyectoFinalApp(ventana_principal)
    ventana_principal.mainloop()