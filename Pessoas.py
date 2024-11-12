import random

class Documento:
    __rg: str
    __cpf: str

    def __init__(self, rg: str = '', cpf: str = ''):
        # cpf = 11 digitor
        # rg = 9 digitos
        self.__rg = ''
        self.__cpf = ''
        if cpf == '':
            self.criar_cpf()
        if rg == '':
            self.criar_rg()
    
    def criar_rg(self):
        for digito in range (0, 9):
            i = random.randint(0, 9)
            if digito in [2, 5]:
                self.__rg += '.'
            elif digito == 8:
                self.__rg += '-'
            self.__rg += str(i)
            
    #método para criar cpf aleatório (o cpf não passa por nenhuma verificação, é só um exemplo para facilitar o uso)
    def criar_cpf(self):
        for digito in range(0, 11):
            i = random.randint(0, 9)
            if digito in [3, 6]:
                self.__cpf += '.'
            elif digito == 9:
                self.__cpf += '-'
            self.__cpf += str(i)
    
    def get_rg(self):
        return self.__rg
    
    def get_cpf(self):
        return self.__cpf

    def __str__(self):
        info = (
            f'RG: {self.__rg}\n'
            f'CPF: {self.__cpf}'
        )
        return info 

doc = Documento()
print (doc)
