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

class Partidos(Model):
    idC = IntegerField(primary_key=True)
    Fecha = DateField()
    hora = TimeField()
    idE1 = IntegerField()
    idE2 = IntegerField()
    puntA = IntegerField()
    puntB = IntegerField()
    GolesA = IntegerField()
    GolesB = IntegerField()
    IdCAN = IntegerField()
    CIA = CharField()
    idC = IntegerField()

    class Meta:
        database= database
        table_name= 'partidos'