from flask import Flask
import psycopg
import requests

app = Flask(__name__)
connection_db = psycopg.connect('dbname=nerdgeeks user=postgres password=3f@db host=164.90.152.205 port=80')

@app.route("/consultarnome/<title>", methods=["GET"])
def consultar_nome(title):
    cursor  = connection_db.cursor()
    
    if title[0] + title[1] == "tt":
        r = requests.get(f'http://www.omdbapi.com/?apikey=221fdad0&i={title}')
    else:
        r = requests.get(f'http://www.omdbapi.com/?apikey=221fdad0&t={title}')
    
    id = r.json()["imdbID"]
    cursor.execute(f"select count(*) from filmes_series where id = '{id}'")
    rows = cursor.fetchall()
    if rows != [(0,)]:
        return r.text
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