import sqlite3
import base64
import configparser

import requests
from flask import *

import database

config = configparser.ConfigParser()
config.read('config.ini')
DATABASE_PATH = config.get('DATABASE', 'PATH')


app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index_cat():
    # TODO rertonando foto do gato e o id 
    get_picture = requests.get('https://api.thecatapi.com/v1/images/search')  # dando get na foto do gato
    url_pic = get_picture.json()[0]["url"]  # get da url da foto do gato
    id_pic = get_picture.json()[0]["id"]  # get do id da foto do gato
    base64_pic = base64.b64encode(requests.get(url_pic).content).decode("UTF-8")

    cur = get_db().cursor()  # conecta ao db
    database.add_cat_to_bd(base64_pic, id_pic, cur)  # add a foto do gato ao db
    get_db().commit()  # commita o db
    return render_template('index.html', data=base64_pic)


@app.route('/<cat_id>/')
def get_cat_by_id(cat_id):
    # TODO retorna foto do gato e o id se o id existir
    cur = get_db().cursor()
    url = database.find_cat_id(cat_id, cur)  # tenta buscar o id no db
    if url is None:
        abort(404)  # se o db não encontrar o id, retorna 404
    else:
        return render_template('index.html', data=url[0])


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    database.create_db()  # cria o db se nao existir
    app.run()
