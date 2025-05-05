from flask import Flask
import psycopg
import requests

# Armazena a aplicação em uma variável para inicia-lá depois
app = Flask(__name__)

# Armazena a conexão em uma variável, com ela já sendo excecutada
connection_db = psycopg.connect('dbname=nerdgeeks user=postgres password=3f@db host=164.90.152.205 port=80')

# Definição da rota consultar nome por título ou id
@app.route("/consultarnome/<title>", methods=["GET"])
def consultar_nome(title):

    # Define o cursor
    cursor  = connection_db.cursor()

    # Verifica se foi passado um título ou um id (todos os ids iniciam com "tt")
    if title[0] + title[1] == "tt":
        # Se for, faz a requisição pelo id
        r = requests.get(f'http://www.omdbapi.com/?apikey=221fdad0&i={title}')
    else:
        # Se não, faz pelo título
        r = requests.get(f'http://www.omdbapi.com/?apikey=221fdad0&t={title}')

    # Verifica se o filme já está na tabela
    id = r.json()["imdbID"]
    cursor.execute(f"select count(*) from filmes_series where id = '{id}'")
    rows = cursor.fetchall()

    # Se retornou algo, mostrar o texto
    if rows != [(0,)]:
        return r.text
    # Se não, inclui na tabela
    else:
        titulo = r.json()["Title"]
        year = r.json()["Year"]
        rated = r.json()["Rated"]
        released = r.json()["Released"]
        runtime = r.json()["Runtime"]
        genre = r.json()["Genre"]
        director = r.json()["Director"]
        writer = r.json()["Writer"]
        actors = r.json()["Actors"]
        plot = r.json()["Plot"]
        language = r.json()["Language"]
        country = r.json()["Country"]
        awards = r.json()["Awards"]
        poster = r.json()["Poster"]
        ratings = ""
        for i in r.json()["Ratings"]:
            ratings += (i["Source"]+ " : "+ i["Value"] + ", ")
        metascore = r.json()["Metascore"]
        imdbrating = r.json()["imdbRating"]
        imdbvotes = r.json()["imdbVotes"]
        type = r.json()["Type"]

        sql = """
        INSERT INTO filmes_series (
            id, titulo, year, rated, released, runtime, genre, director,
            writer, actors, plot, language, country, awards, poster,
            ratings, metascore, imdbrating, imdbvotes, type
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            id, titulo, year, rated, released, runtime, genre, director,
            writer, actors, plot, language, country, awards, poster,
            ratings, metascore, imdbrating, imdbvotes, type
        )

        cursor.execute(sql, values)
        connection_db.commit()
        return r.text
