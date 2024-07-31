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

## Carga y limpieza de datos

Lo primero que hice fue descargar los .csv y convertirlos a DF.
Al hacerlo me di cuenta que habia muchos valores nulos y columnas que no me servian para las funciones que se me pedia. Asi que desanide las columnas que para mi eran utiles (unicamente el datasets credits) quite los valores nulos y elimine las columnas que no eran necesarias. Por ultimo transfore los df a parquet para poder subirlos a FastAPI

## Funciones

Cree 4 datasets en los cuales deje unicamente las columnas que usaria para cada funcion.
El primer datasets lo utilice para las primeras 3 funciones, el segundo para la funcion 4, el tercero para la funcion 5 y el ultimo datasets que era para el ML lo tuve que recortar bastante para que funcionara dentro de render ya que se me pasaba el tamañana maximo



## Requisitos para usar FASTAPI y Render

- Python 3.7+
- FastAPI
- Uvicorn
- pandas
- scikit-learn

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/Federicoo11/PROYECTO_INDIVIDUAL_N-1
    cd PROYECTO_INDIVIDUAL_N-1
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
