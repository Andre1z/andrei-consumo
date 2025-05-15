"""
energy_monitor.py – Módulo para simular la medición del consumo energético en MWh
================================================================================

Este módulo contiene la clase EnergyMonitor que simula la medición 
del consumo energético de un proceso o fragmento de código, calculándolo 
a partir del tiempo transcurrido y un factor de consumo expresado en MWh/seg.
"""

import time
import logging

class EnergyMonitor:
    """
    Clase para simular la medición del consumo energético en MWh.

    Registra el tiempo de inicio y fin de una operación y estima el consumo
    energético multiplicando el tiempo transcurrido por un factor de consumo (MWh/seg).
    """
    def __init__(self, label="default", consumption_rate=1.3889e-8):
        """
        Inicializa el monitor simulado.
        
        Parámetros:
            label (str): Identificador para la medición.
            consumption_rate (float): Consumo simulado en MWh/segundo.
                                      Por defecto, 50 Joules/seg equivale aproximadamente a 1.3889e-8 MWh/seg.
        """
        self.label = label
        self.consumption_rate = consumption_rate
        self.logger = logging.getLogger("andrei_consumo.EnergyMonitor")
        self.start_time = None
        self.end_time = None

    def start(self):
        """
        Inicia la medición simulada registrando el tiempo de inicio.
        """
        self.start_time = time.time()
        self.logger.info(f"Medición simulada iniciada para '{self.label}'.")

    def stop(self):
        """
        Finaliza la medición simulada registrando el tiempo de finalización.
        """
        if self.start_time is None:
            self.logger.warning("No se ha iniciado una medición simulada.")
        else:
            self.end_time = time.time()
            self.logger.info(f"Medición simulada finalizada para '{self.label}'.")

    def get_energy(self):
        """
        Calcula y retorna el consumo energético simulado en MWh.
        
        Retorna:
            float o None: Consumo estimado en MWh o None si la medición es incompleta.
        """
        if self.start_time is None or self.end_time is None:
            self.logger.warning("La medición simulada no se completó correctamente (falta start_time o end_time).")
            return None
        
        elapsed_time = self.end_time - self.start_time  # tiempo en segundos
        simulated_energy = elapsed_time * self.consumption_rate
        self.logger.info(f"Consumo energético simulado: {simulated_energy:.10f} MWh.")
        return simulated_energy

    def __enter__(self):
        """
        Permite utilizar el monitor en un contexto 'with'. Inicia la medición.
        
        Ejemplo:
            with EnergyMonitor(label="TestMonitor") as mon:
                # código a medir
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Finaliza la medición al salir del bloque 'with'.
        """
        self.stop()
        return False  # Permite que las excepciones se propaguen

if __name__ == "__main__":
    # Configuración básica de logging para ver mensajes en consola.
    logging.basicConfig(level=logging.INFO)
    
    # Ejemplo 1: Uso mediante start() y stop()
    monitor = EnergyMonitor(label="TestSimulado")
    monitor.start()
    # Simula una operación costosa durante 2 segundos
    time.sleep(2)
    monitor.stop()
    energy_mwh = monitor.get_energy()
    print(f"Energía consumida (simulada): {energy_mwh:.10f} MWh")
    
    # Ejemplo 2: Uso con el contexto 'with'
    with EnergyMonitor(label="ContextSimulado") as mon:
        time.sleep(1)
    print(f"Energía consumida con 'with': {mon.get_energy():.10f} MWh")