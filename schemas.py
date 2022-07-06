import string
from datetime import date, time, datetime
from pydantic import BaseModel

class EquipoRequestModel(BaseModel):
    nombre: str

class ArbitrosRequestModel(BaseModel):
    nombre: str
    CI: int

class CampeonatosRequestModel(BaseModel):
    id : int
    ano : int
    nombre: str

class CanchasRequestModel(BaseModel):
    id : int
    nombre: str

class GolesRequestModel(BaseModel):
    CIJ : int
    id_partido : int
    cant_goles: int

#class JugadoresRequestModel(BaseModel):
#    CIJ: int
#    nombre: str
#    fecha_nac: datetime.date
#    id_equipo: int
#    es_golero: bool

#class PartidosRequestModel(BaseModel):
#    id_partido : int
#    fecha : datetime.date
#    hora : datetime.time
#    id_equipo1 : int
#    id_equipo2 : int
#    punt_equipo1 : int
#    punt_equipo2 : int
#    goles_equipo1 : int
#    goles_equipo2 : int
#    id_cancha : int
#    CIA : int
#    id_campeonato : int
class PartidoRequestModel(BaseModel):
    fecha : date
    hora : time
    idEquipo1 : int
    idEquipo2 : int
    idCancha : int
    CIArbitro : int
    idCampeonato : int
