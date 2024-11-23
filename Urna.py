import tkinter as tk
from tkinter import *
from tkinter import ttk
from Teclado import *
from typing import List
from Pessoas_eleicao import *
from abc import ABC
import pickle


class InfoUrna(ABC):
    candidatos: List[Candidato]
    teclado: Teclado # Do arquivo Teclado.py
    eleitores: List[Eleitor]

    def __init__(self):
        self.teclado = Teclado()
        self.candidatos = []
        self.carregar_candidatos()
        self.eleitores = []
        self.carregar_eleitores()

    def verificar_voto(self):
        for candidato in self.candidatos:
            if self.teclado.voto == str(candidato.numero_eleitoral):
                return True
        return False

    def verificar_eleitor(self, titulo: str):
        for eleitor in self.eleitores:
            if self.teclado.voto == str(eleitor.titulo.strip()):
                return True
        return False


    def carregar_candidatos(self):
        with open('candidatos.pkl', 'rb') as arquivo:
            self.candidatos = pickle.load(arquivo)

    def registrar_candidatos(self):
        with open('candidatos.pkl', 'wb') as arquivo:
            pickle.dump(self.candidatos, arquivo)

    def carregar_eleitores(self):
        with open('eleitores.pkl', 'rb') as arquivo:
            self.eleitores = pickle.load(arquivo)

    def registrar_eleitores(self):
        with open('eleitores.pkl', 'wb') as arquivo:
            pickle.dump(self.eleitores, arquivo)

    def registrar_voto(self):
        pass



class Urna(InfoUrna):
    janela: tk.Tk # Janela principal (A urna em si)
    voto: StringVar # StringVar é uma forma de modificar textos dentro da janela
    frame: ttk.Frame # Até onde entendi, ttk.Frame é a distância que a borda da tela fica dos botões

    def __init__(self):
        super().__init__()
        self.janela = Tk()
        self.frame = ttk.Frame(self.janela, padding=0)
        self.frame.grid()
        self.largura = 500
        self.altura = 350

        self.voto = StringVar() # Criação do texto do voto
        self.voto.set('_ _')
    
    def add_numero(self, texto):

        # Essa verificação faz com que o usuário não possa digitar nada em quanto "FIM" está na tela
        if self.voto.get() == 'FIM':
            return

        retorno = self.teclado.clicar(texto)
        self.atualizar_voto()

        if super().verificar_voto():
            print ('Candidato Verdadeiro') # Apenas por agora, mostraremos a "foto" do candidato depois

        if retorno is not None: # Se não retornar nada, significa que o eleitor 
            #apertou em algum número ou em 'CORRIGE' ou em 'BRANCO'
            if retorno == 'BRANCO':
                pass # O voto tem que ser "anulado" ainda

            elif retorno == 'CONFIRMA':
                if super().verificar_voto():
                    self.resetar_urna() # Reseta os parâmetros da urna
                self.teclado.voto = ''
                # Limpa o voto caso seja confirmado, independente se o voto foi válido ou não

    def iniciar_teclado(self):

        label_voto = ttk.Label(self.frame, textvariable=self.voto, font=("Arial", 20))
        label_voto.grid(row=0, column=0, columnspan=3, pady=20)
        self.janela.resizable(True, True)
        self.janela.geometry(f'{self.largura}x{self.altura}')

        for i in range (0, 5):
            self.janela.rowconfigure(i, weight=1)
        for i in range (0, 3):
            self.janela.columnconfigure(i, weight=1)

        for i in range(0, 5):
            for j in range(0, 3):
                if self.teclado.teclas[i][j]: # Verifica se não é None, já que o teclado não é um 5x3 perfeito
                    ttk.Button(self.janela, text=self.teclado.teclas[i][j],
                    command=lambda texto=self.teclado.teclas[i][j]:
                    self.add_numero(texto=texto)).grid(column=j, row=i+1, sticky='nsew') #i+1 pra não sobrepor o label
                # Esse 'command=[...]' é dizendo que quando o botão for apertado, ele vai para esse método "add_numero"
                #que vai adicionando o número em uma string dos votos
                
    def iniciar_urna(self):
        self.iniciar_teclado()
        self.janela.mainloop()

    # Método para atualizar o voto, se for vazio, ele coloca '_ _' Para indicar que um número pode ser digitado
    def atualizar_voto(self):
        if self.teclado.voto == '':
            self.voto.set('_ _')
        else:
            self.voto.set(self.teclado.voto)

    def pegar_titulo(self):
        pass

    def pegar_voto(self):
        pass

    def resetar_urna(self):
        self.voto.set('FIM')
        self.teclado.voto = ''
        self.janela.after(5000, self.atualizar_voto) # 5000 ms = 5s

urna = Urna()
urna.iniciar_urna()
    
