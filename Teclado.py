from typing import Tuple

class Teclado:
    teclas: Tuple
    voto: str

    def __init__(self):
        self.teclas = (
            ('1', '2', '3'),
            ('4', '5', '6'),
            ('7', '8', '9'),
            (None, '0', None),
            ('BRANCO', 'CORRIGE', 'CONFIRMA')
        )
        self.voto = ''
    
    def clicar(self, digito: str):
        if digito == 'CONFIRMA':
            return digito # RETORNA CONFIRMA

        if digito == 'BRANCO':
            self.voto = '' # Limpa a string self.voto
            return digito # Retorna BRANCO
        
        if digito == 'CORRIGE':
            self.voto = '' # Limpa a string self.voto

        else:
            self.voto += digito