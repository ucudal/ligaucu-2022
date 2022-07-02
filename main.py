from fastapi import FastAPI
from database import database as conexion, Campeonato, Equipos, Arbitros, Jugadores, Canchas, Goles
from schemas import *

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

@app.get('/jugadores')
def jugadores():
    jugadores = Jugadores.select().dicts()
    return list(jugadores)

@app.get('/equipos')
def get_equipos():
    equipos = Equipos.select().dicts()
    return list(equipos)

@app.put('/goles')
def modificar_goles(goles: GolesRequestModel):
    if(not Goles.select().where(Goles.CIJ==CI)):
        goles = Goles.create(
            CIJ=goles.CIJ,
            IdP=goles.IdP,
            cant_goles=goles.cant_goles
        )
    goles = Goles.update(
        CIJ=goles.CIJ,
        IdP=goles.IdP,
        cant_goles=goles.cant_goles
    )
    return

@app.get('/jugadores')
def jugador(CI:int):
    if(not Jugador.select().where(Jugador.CIJ==CI)):
        return HTTPException(404,'Jugador {CI} no existe'.format(CI))
    Jugador.get_by_CI(CI)
    return True
