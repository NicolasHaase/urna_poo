import pickle
from typing import List
from Pessoas import *


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


class Mesario(Eleitor):
    pass


#Candidatos podem votar, então vão herdar de eleitor
class Candidato(Eleitor):
    numero_eleitoral: int
    __votos: int

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
'''
candidato = Candidato (numero_eleitoral=123)

print (candidato)

eleitores: List = [Eleitor(), Eleitor(), Eleitor(), Eleitor(), Eleitor(), Eleitor(), Eleitor(), Eleitor()]
with open('eleitores', 'wb') as arquivo:
    pickle.dump(eleitores, arquivo)
'''
'''
with open('eleitores', 'rb') as arquivo:
    eleitores = pickle.load(arquivo)

for eleitor in eleitores:
    print (eleitor.titulo)
    8277 7702 1064
    3631 7131 8173
    3460 7183 7656
    3613 0537 3981
    3600 1149 4843
    6843 1665 2454
    2974 0846 7403
    1393 7732 5600
    '''