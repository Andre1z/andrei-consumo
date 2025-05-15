# Andrei | Consumo

Descripción:
------------
andrei-consumo es una aplicación en Python diseñada para medir el consumo energético
de programas informáticos de forma simulada. La aplicación monitorea todos los procesos
en ejecución en el sistema Windows y calcula el consumo energético estimado en megavatios-hora (MWh)
utilizando un factor de simulación (por defecto, 1.3889e-8 MWh/seg, equivalente a 50 Joules/seg).

Nota: Se utiliza una simulación para estimar el consumo energético, ya que la medición 
real mediante hardware (por ejemplo, a través de pyRAPL) no es compatible en Windows sin 
herramientas adicionales.

Características:
----------------
- Detecta y monitorea automáticamente todas las aplicaciones (procesos) en ejecución.
- Inicia para cada proceso un monitor simulado que calcula el consumo en MWh basado en el 
  tiempo transcurrido.
- Permite visualizar el consumo individual de cada proceso, así como el consumo total acumulado.
- El monitoreo se detiene al pulsar cualquier tecla, mostrando un resumen final de los consumos.

Estructura del Proyecto:
------------------------
```
andrei-consumo/
│
├── README.md
├── main
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   ├── config.cpython-313.pyc
│   │   ├── energy_monitor.cpython-313.pyc
│   │   ├── process_detector.cpython-313.pyc
│   │   └── process_runner.cpython-313.pyc
│   ├── config.py
│   ├── energy_monitor.py
│   ├── process_detector.py
│   └── process_runner.py
└── setup.py
```
Instalación:
-------------
1. Clona el repositorio:
     git clone https://github.com/Andre1z/andrei-consumo
2. Accede al directorio del proyecto:
     cd andrei-consumo
3. (Opcional) Crea y activa un entorno virtual:
     python -m venv venv
     En Windows:
         venv\Scripts\activate

Uso:
----
Para iniciar el monitoreo de procesos y ver el consumo energético:
1. Desde el directorio raíz del proyecto, ejecuta:
     python -m main.process_detector
2. El script iniciará el monitoreo de todos los procesos en ejecución, mostrando 
   de forma periódica el consumo individual y el total en la consola.
3. Para detener el monitoreo, simplemente pulsa cualquier tecla. En ese instante se 
   registrarán los consumos finales y se mostrará un resumen completo.

Personalización:
----------------
- Puedes modificar el parámetro `consumption_rate` en el archivo andrei_consumo/energy_monitor.py 
  para ajustar la tasa de simulación (MWh/seg).
- Otros parámetros de configuración se encuentran en andrei_consumo/config.py.

Compatibilidad:
---------------
- Requiere Python 3.6 o superior.
- Optimizado para Windows 11. En sistemas Linux/Unix se puede integrar la medición real con pyRAPL (requiere ajustes).

Licencia:
---------
Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

Autor:
------
Andrei Buga

Contacto:
---------
Para sugerencias, dudas o reportar errores, envía un correo a: bugaandrei1@gmail.com

---------------------------------------------------------