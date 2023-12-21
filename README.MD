# ERP AGROFLORI

Sistema de gestión para el bioparque Agroflori. Actualmente solo cuenta con el módulo de finanzas, pero a futuro se planea implementar el módulo de gestión de animales y de recursos humanos.

Este proyecto se ejecuta de manera local.

**Versión:** 1.0

## Uso

- Descargar el repositorio y correr `pip install -r ./requirements.txt` para instalar todas las dependencias necesarias.
- Crear una base de datos llamada "agroflori".
- Instalar el servidor PostgreSQL y la interfaz gráfica pgAdmin.
- A la altura del archivo "settings.py", correr el comando `python manage.py make migrations`.
- A la altura del archivo "settings.py", correr el comando `python manage.py migrate`.
- A la altura del archivo "settings.py", correr el comando `python manage.py runserver`.
- Abrir la URL en un navegador.

## Créditos

- [@giulianad](https://github.com/GiulianaD)
- [@lauradelgadillo](https://github.com/lauradelgadillo)
- [@selwav](https://github.com/selwav)
