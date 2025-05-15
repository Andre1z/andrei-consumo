#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# Obtenemos el directorio actual para poder leer el README
here = os.path.abspath(os.path.dirname(__file__))

# Leemos el README.md para usarlo como descripción larga del paquete
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='andrei-consumo',
    version='0.1.0',
    description='Herramienta para medir el consumo energético de aplicaciones informáticas.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Andrei',
    author_email='tu@correo.com',  # Cambia esto por tu correo de contacto
    url='https://github.com/Andre1z/andrei-consumo',  # Reemplaza con la URL de tu repositorio
    packages=find_packages(exclude=['tests*', 'docs', 'examples']),
    install_requires=[
        'pyRAPL>=1.0.0',  # Asegúrate de ajustar el requisito según la versión que necesites
        'psutil>=5.0.0'
    ],
    entry_points={
        'console_scripts': [
            'andrei-consumo=andrei_consumo.__main__:main'
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)