from fastapi import FastAPI

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
