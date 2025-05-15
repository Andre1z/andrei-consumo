"""
Andrei Consumo
==============

Este paquete ofrece herramientas para medir el consumo energético de programas informáticos.
Se incluyen clases y funciones para monitorear la energía, ejecutar procesos y manejar
configuraciones predeterminadas de medición.

Uso:
    from andrei_consumo import EnergyMonitor, run_program, DEFAULT_CONFIG

Módulos disponibles:
    - energy_monitor: contiene la clase EnergyMonitor que implementa la lógica de medición.
    - process_runner: contiene funciones para ejecutar programas y capturar sus métricas.
    - config: define parámetros y configuraciones predeterminadas para el monitoreo.
"""

__version__ = "0.1.0"

# Importación de elementos clave del paquete
from .energy_monitor import EnergyMonitor
from .process_runner import run_program  # Se espera que en process_runner definas run_program
from .config import DEFAULT_CONFIG

# Definición de la API pública del paquete
__all__ = ["EnergyMonitor", "run_program", "DEFAULT_CONFIG"]

# Configuración básica de logging para todo el paquete
import logging

logger = logging.getLogger("andrei_consumo")
if not logger.handlers:
    # Configuramos un handler para salida por consola si aún no existe
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

logger.info("Se ha inicializado el paquete andrei_consumo.")