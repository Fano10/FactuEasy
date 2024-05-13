import click
import os
from flask.cli import with_appcontext
from peewee import *

def get_db_path():
    return os.environ.get('DATABASE','./db.sqlite') # recuperer le chemin de la base de donnee a partir d'une variable d'environnement sinon mette dans ./

class BaseModel(Model): #une classe de base pour tous les models de donnees de l'applicatopn
    class Meta: # fournit des metadonnes specifiques a la classe BaseModel
        database = SqliteDatabase(get_db_path())

class Bill(BaseModel):
    id = AutoField(primary_key=True)
    nom = CharField()
    date = DateField()#ne prend pas en compte l'heure et minute
    total = FloatField()

class Product(BaseModel):
    id = AutoField(primary_key=True)
    nom = CharField()
    idBill = IntegerField()
    price = FloatField()


@click.command("init-db")
@with_appcontext
def init_db_command():
    mesModeles = [Bill,Product]
    database = SqliteDatabase(get_db_path())
    try:
        database.create_tables(mesModeles)
        click.echo("Initialized the database. ")
    except:
        click.echo("Table already exist ...")

def init_app(app):
    app.cli.add_command(init_db_command)