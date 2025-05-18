from flask import Flask, jsonify, request, g
import sqlite3
from db import upsert_verb, get_verb, get_verb_names, migrate
from settings import SQLITE_DB_FILENAME


app = Flask(__name__)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_FILENAME)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


with app.app_context():
    migrate(get_db())


@app.route("/verb", methods=["GET"])
def http_get_verbs():
    db = get_db()
    return {"verbs": get_verb_names(db)}


@app.route("/verb/<verb>", methods=["GET"])
def http_get_verb(verb):
    db = get_db()
    result = get_verb(db, verb)
    if not result:
        return "verb not found", 404
    return jsonify(result)


@app.route("/verb/<verb>", methods=["PUT"])
def http_post_verb(verb):
    req = request.json

    if "conjugations" not in req:
        return jsonify("missing conjugations in request body"), 400

    db = get_db()
    upsert_verb(
        db=db,
        infinitive=verb,
        conjugations=req.get("conjugations"),
    )
    return "Verb added", 201
