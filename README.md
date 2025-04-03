# Proyecto FastAPI en Python

Este proyecto utiliza **FastAPI**, un framework moderno, rápido y asíncrono para construir aplicaciones web y API con Python.

## Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes programas:

- Python 3.7 o superior
- pip (incluido con Python)
- Git (opcional, para clonar el repositorio)

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto:

1. **Clona el repositorio** (o descarga el código):

    ```bash
    git clone https://github.com/Fernanda-Marcano/api_todo.git
    ```

2. **Crea un entorno virtual** (recomendado):

    ```bash
    python -m venv env
    ```

3. **Activa el entorno virtual**:

    - En Windows:
      ```bash
      .\env\Scripts\activate
      ```
    - En macOS/Linux:
      ```bash
      source env/bin/activate
      ```

4. **Instala las dependencias** listadas en `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

5. **Ejecuta el servidor FastAPI**:

    ```bash
    uvicorn src.main:app --reload
    ```

    Asegúrate de que el archivo principal se llama `main.py` y contiene tu instancia de `FastAPI`.

6. **Accede a la aplicación**:

    Una vez ejecutado el servidor, abre tu navegador y accede a:
    [http://127.0.0.1:8000](http://127.0.0.1:8000)

    La documentación interactiva estará disponible en:
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


