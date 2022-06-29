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
    nombre = CharField()

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
