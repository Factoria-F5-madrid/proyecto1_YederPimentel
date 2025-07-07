# gui/main_window.py
import tkinter as tk
import time
from tkinter import messagebox
from TaximetroCLI.taximetro import Taximetro

class TaximetroApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title(f"Taxímetro - Bienvenido {username}")
        self.username = username
        self.taximetro = Taximetro()

        self.trip_active = False
        self.stop_time = 0
        self.moving_time = 0
        self.state = None
        self.state_start_time = 0
        self.suitcase = 0
        self.suitcase_count = 0

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="💼 Precio por maleta:").grid(row=0, column=0, sticky="w")
        self.suitcase_entry = tk.Entry(self.root)
        self.suitcase_entry.grid(row=0, column=1)

        tk.Label(self.root, text="🎒 Cantidad de maletas:").grid(row=1, column=0, sticky="w")
        self.suitcase_count_entry = tk.Entry(self.root)
        self.suitcase_count_entry.grid(row=1, column=1)

        self.tarifa_label = tk.Label(self.root, text="⏳ Tarifa no calculada")
        self.tarifa_label.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(self.root, text="Calcular tarifa", command=self.mostrar_tarifas).grid(row=3, column=0, columnspan=2, pady=5)

        tk.Button(self.root, text="▶️ Iniciar viaje", command=self.iniciar_viaje).grid(row=4, column=0)
        tk.Button(self.root, text="⏸️ Detenido", command=lambda: self.cambiar_estado("stop")).grid(row=4, column=1)
        tk.Button(self.root, text="🚗 En movimiento", command=lambda: self.cambiar_estado("moving")).grid(row=5, column=0)
        tk.Button(self.root, text="⛔ Finalizar viaje", command=self.finalizar_viaje).grid(row=5, column=1)

    def mostrar_tarifas(self):
        try:
            self.suitcase = float(self.suitcase_entry.get())
            self.suitcase_count = int(self.suitcase_count_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Introduce valores válidos para las maletas")
            return

        stop_rate_base, moving_rate_base, franja = self.taximetro.get_time_based_rates()
        stop_rate, moving_rate, razones, multiplicador = self.taximetro.apply_multipliers(stop_rate_base, moving_rate_base)

        self.tarifa_info = (stop_rate, moving_rate)
        texto = f"Tarifa: {franja} - Detenido: {stop_rate:.3f} €/s - En movimiento: {moving_rate:.3f} €/s"
        if razones:
            texto += f" (Multiplicadores: {', '.join(razones)} x{multiplicador:.2f})"
        self.tarifa_label.config(text=texto)

    def iniciar_viaje(self):
        if self.trip_active:
            messagebox.showinfo("Error", "El viaje ya está activo")
            return

        self.trip_active = True
        self.stop_time = 0
        self.moving_time = 0
        self.state = "stop"
        self.state_start_time = time.time()
        messagebox.showinfo("Inicio", "Viaje iniciado")

    def cambiar_estado(self, nuevo_estado):
        if not self.trip_active:
            messagebox.showwarning("Advertencia", "Primero inicia el viaje")
            return

        duracion = time.time() - self.state_start_time
        if self.state == "stop":
            self.stop_time += duracion
        else:
            self.moving_time += duracion

        self.state = nuevo_estado
        self.state_start_time = time.time()
        messagebox.showinfo("Estado", f"Estado cambiado a: {nuevo_estado}")

    def finalizar_viaje(self):
        if not self.trip_active:
            messagebox.showinfo("Error", "El viaje no ha iniciado")
            return

        duracion = time.time() - self.state_start_time
        if self.state == "stop":
            self.stop_time += duracion
        else:
            self.moving_time += duracion

        stop_rate, moving_rate = self.tarifa_info
        total = self.taximetro.calculate_fare(self.stop_time, self.moving_time, stop_rate, moving_rate, self.suitcase, self.suitcase_count)
        self.taximetro.history_trips(self.stop_time, self.moving_time, self.suitcase_count, total)

        recibo = (
            f"Detenido: {self.stop_time:.1f}s\n"
            f"En movimiento: {self.moving_time:.1f}s\n"
            f"Maletas: {self.suitcase_count}\n"
            f"Total: {total:.2f} €"
        )

        messagebox.showinfo("Recibo final", recibo)
        self.trip_active = False
        self.state = None
