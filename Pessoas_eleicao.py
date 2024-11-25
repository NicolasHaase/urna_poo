import pickle
from typing import List
from Pessoas import *



# Detalhe importante, em um sistema mais "real", os parâmetros seriam necessários, mas para deixar mais fácil criar objetos
# De classes que herdam de pessoa, os parâmetros não precisam ser passados e são criados automaticamente
class Eleitor(Pessoa):
    titulo: str
    zona: str
    secao: str

    def __init__(self, titulo: str = '', zona: str = '', secao: str = '', nome: str = '',
    nacionalidade: str = 'Brasileira', documento: Documento() = None, contato: Contato() = None):

        super().__init__(nome=nome, nacionalidade=nacionalidade, documento=documento, contato=contato)

        self.titulo = titulo
        if self.titulo == '':
            self.criar_titulo()

        self.zona = zona
        if self.zona == '':
            self.criar_zona()

        self.secao = secao
        if self.secao == '':
            self.criar_secao()

    def criar_titulo(self):
        for digito in range (12):
            i = str(random.randint(0, 9))
            if digito in [4, 8]:
                self.titulo += ' '
            self.titulo += i

    def criar_zona(self):
        for digito in range (3):
            i = str(random.randint(0, 9))
            self.zona += i

    def criar_secao(self):
        for digito in range (4):
            i = str(random.randint(0, 9))
            self.secao += i

    def __str__(self):
        info = super().__str__()
        info += '\n\n'
        info += (
            f'Título: {self.titulo}\n'
            f'Zona: {self.zona}\n'
            f'Seção: {self.secao}\n'
        )
        return info


# Nada foi feito com "Mesario", então a classe ficará só com pass, mas já vai existir para possíveis adições futuras
class Mesario(Eleitor):
    pass


# Candidatos podem votar, então vão herdar de eleitor
class Candidato(Eleitor):
    numero_eleitoral: int

    def __init__(self, numero_eleitoral: int, titulo: str = '', zona: str = '', secao: str = '', nome: str = '',
    nacionalidade: str = 'Brasileira', documento: Documento() = None, contato: Contato() = None):

        #inicia Eleitor
        super().__init__(titulo=titulo, zona=zona, secao=secao, nome=nome, nacionalidade=nacionalidade,
                         documento=documento, contato=contato)

        self.numero_eleitoral = numero_eleitoral
        self.__votos = 0

    def __str__(self):

        info = super().__str__()
        info += (
            f'Número eleitoral: {self.numero_eleitoral}\n'
        )
        return info
