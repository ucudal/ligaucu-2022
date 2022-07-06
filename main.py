from fastapi import FastAPI
from schemas import *
from fastapi.encoders import jsonable_encoder
from peewee import fn
from utils import sum_by_common_key
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
    return 'Campeonatos'

#@app.put('/jugadores')
#def modificar_jugador(jugador: JugadoresRequestModel):
#    if Jugadores.select().where(Jugadores.CIJ == jugador.CIJ):
#        jugadorResp = Jugadores.update({
#            Jugadores.nombre:jugador.nombre,
#            Jugadores.fecha_nac:jugador.fecha_nac,
#            Jugadores.idE:jugador.id_equipo,
#            Jugadores.es_golero:jugador.es_golero}
#        ).where(Jugadores.CIJ==jugador.CIJ).execute()
#        return True

#    jugadorResp = Jugadores.create(
#        CIJ=jugador.CIJ,
#        nombre=jugador.nombre,
#        fecha_nac=jugador.fecha_nac,
#        idE=jugador.id_equipo,
#        es_golero=jugador.es_golero
#    )
#    return jugadorResp._data_

    

@app.patch('/partidos')
def modificar_datos(partido: PartidoRequestModel,id_partido: int):
    if(not Partidos.select().where(Partidos.IdP==id_partido)):
       return HTTPException(404,'Partido {id_partido} no existe'.format(id_partido))
        
    partidos = Partidos.update({
        partidos.fecha:partido.fecha,
        partidos.hora:partido.hora,
        partidos.IdE1:partido.punt_equipo1,
        partidos.IdE2:partido.punt_equipo2,
        partidos.puntA:partido.id_equipo1,
        partidos.puntB:partido.id_equipo2,
        partidos.goles_GolesA:partido.goles_equipo1,
        partidos.goles_GolesB:partido.goles_equipo2,
        partidos.IdCAN:partido.id_cancha,
        partidos.CIA:partido.CIA,
        partidos.idC:partido.id_campeonato}
        
    ).where(Partidos.IdP==id_partido).execute()
    return True


    
    




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

@app.get('/goleador/{campeonato}')
def get_goleador(id_campeonato):
    partidos_camp = Partidos.select(Partidos.idP).where(Partidos.idC == id_campeonato)
    id_partidos = list(partidos_camp)
    #print(id_partidos)
    query = (Goles.select(Goles.CIJ, fn.SUM(Goles.cant_goles).alias('goles')).where(Goles.idP.in_(id_partidos)).group_by(Goles.CIJ).order_by(fn.SUM(Goles.cant_goles).desc())).dicts()
    goleadores = list(query)
    print(goleadores)
    CIJ_goleador = goleadores[0]['CIJ']

    nombre_goleador = Jugadores.select(Jugadores.nombre).where(Jugadores.CIJ == goleadores[0]['CIJ']).dicts()
    return list(nombre_goleador)
    
    
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
    partido = Partidos.create(
        fecha = partido.fecha,
        hora = partido.hora,
        idE1 = partido.idEquipo1,
        idE2 = partido.idEquipo2,
        IdCAN = partido.idCancha,
        CIA = partido.CIArbitro,
        idC = partido.idCampeonato
    
    )
    return partido
