import time
import logging

#Empezamos con la configuracion del sistema de logs

logging.basicConfig(
    filename="../logs/taximetro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def calculate_fare(second_stopped, second_moving, stop_rate, moving_rate, suitcase, suitcaseCount):
    suitCaseFare = suitcaseCount * suitcase
    fare = second_stopped * stop_rate + second_moving * moving_rate + suitCaseFare
    return fare

def print_ticket(stop_time, moving_time, suitcaseCount, total_fare):
    total_time = stop_time + moving_time
    print("\n====== RECIBO TAXÍMETRO ======")
    print(f"Tiempo detenido: {stop_time:.1f} segundos")
    print(f"Tiempo en movimiento: {moving_time:.1f} segundos")
    print(f"Maletas cargadas: {suitcaseCount}")
    print(f"Tiempo total del trayecto: {total_time:.1f} segundos")
    print(f"Precio total a pagar: {total_fare:.2f} €")
    print("==============================\n")
    logging.info("Se ha generado un recibo de viaje.")

def taximeter():
    print("🚕 Bienvenido al Taxímetro CLI")
    print("Este programa calcula el coste de un trayecto en taxi.")
    logging.info("Se ha iniciado el programa.")

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
                logging.error("Error de entrada en las tarifas o maletas")

        print("Comandos: start, stop, moving, finish, exit")

        trip_active = False
        start_time = 0
        stop_time = 0
        moving_time = 0
        state = None
        state_start_time = 0

        while True:
            command = input("> ").strip().lower()
            logging.info(f"Se ha introducido el comando: {command}")

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
                logging.info("Se ha iniciado un nuevo trayecto.")

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
                logging.info(f"Se ha cambiado el estado a: {state}")

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
                logging.info(f"Se ha terminado el trayecto. Tiempo detenido: {stop_time:.1f} s, Tiempo en movimiento: {moving_time:.1f} s, Maletas cargadas: {suitcaseCount}, Precio total: {total_fare:.2f} €")

                # Preguntar si quiere recibo
                while True:
                    want_receipt = input("¿Deseas un recibo? (s/n): ").strip().lower()
                    if want_receipt == "s":
                        print_ticket(stop_time, moving_time, suitcaseCount, total_fare)
                        break
                    elif want_receipt == "n":
                        break
                    else:
                        print("Por favor, responde con 's' o 'n'.")

                trip_active = False
                state = None

                # Preguntar si quiere otro viaje
                while True:
                    respuesta = input("¿Deseas iniciar un nuevo trayecto? (s/n): ").strip().lower()
                    if respuesta == "s":
                        break  # rompe solo el bucle del trayecto actual
                    elif respuesta == "n":
                        print("Gracias por usar el taxímetro.")
                        logging.info("El usuario ha salido del programa")
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
                    logging.info(f"Se ha terminado el trayecto. Tiempo detenido: {stop_time:.1f} s, Tiempo en movimiento: {moving_time:.1f} s, Maletas cargadas: {suitcaseCount}, Precio total: {total_fare:.2f} €")

                    # Preguntar si quiere recibo
                    while True:
                        want_receipt = input("¿Deseas un recibo? (s/n): ").strip().lower()
                        if want_receipt == "s":
                            print_ticket(stop_time, moving_time, suitcaseCount, total_fare)
                            break
                        elif want_receipt == "n":
                            break
                        else:
                            print("Por favor, responde con 's' o 'n'.")

                print("Gracias por usar el taxímetro.")
                logging.info("El usuario ha salido del programa")
                return  # salir del programa completamente
