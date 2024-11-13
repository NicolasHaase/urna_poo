from Pessoas import *


class Eleitor(Pessoa):
    titulo: str
    zona: int
    secao: int
    pass


class Mesario(Eleitor):
    pass


#Candidatos podem votar, então vão herdar de eleitor
class Candidato(Eleitor):
    pass