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

#servicios
@app.get('/campeonatos')
def campeonatos():
    return 'Campeonatos'

@app.put('/jugadores')
def modificar_jugador(jugador: JugadorRequestModel):
    if(not Jugador.select().where(Jugador.CIJ==CI)):
        jugador = Jugadores.create(
            CIJ=jugador.CIJ,
            nombre=jugador.nombre,
            fecha_nac=jugador.fecha_nac,
            IdE=jugador.IdE,
            es_golero=jugador.es_golero
        )
    jugador = Jugadores.update(
        CIJ=jugador.CIJ,
        nombre=jugador.nombre,
        fecha_nac=jugador.fecha_nac,
        IdE=jugador.IdE,
        es_golero=jugador.es_golero
    )

@app.patch('/partidos')
def modificar_datos(partido: PartidoRequestModel):
    if(not partido.select().where(partido.IdP==Id)):
       return  HTTP(404,'Partido {id} no existe')
        
    partido = Partidos.update(
        IdP=partido.IdP,
        fecha=partido.fecha,
        hora=partido.hora,
        IdE1=partido.IdE1,
        IdE2=partido.IdE2,
        puntA=partido.puntA,
        puntB=partido.puntB,
        GolesA=partido.GolesA,
        GolesA=partido.GolesB,
        IdCAN=partido.IdCAN,
        CIA=partido.CIA,
        idC=partido.idC
        
    )

    
    



@app.get('/goleadores')
def goleador(CIJ)
    if(Jugador.select().where())
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

    
    
    
    
    
