

import psycopg2

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext

DATABASE = 'postgresql://localhost/scheduler'
def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    # if "db" not in g:
    #     g.db = psycopg2.connect(
    #         current_app.config["DATABASE"], detect_types=psycopg2.PARSE_DECLTYPES
    #     )
    #     g.db.row_factory = psycopg2.Row
    #
    # return g.db
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(DATABASE)
    return db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    cur = db.cursor()

    cur.execute("DROP TABLE IF EXISTS req;")
    cur.execute("DROP TABLE IF EXISTS maker;")


    cur.execute("CREATE TABLE maker(id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);")

    cur.execute("CREATE TABLE req(id SERIAL PRIMARY KEY, maker_id INTEGER NOT NULL, created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, req_date TEXT NOT NULL, req_time TEXT NOT NULL, location TEXT NOT NULL, priority INTEGER NOT NULL, capacity INTEGER NOT NULL,FOREIGN KEY (maker_id) REFERENCES maker (id));")


    # with current_app.open_resource("schema.sql") as f:
    #     db.cursor().execute(f.read())
    #     db.commit()
    #     db.cursor().close()
    #     #db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
