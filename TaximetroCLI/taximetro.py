# taximetro
import time

def calculate_fare(second_stopped, second_moving, stop_rate, moving_rate , suitcase , suitcaseCount):
    suitCaseFare = suitcaseCount * suitcase
    fare = second_stopped * stop_rate + second_moving * moving_rate + suitCaseFare
    return fare

def taximeter():

    print("🚕 Bienvenido al Taxímetro CLI")
    print("Este programa calcula el coste de un trayecto en taxi.")

    # Configuración de tarifas personalizadas
    while True:
        try:
            stop_rate = float(input('Ingrese el precio por segundo detenido (ej. 0.02): '))
            moving_rate = float(input('Ingrese el precio por segundo en movimiento (ej. 0.05): '))
            suitcase = float(input('Ingrese el precio por suitcase (ej. 2): '))
            suitcaseCount = float(input('Ingrese cuantas maletas llevará): '))
            break
        except ValueError:
            print("Por favor, ingrese un número válido.")

    print("Comandos : start, stop, moving , finish, exit")

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
            print(state_start_time)
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
            print(f"estado a cambiado: {state}")
        
        elif command == "finish":
            if not trip_active:
                print("error: el viaje finalizado.")
                continue

            duration = time.time()- start_time
            
            if state == "stop":
                stop_time += duration
            else: 
                moving_time += duration
            
            total_fare = calculate_fare(stop_time, moving_time, stop_rate, moving_rate, suitcase, suitcaseCount)

            print(f"tiempo detenido : {stop_time : .1f}")
            print(f"tiempo en movimiento : {moving_time : .1f}")
            print(f"maletas cargadas : {suitcaseCount}")
            print(f"precio total : {total_fare : .1f}")
            
            trip_active = False
            state = None
        
        elif command == "exit":
            print("Gracias por usar el taximetro")
            break


# if __name__ == "__main__":
#     taximeter()
            