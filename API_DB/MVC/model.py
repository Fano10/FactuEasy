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
    idUser = IntegerField()
    name = CharField()
    date = DateField()#ne prend pas en compte l'heure et minute
    total = FloatField()

class Product(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    description = CharField()
    idBill = IntegerField()
    idUser = IntegerField()
    price = FloatField()

class Users(BaseModel):
    id = AutoField(primary_key=True)
    username = CharField()
    password = CharField()

@click.command("init-db")
@with_appcontext
def init_db_command():
    mesModeles = [Bill,Product,Users]
    database = SqliteDatabase(get_db_path())
    try:
        database.create_tables(mesModeles)
        Users.create(
            username = 'admin',
            password = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918' #admin
        )
        Users.create(
            username = 'guest',
            password = '84983c60f7daadc1cb8698621f802c0d9f9a3c3c295c810748fb048115c186ec' #guest
        )
        click.echo("Initialized the database. ")
    except:
        click.echo("Table already exist ...")

def init_app(app):
    app.cli.add_command(init_db_command)