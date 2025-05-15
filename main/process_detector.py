#!/usr/bin/env python
"""
process_detector.py – Monitoreo global de procesos con medición simulada de consumo energético (en MWh)

Este script detecta automáticamente todas las aplicaciones (procesos) en ejecución,
iniciando para cada una un monitor simulado (usando EnergyMonitor) que calcula el consumo
acumulado según el tiempo transcurrido. El monitoreo se detiene cuando el usuario pulsa una tecla,
tras lo cual se muestra un resumen del consumo individual y total acumulado.
"""

import time
import psutil
import logging
import msvcrt  # Para detectar pulsaciones de teclas en Windows

# Intentamos primero la importación relativa; si falla, usamos la absoluta.
try:
    from .energy_monitor import EnergyMonitor
except ImportError:
    from energy_monitor import EnergyMonitor

def monitor_all_processes(polling_interval=1):
    """
    Detecta y monitorea de forma continua todas las aplicaciones en ejecución,
    calculando el consumo simulado individual (en MWh) para cada una y mostrando el total.
    El monitoreo finaliza cuando el usuario pulsa una tecla.
    """
    logger = logging.getLogger("ProcessDetector")
    logger.info("Iniciando monitoreo de procesos...")

    # Diccionario de procesos activos: key = PID, value = dict con {process, monitor}
    monitored = {}
    # Historial de procesos finalizados: key = PID, value = dict con {process, energy}
    finished = {}

    try:
        while True:
            # --- Paso 1: Detectar procesos en ejecución ---
            for proc in psutil.process_iter(attrs=["pid", "name"]):
                try:
                    # Si el proceso aún no está siendo monitoreado, iniciamos el monitor simulado.
                    if proc.pid not in monitored:
                        monitor = EnergyMonitor(label=f"{proc.info['name']}_{proc.pid}")
                        monitor.start()
                        monitored[proc.pid] = {
                            "process": proc,
                            "monitor": monitor
                        }
                        logger.info(f"Se inicia monitoreo de: {proc.info['name']} (PID {proc.pid}).")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # --- Paso 2: Revisar procesos que han finalizado ---
            finished_pids = []
            for pid, data in list(monitored.items()):
                proc = data["process"]
                monitor = data["monitor"]
                if not proc.is_running():
                    monitor.stop()
                    energy = monitor.get_energy()
                    finished[pid] = {
                        "process": proc,
                        "energy": energy
                    }
                    finished_pids.append(pid)
                    logger.info(f"Proceso finalizado: {proc.info['name']} (PID {pid}). Energía registrada: {energy:.10f} MWh.")

            # Remover procesos que han finalizado del conjunto de monitoreo.
            for pid in finished_pids:
                del monitored[pid]

            # --- Paso 3: Calcular el consumo actual de procesos activos ---
            total_active_consumption = 0.0
            active_details = []
            current_time = time.time()
            for pid, data in monitored.items():
                monitor = data["monitor"]
                # El consumo acumulado se estima como (tiempo_actual - start_time) * consumption_rate
                consumption = (current_time - monitor.start_time) * monitor.consumption_rate
                total_active_consumption += consumption
                proc_name = data["process"].info.get("name", "Desconocido")
                active_details.append((proc_name, pid, consumption))

            # --- Paso 4: Mostrar resumen en consola ---
            print("\n--- Estado de Monitoreo ---")
            print("Procesos Activos:")
            if active_details:
                for name, pid, consumption in active_details:
                    print(f"  {name} (PID {pid}): {consumption:.10f} MWh")
            else:
                print("  No hay procesos activos en monitoreo.")
            print(f"Consumo total de procesos activos: {total_active_consumption:.10f} MWh")

            if finished:
                print("\nHistorial de procesos finalizados:")
                for pid, data in finished.items():
                    name = data["process"].info.get("name", "Desconocido")
                    energy = data["energy"]
                    print(f"  {name} (PID {pid}): {energy:.10f} MWh")
            print("--------------------------\n")

            # --- Paso 5: Verificar pulsación de tecla para detener el monitoreo ---
            if msvcrt.kbhit():
                msvcrt.getch()  # Lee y descarta la tecla pulsada.
                logger.info("Tecla detectada, finalizando monitoreo.")
                break

            time.sleep(polling_interval)

    except KeyboardInterrupt:
        logger.info("Monitoreo interrumpido por el usuario.")

    # --- Finalización: Detener todos los monitores activos ---
    for pid, data in monitored.items():
        monitor = data["monitor"]
        monitor.stop()
        energy = monitor.get_energy()
        finished[pid] = {
            "process": data["process"],
            "energy": energy
        }
        logger.info(f"Proceso finalizado: {data['process'].info.get('name', 'Desconocido')} (PID {pid}). Energía registrada: {energy:.10f} MWh.")

    # Calcular el consumo total final (suma de procesos finalizados)
    total_consumption = sum(data["energy"] for data in finished.values() if data["energy"] is not None)

    print("\n--- Resumen Final ---")
    print("Historial de procesos finalizados:")
    for pid, data in finished.items():
        name = data["process"].info.get("name", "Desconocido")
        energy = data["energy"]
        print(f"  {name} (PID {pid}): {energy:.10f} MWh")
    print(f"\nConsumo total acumulado: {total_consumption:.10f} MWh")
    print("---------------------\n")
    return total_consumption

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    print("Monitoreo de procesos iniciado.")
    print("Presione cualquier tecla para detener el monitoreo y ver el consumo total.\n")
    final_consumption = monitor_all_processes(polling_interval=1)
    print(f"Monitoreo completado. Consumo total acumulado: {final_consumption:.10f} MWh")