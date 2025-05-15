#!/usr/bin/env python
"""
process_detector.py – Monitoreo global de procesos con medición simulada de consumo energético (en MWh)

Este script detecta automáticamente todas las aplicaciones (procesos) en ejecución,
iniciando para cada una un monitor simulado (usando EnergyMonitor) que calcula el consumo
acumulado según el tiempo transcurrido. Se muestra de forma continua el consumo individual
de cada proceso activo y el total de todas las aplicaciones monitoreadas.
"""

import time
import psutil
import logging

# Intentamos primero la importación relativa; si falla, usamos la absoluta.
try:
    from .energy_monitor import EnergyMonitor
except ImportError:
    from energy_monitor import EnergyMonitor
    # Ajusta la ruta de importación según la estructura de tu proyecto.

def monitor_all_processes(polling_interval=1):
    """
    Detecta y monitorea de forma continua todas las aplicaciones (procesos) en ejecución,
    calculando el consumo simulado individual (en MWh) para cada uno y mostrando el total.
    """
    logger = logging.getLogger("ProcessDetector")
    logger.info("Iniciando monitoreo de procesos...")

    # Diccionario para los procesos en ejecución: key = PID, value = dict con {process, monitor}
    monitored = {}
    # Historial de procesos finalizados: key = PID, value = dict con {process, energy}
    finished = {}

    try:
        while True:
            # --- Paso 1: Obtener procesos actuales ---
            current_pids = set()
            for proc in psutil.process_iter(attrs=["pid", "name"]):
                try:
                    current_pids.add(proc.pid)
                    # Si un proceso nuevo no está siendo monitoreado, iniciar un monitor simulado
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
            for pid, data in monitored.items():
                proc = data["process"]
                monitor = data["monitor"]
                # Si el proceso ya no está en ejecución, detenemos su monitor
                if not proc.is_running():
                    monitor.stop()
                    energy = monitor.get_energy()
                    finished[pid] = {
                        "process": proc,
                        "energy": energy
                    }
                    finished_pids.append(pid)
                    logger.info(f"Proceso finalizado: {proc.info['name']} (PID {pid}). Energía registrada: {energy:.10f} MWh.")

            # Remover del diccionario aquellos procesos que han finalizado
            for pid in finished_pids:
                del monitored[pid]

            # --- Paso 3: Calcular consumo actual de procesos activos ---
            total_active_consumption = 0.0
            active_details = []
            current_time = time.time()
            for pid, data in monitored.items():
                monitor = data["monitor"]
                # Para procesos activos, se calcula la energía simulada en base al tiempo actual:
                # consumo = (current_time - start_time) * consumption_rate
                consumption = (current_time - monitor.start_time) * monitor.consumption_rate
                total_active_consumption += consumption
                # Se extrae el nombre del proceso
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

            # Mostrar historial de procesos que finalizaron (opcional)
            if finished:
                print("\nHistorial de procesos finalizados:")
                for pid, data in finished.items():
                    name = data["process"].info.get("name", "Desconocido")
                    energy = data["energy"]
                    print(f"  {name} (PID {pid}): {energy:.10f} MWh")
            print("--------------------------\n")

            time.sleep(polling_interval)

    except KeyboardInterrupt:
        logger.info("Monitoreo interrumpido por el usuario.")
        print("Monitoreo finalizado.")


if __name__ == "__main__":
    # Configuración básica del logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Iniciar el monitoreo global de procesos
    monitor_all_processes(polling_interval=1)