import sys
import os

# Ajustar path para imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from auth.auth import login, register
from TaximetroCLI.taximetro import Taximetro  # Importar el taxímetro CLI

def main():
    print("🚕 Bienvenido al Taxímetro CLI con Autenticación")

    username = ""
    while True:
        choice = input("¿Quieres (r)egistrarte o (l)ogearte? (r/l): ").strip().lower()
        if choice == "r":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            success, msg = register(username, password)
            print(msg)
            if success:
                print("Ahora inicia sesión.")
        elif choice == "l":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            success, result = login(username, password)
            if success:
                print(f"✅ Login correcto, ¡bienvenido {username}!\n")
                break
            else:
                print(result)
        else:
            print("Opción no válida. Elige 'r' o 'l'.")

    # ✅ Ejecutar el taxímetro CLI
    taximetro = Taximetro()
    taximetro.run()

if __name__ == "__main__":
    main()
