import sqlite3
import json


def migrate(db: sqlite3.Connection):
    # keeping things simple for now.. someday this might get
    #  split out into some kind of migration system
    cur = db.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS verb (
            infinitive TEXT PRIMARY KEY,
            conjugations TEXT NOT NULL
        )
        """
    )
    db.commit()
    cur.close()


def get_verb_names(db: sqlite3.Connection):
    cur = db.cursor()
    cur.execute("SELECT infinitive FROM verb")
    rows = cur.fetchall()
    cur.close()
    return [row[0] for row in rows]


def get_verb(db: sqlite3.Connection, infinitive):
    cur = db.cursor()
    cur.execute("SELECT * FROM verb WHERE infinitive=?", (infinitive,))
    row = cur.fetchone()
    cur.close()
    return (
        {
            "infinitive": row[0],
            "conjugations": json.loads(row[1]),
        }
        if row
        else None
    )


def upsert_verb(db: sqlite3.Connection, infinitive, conjugations=[]):
    if type(infinitive) != str:
        raise TypeError("infinitive must be a string")

    cur = db.cursor()
    cur.execute(
        """
        INSERT INTO verb (infinitive, conjugations) VALUES (?, ?)
            ON CONFLICT (infinitive)
            DO UPDATE SET conjugations=excluded.conjugations
        """,
        (infinitive, json.dumps(conjugations)),
    )
    db.commit()
    cur.close()
