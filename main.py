from fastapi import FastAPI
from schemas import *

#creacion de app
app = FastAPI(title='Liga UCU', description='Liga UCU',
version='1.0')

#servicios
@app.get('/campeonatos')
def campeonatos():
    return 'Campeonatos'

@app.put('/jugadores')
def modificar_jugador(jugador: JugadoresRequestModel):
    if Jugadores.select().where(Jugadores.CIJ == jugador.CIJ):
        jugadores : Jugadores.update({
            Jugadores.nombre:jugador.nombre,
            Jugadores.fecha_nac:jugador.fecha_nac,
            Jugadores.idE:jugador.IdE,
            Jugadores.es_golero:jugador.es_golero}
        ).where(Jugadores.CIJ==jugador.CIJ).execute()
        return True

    jugadores : Jugadores.create(
        CIJ=jugador.CIJ,
        nombre=jugador.nombre,
        fecha_nac=jugador.fecha_nac,
        idE=jugador.IdE,
        es_golero=jugador.es_golero
    )
    return jugadores._data_

    

@app.patch('/partidos')
def modificar_datos(partido: PartidosRequestModel,id_partido: int):
    if(not Partidos.select().where(Partidos.IdP==id_partido)):
       return HTTPException(404,'Partido {id_partido} no existe'.format(id_partido))
        
    partidos = Partidos.update({
        partidos.fecha:partido.fecha,
        partidos.hora:partido.hora,
        partidos.punt_equipo1:partido.IdE1,
        partidos.punt_equipo2:partido.IdE2,
        partidos.id_equipo1:partido.puntA,
        partidos.id_equipo2:partido.puntB,
        partidos.goles_equipo1:partido.GolesA,
        partidos.goles_equipo2:partido.GolesB,
        partidos.id_cancha:partido.IdCAN,
        partidos.CIA:partido.CIA,
        partidos.id_campeonato:partido.idC}
        
    ).where(Partidos.IdP==id_partido).execute()
    return True


    
    




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

    
    


