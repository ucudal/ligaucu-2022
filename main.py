from tkinter import HORIZONTAL
from fastapi import FastAPI

from database import database as conexion, Partidos, Campeonato, Equipos, Arbitros, Jugadores, Canchas, Goles
from schemas import *

#creacion de app
app = FastAPI(title='Liga UCU', description='Liga UCU',
version='1.0')

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

@app.get('/arbitros')
def arbitros():
    arbitros = Arbitros.select().dicts()
    return list(arbitros)

@app.get('/canchas')
def canchas():
    canchas = Canchas.select().dicts()
    return list(canchas)

@app.get('/fixture')
def fixture(id: int):
    if(not Campeonato.select().where(Campeonato.idC == id)):
        return HTTPException(404, 'Campeonato {id} no existe.' .format(id))
    fixture = Partidos.select().where((Partidos.idC == id)).dicts()
    return list(fixture)

@app.post('/partido')
def crear_partido(partido: PartidoRequestModel):
    partido = Partidos.create({
        Partidos.Fecha : partido.fecha,
        Partidos.hora : partido.hora,
        Partidos.idE1 : partido.idEquipo1,
        Partidos.idE2 : partido.idEquipo2,
        Partidos.IdCAN : partido.idCancha,
        Partidos.CIA : partido.CIArbitro,
        Partidos.idC : partido.idCampeonato
    
    })
    return partido
