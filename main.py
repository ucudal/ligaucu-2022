from functools import partial
from fastapi import FastAPI, HTTPException
from database import Partidos, database as conexion, Campeonato, Equipos, Arbitros, Jugadores, Canchas, Goles
from schemas import *
from fastapi.encoders import jsonable_encoder
from peewee import fn
from utils import sum_by_common_key

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


@app.delete('/equipos')
def eliminar_equipo(id: int):
    if(not Equipos.select().where(Equipos.idE == id)):
        return HTTPException(404, 'Equipo {id} no existe.'.format(id))
    Equipos.delete_by_id(id)
    return True

@app.patch('/resultado_partido/{id_partido,goles_equipo1,goles_equipo2}')#, response_model = PartidosRequestModel)
def patch_result_partido(id_partido: int, goles_equipo1: int, goles_equipo2: int):
    if(not Partidos.select().where(Partidos.idP == id_partido)):
        return HTTPException(404, 'Partido {id_partido} no existe.'.format(id_partido))
    if goles_equipo1 > goles_equipo2:
        puntos_equipo1 = 3
        puntos_equipo2 = 0
    elif goles_equipo1 < goles_equipo2:
        puntos_equipo1 = 0
        puntos_equipo2 = 3
    else:
        puntos_equipo1 = 1
        puntos_equipo2 = 1
    
    res = (Partidos
           .update({Partidos.GolesA: goles_equipo1, Partidos.GolesB: goles_equipo2, Partidos.puntA: puntos_equipo1, Partidos.puntB: puntos_equipo2})
           .where(Partidos.idP == id_partido)
           .execute())
    return True

@app.get('/golero')
def get_golero_menos_vencido():

    subquery = ((Partidos.select(Partidos.idE2.alias('id_Eq'), fn.SUM(Partidos.GolesA).alias('total_goles')).group_by(Partidos.idE2)) + (Partidos.select(Partidos.idE1.alias('id_Eq'), fn.SUM(Partidos.GolesB).alias('total_goles')).group_by(Partidos.idE1))).dicts() 
    goles_en_contra = sum_by_common_key(list(subquery), index_key = 'id_Eq')
    id_eq_menos_goles = min(goles_en_contra, key=lambda x:x['total_goles'])
    golero = Jugadores.select(Jugadores.nombre).where((Jugadores.idE == id_eq_menos_goles['id_Eq']) & (Jugadores.es_golero == True)).dicts()

    return list(golero)

    
    
    
    
    
