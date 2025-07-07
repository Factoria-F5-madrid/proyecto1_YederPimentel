# gui/main_gui.py
import tkinter as tk
from tkinter import messagebox
import os
import sys
import time

# Ajustar path para importar desde la raíz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth.auth import register, login, verify_token
from TaximetroCLI.taximetro import Taximetro
from GUI.main_window import TaximetroApp  # importa tu GUI principal

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Taxímetro")
        self.root.geometry("300x250")

        tk.Label(root, text="Usuario").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Contraseña").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Login", command=self.login).pack(pady=5)
        tk.Button(root, text="Registrar", command=self.register).pack()

    def login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        success, token = login(user, pwd)
        if success:
            self.root.destroy()
            MainApp(user, token)
        else:
            messagebox.showerror("Error", token)

    def register(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        success, msg = register(user, pwd)
        if success:
            messagebox.showinfo("Registrado", msg)
        else:
            messagebox.showerror("Error", msg)

class MainApp:
    def __init__(self, username, token):
        self.username = username
        self.token = token
        self.taximetro = Taximetro()

        self.root = tk.Tk()
        self.root.title("Taxímetro")
        self.root.geometry("400x400")

        self.info_label = tk.Label(self.root, text=f"Usuario: {username}")
        self.info_label.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Estado: Inactivo")
        self.status_label.pack(pady=5)

        self.tarifa_label = tk.Label(self.root, text="Tarifas:")
        self.tarifa_label.pack(pady=5)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        tk.Button(self.control_frame, text="Iniciar", command=self.iniciar).grid(row=0, column=0, padx=5)
        tk.Button(self.control_frame, text="Detener", command=self.detener).grid(row=0, column=1, padx=5)
        tk.Button(self.control_frame, text="Mover", command=self.mover).grid(row=0, column=2, padx=5)
        tk.Button(self.control_frame, text="Finalizar", command=self.finalizar).grid(row=0, column=3, padx=5)

        self.output_text = tk.Text(self.root, height=10, width=45)
        self.output_text.pack(pady=10)

        self.estado = None
        self.trip_active = False
        self.start_time = 0
        self.stop_time = 0
        self.moving_time = 0
        self.state_start_time = 0

        self.root.mainloop()

    def iniciar(self):
        self.trip_active = True
        self.stop_time = 0
        self.moving_time = 0
        self.estado = "stop"
        self.state_start_time = time.time()
        self.status_label.config(text="Estado: Detenido")
        self.output("🚕 Viaje iniciado.")

    def detener(self):
        self._update_tiempo()
        self.estado = "stop"
        self.state_start_time = time.time()
        self.status_label.config(text="Estado: Detenido")
        self.output("🛑 Taxi detenido.")

    def mover(self):
        self._update_tiempo()
        self.estado = "moving"
        self.state_start_time = time.time()
        self.status_label.config(text="Estado: En movimiento")
        self.output("🏁 Taxi en movimiento.")

    def finalizar(self):
        self._update_tiempo()
        stop_rate, moving_rate, razones, multi = self.taximetro.apply_multipliers(*self.taximetro.get_time_based_rates()[:2])
        suitcase_price = 2.0
        suitcase_count = 1

        total = self.taximetro.calculate_fare(self.stop_time, self.moving_time, stop_rate, moving_rate, suitcase_price, suitcase_count)
        self.taximetro.history_trips(self.stop_time, self.moving_time, suitcase_count, total)
        self.taximetro.print_ticket(self.stop_time, self.moving_time, suitcase_count, total)

        self.output(f"✅ Viaje finalizado.\nTotal: {total:.2f} €")
        self.status_label.config(text="Estado: Finalizado")
        self.trip_active = False

    def _update_tiempo(self):
        if not self.trip_active: return
        duracion = time.time() - self.state_start_time
        if self.estado == "stop":
            self.stop_time += duracion
        elif self.estado == "moving":
            self.moving_time += duracion

    def output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


