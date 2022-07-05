from fastapi import FastAPI, HTTPException
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
    if(not Goles.select().where(Goles.CIJ==goles.CIJ)):
        goles = Goles.create({
            Goles.CIJ : goles.CIJ,
            Goles.idP : goles.id_partido,
            Goles.cant_goles : goles.cant_goles
        })
    goles = Goles.update({
        Goles.CIJ : goles.CIJ,
        Goles.idP : goles.id_partido,
        Goles.cant_goles : goles.cant_goles
    })
    return True

#@app.get('/jugadores')
#def jugadores(CI: int):
#    if(not Jugadores.select().where(Jugadores.CIJ == CI)):
#        return HTTPException(404,'Jugador {CI} no existe'.format(CI))
#    Jugadores.get_by_CI(CI)
#    return True



#@app.get('/equipos_ordenados')
#def equipos_ordenados():
#Basado en imagen del docente:
#for equipo en Equipos:
#   if equipo.id = equipo1
#       {equipo.id, punt + puntaje}
#   if equipo.id = equipo2
#       {equipo.id, punt + puntaje}
#return dice ordenado por puntaje