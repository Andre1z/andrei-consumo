"""
process_runner.py – Módulo para ejecutar programas y capturar métricas de consumo energético
=========================================================================================

Este módulo provee la función `run_program`, que permite:

- Ejecutar un comando externo (por ejemplo, un script, una aplicación, etc.).
- Medir el consumo energético durante la ejecución del comando utilizando la clase
  EnergyMonitor (se utilizará pyRAPL si está disponible o una medición simulada).
- Capturar la salida estándar (stdout) y la salida de error (stderr) del proceso.
- Retornar un diccionario con el código de salida, resultados de salida y el consumo
  energético medido.

Ejemplo de uso:
    result = run_program(["echo", "Hola desde process_runner"])
    print(result)
"""

import subprocess
import logging
from .energy_monitor import EnergyMonitor

def run_program(command, shell=False, monitor_label="ProcessRunner", timeout=None, capture_output=True, text=True, **kwargs):
    """
    Ejecuta un proceso externo y mide su consumo energético durante la ejecución.

    Parámetros:
        command (str o list): Comando o lista de argumentos para ejecutar.
        shell (bool): Indica si se debe ejecutar el comando en el shell. Por defecto es False.
        monitor_label (str): Etiqueta identificadora para la medición energética.
        timeout (float): Tiempo máximo de ejecución en segundos (opcional).
        capture_output (bool): Si True, se capturan stdout y stderr (default=True).
        text (bool): Si True, se retorna la salida como cadena en vez de bytes (default=True).
        **kwargs: Parámetros adicionales que se pasan a `subprocess.run()`.

    Retorna:
        dict: Diccionario con las siguientes claves:
            - exit_code: Código de salida del proceso.
            - stdout: Salida estándar (si se capturó).
            - stderr: Salida de error (si se capturó).
            - energy_consumed: Energía consumida durante la ejecución (en Joules).
    """
    logger = logging.getLogger("andrei_consumo.process_runner")
    logger.info(f"Ejecutando comando: {command} (shell={shell})")
    
    # Se utiliza el EnergyMonitor como context manager para garantizar que la medición se inicie y se detenga correctamente.
    with EnergyMonitor(label=monitor_label) as monitor:
        try:
            result = subprocess.run(
                command,
                shell=shell,
                timeout=timeout,
                capture_output=capture_output,
                text=text,
                **kwargs
            )
            logger.info(f"Proceso finalizado con código de salida: {result.returncode}")
        except subprocess.TimeoutExpired as te:
            logger.error(f"El proceso excedió el tiempo límite de {timeout} segundos.")
            # En caso de timeout, se captura la excepción y se asigna el valor retornado.
            result = te
        except Exception as e:
            logger.error(f"Error al ejecutar el proceso: {e}")
            raise  # Se propaga la excepción para que el usuario la maneje

    # Una vez finalizado el proceso, se obtiene el consumo energético medido.
    energy_consumed = monitor.get_energy()

    output = {
        "exit_code": result.returncode if hasattr(result, "returncode") else None,
        "stdout": result.stdout if hasattr(result, "stdout") else None,
        "stderr": result.stderr if hasattr(result, "stderr") else None,
        "energy_consumed": energy_consumed
    }

    return output

if __name__ == "__main__":
    # Configuración básica de logging para visualizar información en consola.
    logging.basicConfig(level=logging.INFO)
    
    # Ejemplo sencillo: ejecutar un comando de impresión en consola.
    command_to_run = ["echo", "Hola desde process_runner"]
    result = run_program(command_to_run)
    
    print("Resultado de la ejecución:")
    print(f"Código de salida: {result['exit_code']}")
    print(f"Salida: {result['stdout']}")
    print(f"Error: {result['stderr']}")
    print(f"Energía consumida: {result['energy_consumed']} Joules")