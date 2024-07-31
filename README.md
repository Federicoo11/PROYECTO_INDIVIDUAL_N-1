# Sistema de Recomendación de Películas

Este proyecto implementa una API para realizar análisis y recomendaciones de películas utilizando FastAPI, pandas, y scikit-learn.

## Descripción

La API proporciona varias funcionalidades, incluyendo:
- Obtener la cantidad de filmaciones por mes.
- Obtener la cantidad de filmaciones por día de la semana.
- Obtener el score (popularidad) de una película.
- Obtener la cantidad de votos y el promedio de una película.
- Obtener la información de un actor, incluyendo el retorno total y promedio por película.
- Obtener la información de un director, incluyendo el retorno total y promedio por película.
- Recomendar películas similares a una dada.



## Requisitos

- Python 3.7+
- FastAPI
- Uvicorn
- pandas
- scikit-learn

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. Crea un entorno virtual y actívalo:
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Asegúrate de tener los archivos de datos necesarios (`movies1.parquet`, `movies2.parquet`, `movies3.parquet`, `movies4.parquet`) en la carpeta `csv/`.

## Ejecución

Para ejecutar la aplicación, utiliza el siguiente comando:
```bash
uvicorn main:app --reload
