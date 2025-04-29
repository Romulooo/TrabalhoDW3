from flask import Flask, request
import psycopg
import requests

app = Flask(__name__)
connection_db = psycopg.connect('dbname=nerdgeeks user=postgres password=3f@db host=164.90.152.205 port=80')



@app.route("/consultarnome/<title>", methods=["GET"])
def consultar_nome(title):
    cursor = connection_db.cursor()
    cursor.execute('insert into filmes (titulo, id) values (%s, %s)', (title, id))
    r = requests.get(f'http://www.omdbapi.com/?apikey=221fdad0&t={title}')
    title = r.json()["Title"]
    print(title)
    return(r.text)

