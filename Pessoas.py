import random
from abc import ABC


class Documento:
    __rg: str
    __cpf: str

    def __init__(self, rg: str = '', cpf: str = ''):
        # cpf = 11 digitos
        # rg = 9 digitos
        self.__rg = ''
        self.__cpf = ''
        if cpf == '':
            self.criar_cpf()
        if rg == '':
            self.criar_rg()
    
    #metodo para criar rg aleatório (o rg não passa por nenhuma verificação, é s)
    def criar_rg(self):
        for digito in range (0, 9):
            i = random.randint(0, 9)
            if digito in [2, 5]:
                self.__rg += '.'
            elif digito == 8:
                self.__rg += '-'
            self.__rg += str(i)
            
    #metodo para criar cpf aleatório (o cpf não passa por nenhuma verificação, é só um exemplo para facilitar o uso)
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


class Contato:
    telefone: str
    email: str
    __endereco: str

    def __init__(self, telefone: str = '', email: str = '', endereco: str = ''):
        if telefone == '':
            self.telefone = '123456789'
        else:
            self.telefone = telefone

        if email == '':
            self.email = 'exemplo@gmail.com'
        else:
            self.email = email

        if endereco == '':
            self.__endereco = 'Rua Exemplo, numero 0'
        else:
            self.__endereco = endereco

    def get_endereco(self):
        return self.__endereco

    def __str__(self):
        info = (
            f'Telefone: {self.telefone}\n'
            f'Email: {self.email}\n'
            f'Endereço: {self.__endereco}'
        )
        return info


class Pessoa(ABC):
    nome: str
    nacionalidade: str
    documento: Documento
    contato: Contato

    def __init__(self, nome: str = '', nacionalidade: str = 'Brasileira', documento: Documento = Documento(), contato: Contato = Contato()):
        if nome == '':
            nomes = ['Arthur Almeida Lima', 'Daniel Santiago Purificação', 'Nicolas Jimenes Haase', 'Pedro Dias Guedes Santos']
            self.nome = nomes[random.randint(0, 3)]

        self.nacionalidade = nacionalidade
        self.documento = documento
        self.contato = contato

    def __str__(self):
        info = (
            f'Nome: {self.nome}\n'
            f'Nacionalidade: {self.nacionalidade}\n\n'
            f'Documentos:\n{self.documento}\n\n'
            f'Contatos:\n{self.contato}'
        )
        return info