from fastapi import FastAPI
import pandas as pd
import calendar
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Cargar los csv
df_movies1 = pd.read_parquet("csv/movies1.parquet")
df_movies2 = pd.read_parquet("csv/movies2.parquet")
df_movies3 = pd.read_parquet("csv/movies3.parquet")
df_movies3 = pd.read_parquet("csv/movies4.parquet")

def cantidad_filmaciones_mes(mes, df_movies1):
    meses_espanol_ingles = {
        "enero": "January",
        "febrero": "February",
        "marzo": "March",
        "abril": "April",
        "mayo": "May",
        "junio": "June",
        "julio": "July",
        "agosto": "August",
        "septiembre": "September",
        "octubre": "October",
        "noviembre": "November",
        "diciembre": "December"
    }
    
    mes_ingles = meses_espanol_ingles.get(mes.lower())
    
    if not mes_ingles:
        return f"Mes {mes} no es válido. Por favor ingresa un mes en español."

    df_movies1['release_date'] = pd.to_datetime(df_movies1['release_date'], errors='coerce')
    df_filtered = df_movies1[df_movies1['release_date'].dt.month == list(calendar.month_name).index(mes_ingles)]
    cantidad = df_filtered.shape[0]
    
    return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"

@app.post("/cantidad_filmaciones_mes/")
def get_cantidad_filmaciones_mes(mes: str):
    result = cantidad_filmaciones_mes(mes, df_movies1)
    return {"mensaje": result}


def cantidad_filmaciones_dia(dia, df_movies1):
    dias_espanol_num = {
        "lunes": 0,
        "martes": 1,
        "miércoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sábado": 5,
        "domingo": 6
    }
    
    dia_num = dias_espanol_num.get(dia.lower())
    
    if dia_num is None:
        return f"Día {dia} no es válido. Por favor ingresa un día en español."
    
    df_movies1['release_date'] = pd.to_datetime(df_movies1['release_date'], errors='coerce')
    df_filtered = df_movies1[df_movies1['release_date'].dt.dayofweek == dia_num]
    cantidad = df_filtered.shape[0]
    
    return f"{cantidad} cantidad de películas fueron estrenadas en los días {dia}"

@app.post("/cantidad_filmaciones_dia/")
def get_cantidad_filmaciones_dia(dia: str):
    result = cantidad_filmaciones_dia(dia, df_movies1)
    return {"mensaje": result}


def score_titulo(titulo_de_la_filmacion, df):
    filmacion = df[df['title'].str.lower() == titulo_de_la_filmacion.lower()]

    if filmacion.empty:
        return f"No se encontró una filmación con el título '{titulo_de_la_filmacion}'."

    titulo = filmacion.iloc[0]['title']
    anio_estreno = pd.to_datetime(filmacion.iloc[0]['release_date']).year
    score = filmacion.iloc[0]['popularity']

    return f"La película {titulo} fue estrenada en el año {anio_estreno} con un score/popularidad de {score}"

@app.post("/score_titulo/")
def get_score_titulo(titulo: str):
    result = score_titulo(titulo, df_movies1)
    return {"mensaje": result}


def votos_titulo(titulo_de_la_filmacion, df_movies1):
    filmacion = df_movies1[df_movies1['title'].str.lower() == titulo_de_la_filmacion.lower()]

    if filmacion.empty:
        return f"No se encontró una filmación con el título '{titulo_de_la_filmacion}'."

    titulo = filmacion.iloc[0]['title']
    anio_estreno = pd.to_datetime(filmacion.iloc[0]['release_date']).year
    cantidad_votos = filmacion.iloc[0]['vote_count']
    promedio_votos = filmacion.iloc[0]['vote_average']

    if cantidad_votos < 2000:
        return f"La película '{titulo}' no cumple con la condición de tener al menos 2000 valoraciones."

    return f"La película {titulo} fue estrenada en el año {anio_estreno}. La misma cuenta con un total de {cantidad_votos} valoraciones, con un promedio de {promedio_votos:.2f}"

@app.post("/votos_titulo/")
def get_votos_titulo(titulo: str):
    result = votos_titulo(titulo, df_movies1)
    return {"mensaje": result}


def get_actor(nombre_actor, df_movies2):
    peliculas_actor = df_movies2[df_movies2['name'] == nombre_actor]

    if peliculas_actor.empty:
        return f"No se encontraron películas en las que haya participado el actor '{nombre_actor}'."

    peliculas_actor['budget'] = pd.to_numeric(peliculas_actor['budget'], errors='coerce')
    peliculas_actor['revenue'] = pd.to_numeric(peliculas_actor['revenue'], errors='coerce')

    peliculas_actor = peliculas_actor.dropna(subset=['budget', 'revenue'])

    peliculas_actor['return'] = peliculas_actor['revenue'] - peliculas_actor['budget']

    total_retorno = peliculas_actor['return'].sum()
    cantidad_peliculas = len(peliculas_actor)
    promedio_retorno = total_retorno / cantidad_peliculas if cantidad_peliculas > 0 else 0

    return f"{nombre_actor} ha participado de {cantidad_peliculas} filmaciones, ha conseguido un retorno de {total_retorno:.2f} con un promedio de {promedio_retorno:.2f} por filmación"

@app.post("/get_actor/")
def get_actor_endpoint(nombre_actor: str):
    result = get_actor(nombre_actor, df_movies2)
    return {"mensaje": result}


def get_director(nombre_director, df_movies3):
    peliculas_director = df_movies3[df_movies3['director'] == nombre_director].copy()

    if peliculas_director.empty:
        return f"No se encontraron películas dirigidas por '{nombre_director}'."

    peliculas_director.loc[:, 'budget'] = pd.to_numeric(peliculas_director['budget'], errors='coerce')
    peliculas_director.loc[:, 'revenue'] = pd.to_numeric(peliculas_director['revenue'], errors='coerce')

    peliculas_director = peliculas_director.dropna(subset=['budget', 'revenue'])

    peliculas_director.loc[peliculas_director['budget'] == 0, 'budget'] = pd.NA

    peliculas_director = peliculas_director.dropna(subset=['budget', 'revenue'])

    peliculas_director['return'] = peliculas_director['revenue'] - peliculas_director['budget']

    total_retorno = peliculas_director['return'].sum()
    cantidad_peliculas = len(peliculas_director)
    promedio_retorno = total_retorno / cantidad_peliculas if cantidad_peliculas > 0 else 0

    peliculas_info = []
    for _, row in peliculas_director.iterrows():
        titulo = row['title']
        fecha_lanzamiento = row['release_date']
        retorno_individual = row['return']
        costo = row['budget']
        ganancia = row['revenue']
        peliculas_info.append(f"Película: {titulo}, Fecha de lanzamiento: {fecha_lanzamiento}, Retorno: {retorno_individual:.2f}, Costo: {costo:.2f}, Ganancia: {ganancia:.2f}")

    mensaje_peliculas = "\n".join(peliculas_info)
    mensaje_final = (f"El director {nombre_director} ha dirigido {cantidad_peliculas} películas, "
                     f"consiguiendo un retorno total de {total_retorno:.2f} con un promedio de {promedio_retorno:.2f} por filmación.\n"
                     f"Detalles de cada película:\n{mensaje_peliculas}")

    return mensaje_final

@app.post("/get_director/")
def get_director_endpoint(nombre_director: str):
    result = get_director(nombre_director, df_movies3)
    return {"mensaje": result}

# Usar TF-IDF Vectorizer en los títulos de las películas
tfidf = TfidfVectorizer(stop_words='english')
df_movies1['title'] = df_movies1['title'].fillna('')
tfidf_matrix = tfidf.fit_transform(df_movies1['title'])

# Calcular la similitud del coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Crear un índice para los títulos de las películas
indices = pd.Series(df_movies4.index, index=df_movies1['title']).drop_duplicates()

def recomendacion(titulo):
    # Verificar si el título existe en los datos
    if titulo not in indices:
        raise HTTPException(status_code=404, detail="Título no encontrado")
    
    # Obtener el índice de la película que coincide con el título
    idx = indices[titulo]

    # Obtener las puntuaciones de similitud de todas las películas con esa película
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenar las películas según las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener las puntuaciones de las 5 películas más similares
    sim_scores = sim_scores[1:6]

    # Obtener los índices de las películas más similares
    movie_indices = [i[0] for i in sim_scores]

    # Retornar los títulos de las películas más similares
    return df_movies1['title'].iloc[movie_indices].tolist()

# Definir la ruta de recomendación en FastAPI
@app.get("/recomendacion/")
def get_recomendacion(titulo: str):
    return {"recomendaciones": recomendacion(titulo)}



if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)