import os 
from datetime import datetime
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

def history_trips(stop_time, moving_time, suitcaseCount, total_fare):
    os.makedirs("../history", exist_ok=True)
    with open("../history/historico.txt", "a", encoding="utf-8") as f:
        f.write("==== Nuevo Trayecto ====\n")
        f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Tiempo detenido: {stop_time:.1f} segundos\n")
        f.write(f"Tiempo en movimiento: {moving_time:.1f} segundos\n")
        f.write(f"Maletas cargadas: {suitcaseCount}\n")
        f.write(f"Precio total: {total_fare:.2f} €\n")
        f.write("========================\n\n")

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

def get_time_based_rates():
    now = datetime.now().time()
    hour = now.hour

    if 7 <= hour < 9:
        return 0.025, 0.06, "Hora Punta Mañana"
    elif 17 <= hour < 19:
        return 0.025, 0.06, "Hora Punta Tarde"
    elif 0 <= hour < 3:
        return 0.03, 0.07, "Nocturna"
    elif 10 <= hour < 16:
        return 0.015, 0.035, "Valle"
    else:
        return 0.02, 0.04, "Normal"

def apply_multipliers(stop_rate, moving_rate):
    multiplier = 1.0
    razones = []

    lluvia = input("¿Está lloviendo? (s/n): ").strip().lower()
    if lluvia == "s":
        multiplier *= 1.2
        razones.append("Lluvia")

    evento = input("¿Hay evento especial? (s/n): ").strip().lower()
    if evento == "s":
        multiplier *= 1.3
        razones.append("Evento")

    return stop_rate * multiplier, moving_rate * multiplier, razones, multiplier


def taximeter():
    print("🚕 Bienvenido al Taxímetro CLI")
    print("Este programa calcula el coste de un trayecto en taxi.")
    logging.info("Se ha iniciado el programa.")

    while True:
        # TARIFA AUTOMÁTICA SEGÚN LA HORA
        stop_rate_base, moving_rate_base, franja = get_time_based_rates()
        stop_rate, moving_rate, razones, multiplicador = apply_multipliers(stop_rate_base, moving_rate_base)

        print(f"\n💡 Tarifa automática aplicada ({franja})")
        print(f"  ➤ Precio por segundo detenido: {stop_rate:.3f} €/s")
        print(f"  ➤ Precio por segundo en movimiento: {moving_rate:.3f} €/s")
        if razones:
            print(f"  ➤ Multiplicadores por: {', '.join(razones)} → x{multiplicador:.2f}")
        print("")

        # MALETAS
        while True:
            try:
                suitcase = float(input('Ingrese el precio por maleta (ej. 2): '))
                suitcaseCount = float(input('Ingrese cuántas maletas llevará: '))
                break
            except ValueError:
                print("Por favor, ingrese un número válido.")
                logging.error("Error de entrada en las maletas")

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

                duration = time.time() - state_start_time
                if state == "stop":
                    stop_time += duration
                else:
                    moving_time += duration

                total_fare = calculate_fare(stop_time, moving_time, stop_rate, moving_rate, suitcase, suitcaseCount)
                history_trips(stop_time, moving_time, suitcaseCount, total_fare)

                print(f"Tiempo detenido: {stop_time:.1f} s")
                print(f"Tiempo en movimiento: {moving_time:.1f} s")
                print(f"Maletas cargadas: {suitcaseCount}")
                print(f"Precio total: {total_fare:.2f} €")
                logging.info(f"Se ha terminado el trayecto. Tiempo detenido: {stop_time:.1f} s, Tiempo en movimiento: {moving_time:.1f} s, Maletas: {suitcaseCount}, Precio: {total_fare:.2f} €")

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

                while True:
                    respuesta = input("¿Deseas iniciar un nuevo trayecto? (s/n): ").strip().lower()
                    if respuesta == "s":
                        break
                    elif respuesta == "n":
                        print("Gracias por usar el taxímetro.")
                        logging.info("El usuario ha salido del programa")
                        return
                    else:
                        print("Opción no válida. Escribe 's' o 'n'.")
                break

            elif command == "exit":
                if trip_active:
                    duration = time.time() - state_start_time
                    if state == "stop":
                        stop_time += duration
                    else:
                        moving_time += duration

                    total_fare = calculate_fare(stop_time, moving_time, stop_rate, moving_rate, suitcase, suitcaseCount)
                    history_trips(stop_time, moving_time, suitcaseCount, total_fare)

                    print(f"Tiempo detenido: {stop_time:.1f} s")
                    print(f"Tiempo en movimiento: {moving_time:.1f} s")
                    print(f"Maletas cargadas: {suitcaseCount}")
                    print(f"Precio total: {total_fare:.2f} €")
                    logging.info(f"Se ha terminado el trayecto. Tiempo detenido: {stop_time:.1f} s, Tiempo en movimiento: {moving_time:.1f} s, Maletas: {suitcaseCount}, Precio: {total_fare:.2f} €")

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
                return