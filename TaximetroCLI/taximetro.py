import os
from datetime import datetime
import time
import logging


class Taximetro:
    def __init__(self):
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_dir = os.path.join(base_dir, "logs")
        self.history_dir = os.path.join(base_dir, "history")

        
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)

        logging.basicConfig(
            filename=os.path.join(self.log_dir, "taximetro.log"),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def calculate_fare(self, second_stopped, second_moving, stop_rate, moving_rate, suitcase, suitcaseCount):
        suitCaseFare = suitcaseCount * suitcase
        fare = second_stopped * stop_rate + second_moving * moving_rate + suitCaseFare
        return fare

    def history_trips(self, stop_time, moving_time, suitcaseCount, total_fare):
        with open(os.path.join(self.history_dir, "historico.txt"), "a", encoding="utf-8") as f:
            f.write("==== Nuevo Trayecto ====\n")
            f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Tiempo detenido: {stop_time:.1f} segundos\n")
            f.write(f"Tiempo en movimiento: {moving_time:.1f} segundos\n")
            f.write(f"Maletas cargadas: {suitcaseCount}\n")
            f.write(f"Precio total: {total_fare:.2f} €\n")
            f.write("========================\n\n")

    def print_ticket(self, stop_time, moving_time, suitcaseCount, total_fare):
        total_time = stop_time + moving_time
        print("\n====== RECIBO TAXÍMETRO ======")
        print(f"Tiempo detenido: {stop_time:.1f} segundos")
        print(f"Tiempo en movimiento: {moving_time:.1f} segundos")
        print(f"Maletas cargadas: {suitcaseCount}")
        print(f"Tiempo total del trayecto: {total_time:.1f} segundos")
        print(f"Precio total a pagar: {total_fare:.2f} €")
        print("==============================\n")
        logging.info("Se ha generado un recibo de viaje.")

    def get_time_based_rates(self):
        now = datetime.now().time()
        hour = now.hour

        if 7 <= hour < 9:
            return 0.025, 0.06, "Hora Punta Mañana"
        elif 17 <= hour < 19:
            return 0.025, 0.06, "Hora Punta Tarde"
        elif 22 <= hour or hour < 5:  # Desde 22:00 hasta 4:59 AM
            return 0.03, 0.07, "Nocturna"
        else:
            return 0.02, 0.04, "Normal"

    def apply_multipliers(self, stop_rate, moving_rate, lluvia=False, evento=False):
        razones = []
        multiplicador = 1.0

        if lluvia:
            multiplicador *= 1.5
            razones.append("Lluvia")
        if evento:
            multiplicador *= 2.0
            razones.append("Evento especial")

        stop_rate *= multiplicador
        moving_rate *= multiplicador

        return stop_rate, moving_rate, razones, multiplicador

    def run(self):
        print("🚕 Bienvenido al Taxímetro CLI")
        print("Este programa calcula el coste de un trayecto en taxi.")
        logging.info("Se ha iniciado el programa.")

        while True:
            # Preguntar condiciones especiales
            lluvia = input("¿Está lloviendo? (s/n): ").strip().lower() == "s"
            evento = input("¿Hay un evento especial? (s/n): ").strip().lower() == "s"

            # Obtener tarifas base y aplicar multiplicadores
            stop_rate_base, moving_rate_base, franja = self.get_time_based_rates()
            stop_rate, moving_rate, razones, multiplicador = self.apply_multipliers(stop_rate_base, moving_rate_base, lluvia, evento)

            print(f"\n💡 Tarifa automática aplicada ({franja})")
            print(f"  ➤ Precio por segundo detenido: {stop_rate:.3f} €/s")
            print(f"  ➤ Precio por segundo en movimiento: {moving_rate:.3f} €/s")
            if razones:
                print(f"  ➤ Multiplicadores por: {', '.join(razones)} → x{multiplicador:.2f}")
            print("")

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
                    logging.info(f"Estado cambiado a: {state}")

                elif command == "finish":
                    if not trip_active:
                        print("Error: el viaje no ha iniciado.")
                        continue

                    duration = time.time() - state_start_time
                    if state == "stop":
                        stop_time += duration
                    else:
                        moving_time += duration

                    total_fare = self.calculate_fare(stop_time, moving_time, stop_rate, moving_rate, suitcase, suitcaseCount)
                    self.history_trips(stop_time, moving_time, suitcaseCount, total_fare)

                    print(f"Tiempo detenido: {stop_time:.1f} s")
                    print(f"Tiempo en movimiento: {moving_time:.1f} s")
                    print(f"Maletas cargadas: {suitcaseCount}")
                    print(f"Precio total: {total_fare:.2f} €")
                    logging.info("Trayecto finalizado")

                    while True:
                        want_receipt = input("¿Deseas un recibo? (s/n): ").strip().lower()
                        if want_receipt == "s":
                            self.print_ticket(stop_time, moving_time, suitcaseCount, total_fare)
                            break
                        elif want_receipt == "n":
                            break

                    trip_active = False
                    state = None

                    while True:
                        again = input("¿Deseas iniciar un nuevo trayecto? (s/n): ").strip().lower()
                        if again == "s":
                            break
                        elif again == "n":
                            print("Gracias por usar el taxímetro.")
                            logging.info("El usuario ha salido del programa")
                            return

                elif command == "exit":
                    print("Gracias por usar el taxímetro.")
                    logging.info("El usuario ha salido del programa")
                    return
