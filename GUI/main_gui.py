# gui/main_gui.py
import tkinter as tk
from tkinter import messagebox
import os
import sys

# Ajustar el path para importar desde la raíz del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.auth import register, login
from GUI.main_window import TaximetroApp


class LoginWindow(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success

        self.master.title("Login - Taxímetro")
        self.master.geometry("300x250")

        tk.Label(self, text="Usuario").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Contraseña").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.handle_login).pack(pady=5)
        tk.Button(self, text="Registrar", command=self.handle_register).pack()

        self.pack()

    def handle_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        success, token = login(user, pwd)
        if success:
            self.on_login_success(user, token)
        else:
            messagebox.showerror("Error", token)

    def handle_register(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        success, msg = register(user, pwd)
        if success:
            messagebox.showinfo("Registrado", msg)
        else:
            messagebox.showerror("Error", msg)


class GUIApp:
    def __init__(self):
        self.root = tk.Tk()
        self.show_login()

    def show_login(self):
        self.clear_window()
        LoginWindow(self.root, self.on_login_success)

    def on_login_success(self, username, token):
        self.clear_window()
        TaximetroApp(self.root, username)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GUIApp()
    app.run()
