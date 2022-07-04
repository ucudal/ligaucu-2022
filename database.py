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

class Equipos(Model):
    idE = IntegerField(primary_key=True)
    nombreE = CharField()

    class Meta:
        database= database
        table_name= 'equipos'

class Arbitros(Model):
    CIA = IntegerField(primary_key=True)
    nombreA = CharField()

    class Meta:
        database= database
        table_name= 'arbitros'

class Canchas(Model):
    idCAN = IntegerField(primary_key=True)
    nombreCAN = CharField()

    class Meta:
        database= database
        table_name= 'canchas'

class Jugadores(Model):
    CIJ = IntegerField(primary_key=True)
    nombre = CharField()
    Fecha_nac = DateField()
    es_golero = BooleanField()
    idE = IntegerField()

    class Meta:
        database = database
        table_name = 'jugadores'

class Goles(Model):
    CIJ = IntegerField()
    idP = IntegerField()
    cant_goles = IntegerField()

    class Meta:
        database = database
        table_name = 'goles'

class Partidos(Model):
    idP = IntegerField(primary_key=True)
    Fecha = DateField()
    hora = TimeField()
    idE1 = IntegerField()
    idE2 = IntegerField()
    puntA = IntegerField()
    puntB = IntegerField()
    GolesA = IntegerField()
    GolesB = IntegerField()
    IdCAN = IntegerField()
    CIA = IntegerField()
    idC = IntegerField()

    class Meta:
        database = database
        table_name = 'partidos'