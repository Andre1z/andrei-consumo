"""
config.py – Configuración Centralizada para andrei-consumo
==========================================================

Este módulo define los parámetros predeterminados para el monitoreo
del consumo energético. Los parámetros incluyen rutas de salida, intervalos
de muestreo, tiempos máximos, entre otros. Además, se incluye una función
para actualizar la configuración con valores personalizados.
"""

import os

# Carpeta por defecto para almacenar resultados, logs u otros archivos generados.
DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), "output")

# Intervalo de muestreo en segundos: tiempo entre cada medición.
DEFAULT_SAMPLE_INTERVAL = 1.0  # 1 segundo

# Tiempo máximo de ejecución (en segundos) para el proceso a medir.
DEFAULT_MAX_EXECUTION_TIME = 3600  # 1 hora

# Método de medición a utilizar: puede ser 'pyRAPL', 'psutil', 'custom', etc.
DEFAULT_MEASUREMENT_METHOD = "pyRAPL"

# Parámetro para habilitar la generación de logs durante la medición.
DEFAULT_ENABLE_LOGGING = True

# Configuración predeterminada agrupada en un diccionario
DEFAULT_CONFIG = {
    "output_dir": DEFAULT_OUTPUT_DIR,
    "sample_interval": DEFAULT_SAMPLE_INTERVAL,
    "max_execution_time": DEFAULT_MAX_EXECUTION_TIME,
    "measurement_method": DEFAULT_MEASUREMENT_METHOD,
    "enable_logging": DEFAULT_ENABLE_LOGGING,
    # Puedes agregar aquí más parámetros específicos que necesites.
}


def update_config(custom_config: dict) -> dict:
    """
    Actualiza la configuración predeterminada con valores personalizados.

    Parámetros:
        custom_config (dict): Diccionario con claves y valores a actualizar.

    Retorna:
        dict: Configuración actualizada.
    
    Ejemplo:
        custom = {"sample_interval": 0.5, "max_execution_time": 7200}
        nueva_config = update_config(custom)
    """
    updated_config = DEFAULT_CONFIG.copy()
    updated_config.update(custom_config)
    return updated_config


if __name__ == "__main__":
    # Ejemplo de uso: muestra la configuración predeterminada y el efecto de la actualización.
    print("Configuración predeterminada:")
    for key, value in DEFAULT_CONFIG.items():
        print(f"  {key}: {value}")

    # Personalizando algunos parámetros
    custom = {
        "sample_interval": 0.5,        # Muestreo cada 0.5 segundos en lugar de 1.0
        "max_execution_time": 7200     # 2 horas en lugar de 1 hora
    }
    new_config = update_config(custom)

    print("\nConfiguración actualizada:")
    for key, value in new_config.items():
        print(f"  {key}: {value}")