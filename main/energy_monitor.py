"""
energy_monitor.py – Módulo para medir el consumo energético
============================================================

Este módulo contiene la clase EnergyMonitor que permite iniciar, detener
y obtener el consumo energético de un proceso o bloque de código. Se utiliza
si es posible la biblioteca pyRAPL; de lo contrario, se realiza una medición simulada.
"""

import time
import logging

# Intentamos importar pyRAPL para mediciones reales de energía.
# Si no está instalado, se utilizará un método simulado.
try:
    import pyRAPL
except ImportError:
    pyRAPL = None
    logging.warning("pyRAPL no está instalado. Se utilizará medición simulada.")

class EnergyMonitor:
    """
    Clase para medir el consumo energético de un proceso o fragmento de código.

    Si se dispone de pyRAPL, se utilizará para medir consumos reales mediante el
    acceso al hardware; en caso contrario, se realizará una simulación basada en el tiempo
    transcurrido, asumiendo un consumo ficticio de 50 Joules/seg.

    Ejemplo de uso tradicional:
        monitor = EnergyMonitor(label="TestMonitor")
        monitor.start()
        # ... ejecutar proceso costoso ...
        monitor.stop()
        energy = monitor.get_energy()

    Ejemplo de uso con contexto:
        with EnergyMonitor(label="ContextMonitor") as mon:
            # ... ejecutar proceso costoso ...
        energy = mon.get_energy()
    """

    def __init__(self, label="default", use_pyrapl=True):
        """
        Inicializa el monitor energético.

        Parámetros:
            label (str): Identificador para la medición.
            use_pyrapl (bool): Indica si se quiere utilizar pyRAPL en caso de estar disponible.
        """
        self.label = label
        self.use_pyrapl = use_pyrapl and (pyRAPL is not None)
        self.logger = logging.getLogger("andrei_consumo.EnergyMonitor")
        self.measurement = None  # Se asignará el objeto de medición pyRAPL
        self.start_time = None   # Para medición simulada: tiempo de inicio
        self.end_time = None     # Para medición simulada: tiempo de finalización

        if self.use_pyrapl:
            try:
                pyRAPL.setup()
                self.logger.info("pyRAPL configurado correctamente.")
            except Exception as e:
                self.logger.error(f"Error al configurar pyRAPL: {e}")
                self.use_pyrapl = False

    def start(self):
        """
        Inicia la medición del consumo energético.
        """
        if self.use_pyrapl:
            # Se crea un objeto Measurement de pyRAPL con la etiqueta proporcionada.
            self.measurement = pyRAPL.Measurement(self.label)
            self.measurement.begin()
            self.logger.info(f"Medición iniciada (pyRAPL) para '{self.label}'.")
        else:
            # Se utiliza la hora actual para marcar el inicio de la medición simulada.
            self.start_time = time.time()
            self.logger.info(f"Medición simulada iniciada para '{self.label}'.")

    def stop(self):
        """
        Finaliza la medición del consumo energético.
        """
        if self.use_pyrapl:
            if self.measurement:
                self.measurement.end()
                self.logger.info(f"Medición finalizada (pyRAPL) para '{self.label}'.")
            else:
                self.logger.warning("No se inició una medición pyRAPL para detener.")
        else:
            if self.start_time:
                self.end_time = time.time()
                self.logger.info(f"Medición simulada finalizada para '{self.label}'.")
            else:
                self.logger.warning("No se inició una medición simulada para detener.")

    def get_energy(self):
        """
        Retorna el consumo energético medido.

        - Para pyRAPL: devuelve el valor medido (se asume que el objeto measurement
          posee un atributo 'result.energy' con la energía en Joules).
        - Para la simulación: calcula un valor estimado basado en el tiempo transcurrido
          (consumo estimado = tiempo * 50 Joules/seg).

        Retorna:
            float o None: Consumo de energía en Joules, o None si no se completó la medición.
        """
        if self.use_pyrapl:
            if self.measurement:
                try:
                    # Se espera que pyRAPL asigne en measurement.result el valor medido.
                    energy_value = self.measurement.result.energy
                    self.logger.info(f"Consumo energético medido: {energy_value} Joules.")
                    return energy_value
                except AttributeError:
                    self.logger.error("El objeto pyRAPL no posee el atributo 'result.energy'.")
                    return None
            else:
                self.logger.warning("Medición pyRAPL no se inició o finalizó correctamente.")
                return None
        else:
            if self.start_time and self.end_time:
                elapsed_time = self.end_time - self.start_time
                simulated_energy = elapsed_time * 50  # Valor simulado: 50 Joules por segundo
                self.logger.info(f"Consumo energético simulado: {simulated_energy:.2f} Joules.")
                return simulated_energy
            else:
                self.logger.warning("La medición simulada no se completó correctamente (faltan start_time o end_time).")
                return None

    def __enter__(self):
        """
        Permite utilizar la clase en un bloque 'with'.

        Ejemplo:
            with EnergyMonitor(label="ContextMonitor") as mon:
                # código a medir
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Finaliza la medición cuando se sale del contexto 'with'.

        No suprime excepciones, por lo que cualquier error se propagará.
        """
        self.stop()
        return False  # Permite que cualquier excepción se propague sin ser suprimida.

# Bloque de prueba para ejecución directa del módulo.
if __name__ == "__main__":
    # Configuración básica de logging para visualizar mensajes en consola.
    logging.basicConfig(level=logging.INFO)

    # Ejemplo 1: Uso tradicional (start/stop)
    monitor = EnergyMonitor(label="TestMonitor")
    monitor.start()
    # Simulamos una operación costosa
    time.sleep(2)
    monitor.stop()
    energy = monitor.get_energy()
    print(f"Consumo energético medido (método directo): {energy} Joules")

    # Ejemplo 2: Uso mediante bloque 'with'
    with EnergyMonitor(label="ContextMonitor") as em:
        time.sleep(1)
    print(f"Consumo energético medido (context): {em.get_energy()} Joules")