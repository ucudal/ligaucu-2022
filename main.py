from fastapi import FastAPI, HTTPException
from database import database as conexion, Campeonato, Equipos, Arbitros, Jugadores, Canchas, Goles
from schemas import *
from fastapi.encoders import jsonable_encoder

#creacion de app
app = FastAPI(title='Liga UCU', description='Liga UCU',
version='1.0')

#eventos
@app.on_event('startup')
def startup():
    if conexion.is_closed():
        conexion.connect()
        print('Conexion iniciada.')

@app.on_event('shutdown')
def shutdown():
    if not conexion.is_closed():
        conexion.close()
        print('Conexion cerrada.')

#servicios
@app.get('/campeonatos')
def campeonatos():
    campeonatos = Campeonato.select().dicts()
    return list(campeonatos)

@app.post('/equipos')
def crear_equipo(equipo: EquipoRequestModel):
    equipo = Equipos.create(
        nombreE = equipo.nombre
    )
    return equipo

@app.get('/equipos')
def get_equipos():
    equipos = Equipos.select().dicts()
    return list(equipos)

@app.delete('/equipos')
def eliminar_equipo(id: int):
    if(not Equipos.select().where(Equipos.idE == id)):
        return HTTPException(404, 'Equipo {id} no existe.'.format(id))
    Equipos.delete_by_id(id)
    return True


    
    
    
