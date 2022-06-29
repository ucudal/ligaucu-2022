from datetime import date
from peewee import *

#conexion
database = PostgresqlDatabase(
    'postgres',
    user='postgres',
    password='ligaucu.',
    host='ligaucu.cbz3dhyiej2f.us-east-2.rds.amazonaws.com',
    port=5432)

#modelos
class Campeonato(Model):
    idC = IntegerField(primary_key=True)
    ano = CharField()
    nombreC = CharField()

    class Meta:
        database= database
        table_name= 'campeonatos'


class Jugadores(Model):
    ci_j = IntegerField(primary_key=True)
    nombre = CharField()
    fecha_nac = DateField()
    es_golero = BooleanField()
    id_equipo = IntegerField(ForeignKeyField=True)

    class Meta:
        database = database
        table_name = 'jugadores'

class Goles(Model):
    ci_j = IntegerField(ForeignKeyField=True)
    id_p = IntegerField(ForeignKeyField=True)
    cant_goles = IntegerField(ForeignKeyField=True)

    class Meta:
        database = database
        table_name = 'goles'