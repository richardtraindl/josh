
import psycopg2
import urllib.parse as urlparse
import os

import click
from flask import current_app, g
from flask.cli import with_appcontext

from .schema import sqldrops, sqlcreates


def get_db():
    if('db' not in g):
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        try:
            g.db = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        except:
            print("unable to connect to the database!")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if(db is not None):
        db.close()


def init_db():
    db = get_db()
    cur = db.cursor()

    for sqldrop in sqldrops:
        cur.execute(sqldrop)
    db.commit()

    for sqlcreate in sqlcreates:
        cur.execute(sqlcreate)
    cur.close()
    db.commit()
    db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

