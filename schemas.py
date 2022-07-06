from datetime import date, time, datetime
from pydantic import BaseModel

class EquipoRequestModel(BaseModel):
    nombre: str

class PartidoRequestModel(BaseModel):
    fecha : date
    hora : str
    idEquipo1 : int
    idEquipo2 : int
    idCancha : int
    CIArbitro : int
    idCampeonato : int