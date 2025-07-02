import time

def calculate_fare(second_stopped, second_moving, stop_rate, moving_rate, suitcase, suitcaseCount):
    suitCaseFare = suitcaseCount * suitcase
    fare = second_stopped * stop_rate + second_moving * moving_rate + suitCaseFare
    return fare

def taximeter():
    print("🚕 Bienvenido al Taxímetro CLI")
    print("Este programa calcula el coste de un trayecto en taxi.")

    while True:  # Bucle principal para múltiples trayectos

        # Configuración de tarifas personalizadas
        while True:
            try:
                stop_rate = float(input('Ingrese el precio por segundo detenido (ej. 0.02): '))
                moving_rate = float(input('Ingrese el precio por segundo en movimiento (ej. 0.05): '))
                suitcase = float(input('Ingrese el precio por maleta (ej. 2): '))
                suitcaseCount = float(input('Ingrese cuántas maletas llevará: '))
                break
            except ValueError:
                print("Por favor, ingrese un número válido.")

        print("Comandos: start, stop, moving, finish, exit")

        trip_active = False
        start_time = 0
        stop_time = 0
        moving_time = 0
        state = None
        state_start_time = 0

        while True:
            command = input("> ").strip().lower()

            if command == "start":
                if trip_active:
                    print("Error: el viaje ya ha iniciado.")
                    continue

                trip_active = True
                start_time = time.time()
                stop_time = 0
                moving_time = 0
                state = "stop"
                state_start_time = time.time()
                print("Viaje iniciado.")

            elif command in ["stop", "moving"]:
                if not trip_active: 
                    print("Error: el viaje no ha iniciado.")
                    continue

                duration = time.time() - state_start_time

                if state == "stop": 
                    stop_time += duration
                else:
                    moving_time += duration
                
                state = "stop" if command == "stop" else "moving"
                state_start_time = time.time()
                print(f"Estado cambiado a: {state}")

            elif command == "finish":
                if not trip_active:
                    print("Error: el viaje no ha iniciado.")
                    continue

                # Calcular último tramo
                duration = time.time() - state_start_time
                if state == "stop":
                    stop_time += duration
                else:
                    moving_time += duration

                # Calcular tarifa total
                total_fare = calculate_fare(stop_time, moving_time, stop_rate, moving_rate, suitcase, suitcaseCount)

                print(f"Tiempo detenido: {stop_time:.1f} s")
                print(f"Tiempo en movimiento: {moving_time:.1f} s")
                print(f"Maletas cargadas: {suitcaseCount}")
                print(f"Precio total: {total_fare:.2f} €")

                trip_active = False
                state = None

                # Preguntar si quiere otro viaje
                while True:
                    respuesta = input("¿Deseas iniciar un nuevo trayecto? (s/n): ").strip().lower()
                    if respuesta == "s":
                        break  # rompe solo el bucle del trayecto actual
                    elif respuesta == "n":
                        print("Gracias por usar el taxímetro.")
                        return
                    else:
                        print("Opción no válida. Escribe 's' o 'n'.")
                break  # reinicia desde el principio

            elif command == "exit":
                if trip_active:
                    # Calcular hasta ahora antes de salir
                    duration = time.time() - state_start_time
                    if state == "stop":
                        stop_time += duration
                    else:
                        moving_time += duration

                    total_fare = calculate_fare(stop_time, moving_time, stop_rate, moving_rate, suitcase, suitcaseCount)

                    print(f"Tiempo detenido: {stop_time:.1f} s")
                    print(f"Tiempo en movimiento: {moving_time:.1f} s")
                    print(f"Maletas cargadas: {suitcaseCount}")
                    print(f"Precio total: {total_fare:.2f} €")

                print("Gracias por usar el taxímetro.")
                return  # salir del programa completamente

# if __name__ == "__main__":
#     taximeter()
