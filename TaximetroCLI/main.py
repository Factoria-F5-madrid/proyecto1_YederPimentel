import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from auth.auth import login, register, verify_token
from taximetro import Taximetro

def main():
    print("🚕 Bienvenido al Taxímetro con Autenticación")

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
                print("✅ Login correcto!")
                print(f"Tu token es: {result}")  # opcional, para debug
                # Aquí podrías verificar el token o guardarlo si quieres
                break
            else:
                print(result)
        else:
            print("Opción no válida. Elige 'r' o 'l'.")

    # Si llegamos aquí, el usuario está autenticado:
    app = Taximetro()
    app.run()

if __name__ == "__main__":
    main()
